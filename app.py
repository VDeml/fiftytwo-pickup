import click
from flask import Flask, g, render_template, request, redirect, session, current_app
from helpers import apology, login_required, usd
import os
import sqlite3

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

@app.cli.command("init-db")
def init_db_command():
    """ Create database tables """
    init_db()
    print("Database created.")


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)