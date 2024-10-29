import requests, re

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def error(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def validate_username(db, usr_username):
    # Ensure username was submitted
    if not usr_username:
        return "Brukernavn mangler", 400

    # Check length
    if len(usr_username) < 2:
        return "Brukernavnet må ha minst 2 tegn", 400
    if len(usr_username) > 20:  # Max length
        return "Brukernavnet kan ikke være mer enn 20 tegn", 400

    # Check for allowed characters (alphabetical only, no spaces/symbols)
    if not re.match("^[A-Za-z]+$", usr_username):
        return "Brukernavnet kan kun inneholde bokstaver (a - z) uten mellomrom og symboler", 400

    # Check if the username already exists
    rows = db.execute("SELECT * FROM users WHERE username = ?", usr_username)
    if len(rows) != 0:
        return "Brukernavnet er allerede tatt", 400

    return None  # Indicate that validation passed


def validate_password(usr_password, usr_username):
    # Ensure password was submitted
    if not usr_password:
        return "Passord mangler", 400

    # Check length
    if len(usr_password) < 6:
        return "Passordet må ha minst 6 tegn", 400
    if len(usr_password) > 20:  # Max length
        return "Passordet kan ikke være mer enn 20 tegn", 400

    # Check for required character variety
    if not re.search(r"[A-Z]", usr_password):  # At least one uppercase letter
        return "Passordet må inneholde minst én stor bokstav", 400
    if not re.search(r"[a-z]", usr_password):  # At least one lowercase letter
        return "Passordet må inneholde minst én liten bokstav", 400
    if not re.search(r"[0-9]", usr_password):  # At least one number
        return "Passordet må inneholde minst ett tall", 400
    # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", usr_password):  # At least one special character
    #     return "Passordet må inneholde minst ett spesialtegn", 400

    # Check against common passwords
    common_passwords = ["password", "123456", "123456789", "qwerty", "abc123"]  # Example list
    if usr_password.lower() in common_passwords:
        return "Passordet er for vanlig. Velg et sterkere passord.", 400

    # Check if the password contains the username
    if usr_username.lower() in usr_password.lower():
        return "Passordet kan ikke være brukernavnet ditt", 400

    return None  # Indicate that validation passed


def validate_email(email):
    # Ensure email is provided
    if not email:
        return "E-postadresse mangler", 400

    # Use a regular expression to validate the email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return "Ugyldig e-postadresse", 400

    return None  # Indicate that validation passed

def validate_cellphone(cellphone_number):
    # Ensure phone number is provided
    if not cellphone_number:
        return "Telefonnummer mangler", 400

    # Use a regular expression to validate the phone number format
    phone_number_regex = r'^\d{8}$'  # Only 8 digits are allowed
    if not re.match(phone_number_regex, cellphone_number):
        return "Ugyldig telefonnummer. Det må være 8 siffer uten mellomrom.", 400

    return None  # Indicate that validation passed