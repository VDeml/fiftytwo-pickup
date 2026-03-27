import click
import os
import random
import sqlite3


from datetime import datetime
from flask import Flask, g, render_template, request, redirect, session, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from helpers import apology, login_required, usd
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__, instance_relative_config=True)
# We probably don't want to store the key in plain sight, but for now this is fine
app.config['SECRET_KEY'] = 'g?\xce\xf7\x1a#\x88+a N\x08\xf7\xce\xc1\x15B\n\xeb\xc3M\xe3\xcbm'
# Tell Flask where database lives
app.config["DATABASE"] = os.path.join(app.instance_path, "database.db")
# Storing this somewhere in the code, per flask-login documentation, don't know why yet
login_manager = LoginManager()

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

# Create a "form" class
class NamerForm(FlaskForm):
    name = StringField("What's your name brother?", validators=[DataRequired()])
    submit = SubmitField("Submit meeee")


@app.route("/")
@login_required
def index():
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?",(session["user_id"],))
        row = cursor.fetchone()
        if row is None:
            return apology("User not found", 403)


        conn.commit()
        conn.close()

        return render_template("index.html", user = row[1])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchone()
        # Ensure username exists and password is correct
        if rows is None or not check_password_hash(
            rows[3], request.form.get("password")
        ):
            conn.close()
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]
        conn.close()
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route('/name', methods=['GET', 'POST'])
@login_required
def name():
	name = None
	form = NamerForm()
	# Validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		
	return render_template("name.html", 
		name = name,
		form = form)

@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Shuffle a deck of cards, view it, then turn it over and type back the correct order of the cards"""
    if request.method == "POST":
        # once player pushes the button, generate deck and shuffle it
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['H', 'S', 'C', 'D']
        deck = [value + suit for suit in suits for value in values]
        random.shuffle(deck)
        return render_template("play.html", deck=deck)
    else:
        return render_template("play.html")

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
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        username_check = cursor.fetchall()
        if len(username_check) != 0:
            return apology("Username taken", 400)
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        email_check = cursor.fetchall()
        if len(email_check) != 0:
            return apology("Email taken", 400)
        password_hash = generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)
       
        # inserts a new row into the users table with newly registered users credentials
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,)) 
        user_login = cursor.fetchone()
        session["user_id"] = user_login[0]


        conn.commit()
        conn.close()

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/test")
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)