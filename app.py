from flask import Flask, request, render_template
import sqlite3
import subprocess
import hashlib
import pickle

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# VULN-01: SQL Injection
@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    return str(cursor.fetchall())


# VULN-02: Reflected XSS
@app.route("/search")
def search():
    query = request.args.get("q", "")

    return f"""
    <html>
        <body>
            <h1>Search results for: {query}</h1>
        </body>
    </html>
    """


# VULN-03: Command Injection
@app.route("/ping")
def ping():
    host = request.args.get("host")

    result = subprocess.check_output(
        "ping -c 1 " + host,
        shell=True
    )

    return result.decode()


# VULN-04: Hardcoded secret
API_KEY = "TEST_SECRET_123456789"


# VULN-06: Weak cryptography
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


# VULN-07: Insecure deserialization
@app.route("/load")
def load():
    data = request.args.get("data")

    decoded = bytes.fromhex(data)
    obj = pickle.loads(decoded)

    return str(obj)


if __name__ == "__main__":
    # VULN-09: Debug mode enabled
    app.run(debug=True)