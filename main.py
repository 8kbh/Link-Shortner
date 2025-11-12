import random
import sqlite3
from contextlib import contextmanager
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, request, render_template
from flask_cors import CORS


DATABASE = "links.db"
app = Flask(__name__, static_url_path='/r/static', static_folder='static')
CORS(app)


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def grs(length: int) -> str:
    """Generate a random string of specified length."""
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
    return ''.join(random.choice(letters) for _ in range(length))


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@app.route("/r/")
def serve_r():
    return render_template("index.html")


@app.route("/r/<token>", methods=["GET"])
def my_redirect(token: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, link, view_count FROM links WHERE alias=?", (token, ))
        res = cursor.fetchone()
    if res:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE links SET view_count=? WHERE id=?", (res["view_count"] + 1, res["id"],))
            conn.commit()
        return redirect(res["link"])
    else:
        return redirect('/r/404')  # Return a 404 error if the token is not found


@app.route("/r/create", methods=["POST"])
def create():
    link = request.get_json().get("link", "")
    if not is_valid_url(link):
        return "Provided link is invalid", 400

    alias = grs(5)
    pwd = grs(16)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO links (alias, link, pwd) VALUES (?, ?, ?)", (alias, link, pwd))
        conn.commit()
    return jsonify({"alias": alias, "pwd": pwd})


@app.route("/r/statistic", methods=["get"])
def stat():
    pwd = request.args.get("pwd")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM links WHERE pwd=?", (pwd, ))
        res = cursor.fetchone()
    if res:
        return jsonify(dict(res))

    if not res:
        return "pwd is invalid", 403


@app.route("/r/edit", methods=["POST"])
def edit():
    pwd = request.args.get("pwd")
    link = request.get_json().get("link", "")
    if not is_valid_url(link):
        return "Provided link is invalid", 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE links SET link=? WHERE pwd=?", (link, pwd,))
        conn.commit()
    return "OK"


@app.route("/r/404")
def error():
    return "No link"


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)
