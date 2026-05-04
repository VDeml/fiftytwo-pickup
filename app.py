import json
import os
import random
import time 

from datetime import datetime
from flask import Flask, flash, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy

from helpers import apology, login_required
from sqlalchemy import ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__, instance_relative_config=True)
# We probably don't want to store the key in plain sight, but for now this is fine
app.config['SECRET_KEY'] = 'g?\xce\xf7\x1a#\x88+a N\x08\xf7\xce\xc1\x15B\n\xeb\xc3M\xe3\xcbm'
# Tell Flask where database lives
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "database.db")
# And initialize the database
db = SQLAlchemy(app)


# Create model for my SQLAlchemy
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationship to attempts table
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    # Create a string... supposed to be useful for debugging? It's a standard
    def __repr__(self):
        return '<Name %r>' % self.username

class Attempt(db.Model):
    __tablename__="attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    deck_order: Mapped[str] = mapped_column(Text, nullable=False)
    recall_order: Mapped[str | None] = mapped_column(Text, nullable=True)
    accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Relationship to users table
    user: Mapped["User"] = relationship(back_populates="attempts")

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# creating a custom Jinja filter to be ablte to decode JSON in history.html
@app.template_filter("fromjson")
def fromjson_filter(value):
    return json.loads(value) if value else []

@app.route("/")
@login_required
def index():
    user = User.query.filter_by(id=session["user_id"]).first()
    if not user:
        return apology("User not found", 403)
    
    return render_template("index.html", user = user)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    user = User.query.filter_by(id=session["user_id"]).first()
    attempts = Attempt.query.filter_by(user_id=session["user_id"]).all()
    if not attempts:
        flash("No attempts recorded", "danger")
    return render_template("history.html", user = user, attempts = attempts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide a username", "danger")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter your password", "danger")

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

@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Shuffle a deck of cards, view it, then turn it over and type back the correct order of the cards"""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        action = request.form.get("action") or data.get("action")

        if action == "shuffle":
            # once player pushes the button, generate deck and shuffle it
            values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            suits = ['H', 'S', 'C', 'D']
            deck = [value + suit for suit in suits for value in values]
            random.shuffle(deck)
            ## TESTING FEEATURE that uses only 2 values - King, Ace and 2 colors - Hearts, Spades
           # values = ['K', 'A']
           # suits = ['H', 'S']
            deck = [value + suit for suit in suits for value in values]
            random.shuffle(deck)
            session["deck"] = deck
            session["start_time"] = time.time()
            return render_template("play.html", deck=deck, start_time=session.get("start_time"))
        
        elif action == "submit":
            data = request.get_json(silent=True) or {}
            submitted_cards = data.get("cards", [])
            deck = session.get("deck")
            start_time = session.get("start_time")
            if start_time:
                duration = time.time() - start_time
            else:
                duration = None
            # Calculate the accuracy of players attempt
            correct_count = 0
            for i, card in enumerate(deck or []):
                if i < len(submitted_cards) and submitted_cards[i] == card:
                    correct_count += 1
            
            accuracy = (correct_count / len(deck)) * 100 if deck else 0

            # Next input the attempt into the database
            game = Attempt(user_id=session["user_id"],
                             deck_order=json.dumps(deck), 
                             recall_order=json.dumps(submitted_cards),
                             accuracy=accuracy,
                             duration_seconds=duration)
            db.session.add(game)
            db.session.commit()

            message = "WELL DONE" if deck == submitted_cards else "Incorrect"
            flash(
                f"{message} — Accuracy: {round(accuracy, 2)}%, "
                f"Correct: {correct_count}/{len(deck) if deck else 0}."
            )

            return jsonify({
                "accuracy": round(accuracy, 2),
                "correct": correct_count,
                "total": len(deck) if deck else 0,
                "message": message
            })
        else:
            return jsonify({"error": "Invalid action"}), 400

    else:
        return render_template("play.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Please fill out your username")
        
        if not request.form.get("email"):
            return apology("Please fill out your e-mail")

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
        flash("Registration successful!", 'primary')



        return redirect("/")

    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)