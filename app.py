import os
import sqlite3
from flask import Flask, g, render_template

app = Flask(__name__, instance_relative_config=True)

# Tell Flask where database lives
app.config["DATABASE"] = os.path.join(app.instance_path, "database.db")


# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)