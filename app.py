import click
import os
import random

from datetime import datetime
from flask import Flask, flash, g, render_template, request, redirect, session, current_app
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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "database.db")
# And initialize the database
db = SQLAlchemy(app)
# Storing this somewhere in the code, per flask-login documentation, don't know why yet
login_manager = LoginManager()

# Create model for my SQLAlchemy
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a string... supposed to be useful for debugging? It's a standard
    def __repr__(self):
        return '<Name %r>' % self.username

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Create a "form" class
class NamerForm(FlaskForm):
    name = StringField("What's your name brother?", validators=[DataRequired()])
    submit = SubmitField("Submit meeee")


@app.route("/")
@login_required
def index():
    user = User.query.filter_by(id=session["user_id"]).first()
    if not user:
        return apology("User not found", 403)
    
    return render_template("index.html", user = user)


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

        #Checking for correct username, password, logging user in
        user = User.query.filter_by(username=request.form.get("username")).first()
        if not user or not check_password_hash(user.password_hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = user.id
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
        action = request.form.get("action")

        if action == "shuffle":
            # once player pushes the button, generate deck and shuffle it
            values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            suits = ['H', 'S', 'C', 'D']
            deck = [value + suit for suit in suits for value in values]
            random.shuffle(deck)
            session["deck"] = deck
            return render_template("play.html", deck=session["deck"])
        
        elif action == "submit":
            submitted_cards = []
            for i in range(52):
                submitted_cards.append(request.form.get(f"card{i}"))
            deck = session.get("deck")
            if deck == submitted_cards:
                return apology("WELL DONE")
            else:
                return apology ("WRONG")

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
            return apology("Password and password confirmation must match")
        
        #NEW WAY using SQLAlchemy
        username = request.form.get("username")
        email = request.form.get("email")
        username_check = User.query.filter_by(username=username).first()
        email_check = User.query.filter_by(email=email).first()
        if username_check is not None:
            return apology("Username taken", 400)
        if email_check is not None:
            return apology("Email taken", 400)
        password_hash = generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        flash("You did it!")



        return redirect("/")

    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)