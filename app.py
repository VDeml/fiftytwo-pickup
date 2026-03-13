import click
import os
import sqlite3

from flask import Flask, g, render_template, request, redirect, session, current_app
from helpers import apology, login_required, usd
from werkzeug.security import check_password_hash, generate_password_hash




app = Flask(__name__, instance_relative_config=True)

# Tell Flask where database lives
app.config["DATABASE"] = os.path.join(app.instance_path, "database.db")


# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

"""Adding a function to run Schema.sql"""
def init_db():
    with sqlite3.connect(app.config["DATABASE"]) as db:
        with open("schema.sql") as f:
            db.executescript(f.read())

# Initialize database with command-line interface
@app.cli.command("init-db")
def init_db_command():
    """ Create database tables """
    init_db()
    print("Database created.")


@app.route("/")
def index():
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        row = cursor.fetchone()
        cursor.execute("SELECT username, email FROM users")
        rows = cursor.fetchall()
        

        conn.commit()
        conn.close()

        return render_template("index.html", rows = rows, row = row)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide a username")
        
        if not request.form.get("password"):
            return apology("must provide a password")
        
        if not request.form.get("confirmation"):
            return apology("must provide password connfirmation")
        
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Password and passwrod confirmation must match")
        
        # ensure username and email are unique
        username = request.form.get("username")
        email = request.form.get("email")
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username, ))
        username_check = cursor.fetchall()
        if len(username_check) != 0:
            return apology("Username taken", 400)
        cursor.execute("SELECT email FROM users WHERE email = ?", (email, ))
        email_check = cursor.fetchall()
        if len(email_check) != 0:
            return apology("Email taken", 400)
        password_hash = generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)
       
        # inserts a new row into the users table with newly registered users credentials
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))

        conn.commit()
        conn.close()

        

        # And finally log user in
        #session["user_id"] = #probably use a tuple instead of a list of dicts?

        return redirect("/")

    else:
        return render_template("register.html")




if __name__ == "__main__":
    app.run(debug=True)