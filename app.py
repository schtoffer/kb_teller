import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_babel import Babel, _
from werkzeug.security import check_password_hash, generate_password_hash


import helpers as h
from utils.date_utils import format_dates
from db import *

from utils.sql_utils import sql

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set the API key in an environment variable or a configuration
app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')

# Configure Babel settings
app.config['BABEL_DEFAULT_LOCALE'] = 'no'  # Default language
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'no']  # Supported languages

# Initialize Babel
babel = Babel(app)

# Locale selector function
def get_locale():
    # Check the 'lang' query parameter first, then fall back to session or `Accept-Language` header
    language = request.args.get('lang')
    if language:
        # Store the user's selection in the session for persistence
        session['lang'] = language
    else:
        # Use the stored selection or the browser's preferred language
        language = session.get('lang', request.accept_languages.best_match(['no', 'en']))
    
    print("Selected language: " + language)
    return language

babel.init_app(app, locale_selector=get_locale)

# Configure SQLite database
db = SQL(f"sqlite:///{DATABASE}")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@h.login_required
def index():
    # Logged in user id
    user_id = session["user_id"]

    # Prepare values for template rendering
    fname = get_fname(user_id)
    username = get_username(user_id)
    admin = is_admin(user_id)
    reporting_businesses = get_reporting_buinesses(user_id)

    # Render welcome page
    return render_template("index.html", fname=fname, username=username, is_admin=admin, reporting_businesses=reporting_businesses)

@app.route("/admin", methods=["GET", "POST"])
@h.login_required
def admin():
    # Retrieve user id
    user_id = session["user_id"]

    # Get user roles
    user_roles = DB.execute("SELECT role_name FROM user_roles WHERE user_id IN (?)", user_id)

    # Make sure the user is an admin
    is_admin = any(user_role['role_name'] == 'admin' for user_role in user_roles)

    if not is_admin:
        # Redirect to the home page if not an admin
        return redirect("/")
    
    else:
        # Retreive all businesses
        businesses = DB.execute("SELECT * FROM businesses")

        # Retrieve all users
        users = DB.execute("SELECT * FROM users")

        # Return the admin panel page
        return render_template("admin.html", 
                               businesses=businesses,
                               users=users)  # Replace with your actual admin template



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return h.apology("Du må oppgi brukernavn", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return h.apology("Du må oppgi passord", 403)

        # Query database for username
        rows = DB.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return h.apology("Du oppga ugyldig brukernavn og passord", 403)

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


@app.route("/rapporter", methods=["GET", "POST"])
@h.login_required
def rapporter():

    if request.method == "POST":
        business_id = request.form.get("business_id")
        
        # Get name of business
        business_name = sql("businesses", "name", business_id)

        # Get 14 formatted days
        formatted_dates = format_dates(14)

        return render_template("rapport.html", 
                               business_id=business_id, 
                               formatted_dates=formatted_dates,
                               business_name=business_name)
    else:
        return redirect("/")
    

@app.route("/registrer-bruker", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Define variables
        form_fname = request.form.get("fname").capitalize()
        form_lname = request.form.get("lname").capitalize()
        form_username = request.form.get("username").lower()
        form_pwd = request.form.get("password")
        form_pwd_repeat = request.form.get("confirmation")
        form_email = request.form.get("email").lower()
        form_cellphone = request.form.get("cellphone")

        print(form_fname, form_lname, form_username, form_pwd, form_email, form_cellphone)
        
        # Ensure first name is provided
        if not form_fname:
            error = "Fornavn mangler"
            return render_template('register.html', error=error)

        # Ensure last name is provided
        if not form_lname:
            error = "Etternavn mangler"
            return render_template('register.html', error=error)
        
        # Ensure last valid email is provided
        if (email_validation := h.validate_email(form_email)):
            return render_template('register.html', error=email_validation[0])
        
        # Validate phone number
        if (phone_validation := h.validate_cellphone(form_cellphone)):
            return render_template('register.html', error=phone_validation[0])
        # Ensure username was submitted correctly
        validation_error = h.validate_username(db, form_username)
        if validation_error:
            error = validation_error[0]
            return render_template('register.html', error=error)

        # Ensure password was submitted
        elif not form_pwd:
            error = "Pasord mangler"
            return render_template('register.html', error=error)

        # Ensure confirmation of password was submitted
        elif not form_pwd_repeat:
            error = "Du må bekrefte passordet"
            return render_template('register.html', error=error)

        # Ensure password and confirmation are the same
        elif request.form.get("confirmation") != request.form.get("password"):
            error = "Passordene du oppga er ikke like"
            return render_template('register.html', error=error)
        
        # Validate the password
        if (pwd_validation := h.validate_password(form_pwd, form_username)):
            return render_template('register.html', error=pwd_validation[0])

 
        # Hash the password
        pwdhash = generate_password_hash(form_pwd)

        # Insert new user to the users table
        
        DB.execute("INSERT INTO users (username, hash) VALUES (?, ?)", form_username, pwdhash)

        # Retrieve the users id
        result = DB.execute("SELECT id FROM users WHERE username = ?", form_username)
        if result:  # Check if the result is not empty
            usr_id = result[0]['id']  # Extract the id from the first row
        else:
            usr_id = None  # Handle case where no user is found

        # Insert user detail to the user_details table
        DB.execute("INSERT INTO user_details (usr_fname, usr_lname, usr_email, usr_cellphone, user_id) VALUES (?, ?, ?, ?, ?)", 
                   form_fname, 
                   form_lname,
                   form_email,
                   form_cellphone,
                   usr_id)

        # Log the user in
        rows = DB.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        user_id = rows[0]["id"]
        session["user_id"] = user_id

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    

@app.route("/registrer-tilbud", methods=["GET", "POST"])
def register_business():

    # Pass the API key to the template securely
    api_key = app.config['GOOGLE_MAPS_API_KEY']
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        pass
    else:
        return render_template('register-business.html', access_token=api_key)