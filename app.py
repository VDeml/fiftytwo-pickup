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

""" Adding a function to run Schema.sql"""
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
    return render_template("index.html")


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



    else:
        return render_template("register.html")




if __name__ == "__main__":
    app.run(debug=True)