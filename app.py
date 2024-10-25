import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///kb_teller.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']

    """Show portfolio of stocks"""
    return render_template("index.html",
                           user_name=user_name
                           )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    data = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    user_balance = data[0]['cash']
    user_balance_formatted = usd(data[0]['cash'])

    # Check for valid input
    if request.method == "POST":
        symbol = request.form.get("symbol")
        data = lookup(symbol)

        if not data:
            return apology("That is not a valid ticker", 400)

        if not request.form.get("symbol"):
            return apology("You have to enter a ticket before you submit", 400)

        if not request.form.get("shares").isdigit() or int(request.form.get("shares")) < 1:
            return apology("You have to type a positive number", 400)

        # Compute transaction
        n_shares = int(request.form.get("shares"))
        share_price = data['price']
        order_sum = n_shares * share_price
        user_balance = user_balance - order_sum

        # Update users cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", user_balance, session["user_id"])

        # Track the transaction in purchases table
        db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], request.form.get("symbol"), n_shares, share_price)

        return redirect("/")
    else:
        return render_template("buy.html", user_balance_formatted=user_balance_formatted)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM purchases WHERE user_id = ?", session["user_id"])
    print(rows)
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logg-ut")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/ny-rapport", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        data = lookup(symbol)

        if not data:
            return apology("That is not a valid ticker", 400)

        if not request.form.get("symbol"):
            return apology("You have to enter a ticket before you submit", 400)

        price = usd(data['price'])

        return render_template("quoted.html", data=data, price=price)
    else:
        return render_template("rapport.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Brukernavn mangler", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Passord mangler", 400)

        # Ensure confirmation of password was submitted
        elif not request.form.get("confirmation"):
            return apology("Du må bekrefte passordet", 400)

        # Ensure password and confirmation are the same
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passordene matcher ikke", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Check to see if username already exists
        if len(rows) != 0:
            return apology("Brukernavnet er allerede tatt", 400)

        # Hash the password
        pwdhash = generate_password_hash(request.form.get("password"))

        # Insert new user to the users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), pwdhash)

        # Retrieve the users id
        result = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        if result:  # Check if the result is not empty
            usr_id = result[0]['id']  # Extract the id from the first row
        else:
            usr_id = None  # Handle case where no user is found

        # Insert user detail to the user_details table
        db.execute("INSERT INTO user_details (usr_fname, usr_lname, usr_email, usr_cellphone, user_id) VALUES (?, ?, ?, ?, ?)", 
                   request.form.get("fname"), 
                   request.form.get("lname"),
                   request.form.get("email"),
                   request.form.get("cellphone"),
                   usr_id)

        # Log the user in
        rows = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        user_id = rows[0]["id"]
        session["user_id"] = user_id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
