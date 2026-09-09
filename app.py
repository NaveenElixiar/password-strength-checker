from flask import Flask, render_template, request
import re

app = Flask(__name__)


def check_password(password):
    score = 0

    length = len(password) >= 8
    uppercase = bool(re.search(r"[A-Z]", password))
    lowercase = bool(re.search(r"[a-z]", password))
    number = bool(re.search(r"[0-9]", password))
    special = bool(re.search(r"[@#$%!]", password))

    if length:
        score += 1
    if uppercase:
        score += 1
    if lowercase:
        score += 1
    if number:
        score += 1
    if special:
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    checks = {
        "length": length,
        "uppercase": uppercase,
        "lowercase": lowercase,
        "number": number,
        "special": special
    }

    return strength, checks


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    checks = None

    if request.method == "POST":
        password = request.form.get("password", "")
        result, checks = check_password(password)

    return render_template(
        "index.html",
        result=result,
        checks=checks
    )


if __name__ == "__main__":
    app.run(debug=False)