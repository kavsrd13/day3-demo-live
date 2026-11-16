import sqlite3

from flask import Flask, request

app = Flask(__name__)


@app.get("/user")
def user():
    username = request.args.get("name")
    connection = sqlite3.connect("users.db")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
        return str(cursor.fetchall())
    finally:
        connection.close()


@app.get("/hello")
def hello():
    name = request.args.get("name")
    return "<h1>Hello " + name + "</h1>"
