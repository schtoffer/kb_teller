from flask import Flask, g
import sqlite3

# Configure application
app = Flask(__name__)
DATABASE = "app_database.db"  # Name of your SQLite database file

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

def init_db():
    """Initialize the database with the schema from schema.sql if it doesn't already exist."""
    with sqlite3.connect(DATABASE) as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())  # Executes the entire schema.sql script

# Run init_db() directly to initialize the database when the app starts
init_db()

@app.teardown_appcontext
def close_db(exception):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)