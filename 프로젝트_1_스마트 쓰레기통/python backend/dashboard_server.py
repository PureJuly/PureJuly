import hashlib
import os

import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_SERVER_URL = "http://localhost:5000"
app.secret_key = "dev_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.dirname(__file__)}/session.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Text, primary_key=True)
    pw = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route("/")
@login_required
def main():
    try:
        response = requests.get(f"{DB_SERVER_URL}/bin_status")
        bins = response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        bins = []

    return render_template("main.html", bins=bins)


def hash_pw(pw, salt):
    return hashlib.scrypt(
        pw.encode("utf-8"), salt=bytes.fromhex(salt), n=16384, r=8, p=1
    ).hex()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("username")
        login_pw = request.form.get("password")

        if not login_id or not login_pw:
            return "잘못된 입력입니다.", 400

        user = User.query.get(login_id)
        if not user:
            return render_template(
                "login.html", error="아이디 또는 비밀번호가 일치하지 않습니다."
            )

        hashed_pw = hash_pw(login_pw, user.salt)
        print(hashed_pw == user.pw)

        if hashed_pw == user.pw:
            login_user(user)
            return redirect(url_for("main"))
        else:
            return render_template(
                "login.html", error="아이디 또는 비밀번호가 일치하지 않습니다."
            )

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/logs", methods=["GET"])
@login_required
def logs():
    page = int(request.args.get("page", 1))
    length = 20
    offset = (page - 1) * length
    log_type = request.args.get("type", "")

    params = {"q": length, "from": offset}
    if log_type:
        params["type"] = log_type

    try:
        response = requests.get(f"{DB_SERVER_URL}/logs", params=params)
        logs_data = response.json() if response.status_code == 200 else []

    except requests.exceptions.RequestException:
        logs_data = []

    return render_template("logs.html", logs=logs_data, page=page, log_type=log_type)


@app.route("/manage_user", methods=["GET", "POST"])
@login_required
def manage_user():
    if request.method == "POST":
        action = request.form.get("action")

        try:
            if action == "add":
                data = {
                    "name": request.form.get("name"),
                    "key": request.form.get("key"),
                }
                requests.post(f"{DB_SERVER_URL}/add_user", data=data)
            elif action == "edit":
                data = {"id": request.form.get("id")}
                # 빈 문자열이 아닌 경우에만 데이터에 포함
                if request.form.get("name"):
                    data["name"] = request.form.get("name")
                if request.form.get("key"):
                    data["key"] = request.form.get("key")
                requests.post(f"{DB_SERVER_URL}/edit_user", data=data)
            elif action == "delete":
                data = {"id": request.form.get("id")}
                requests.post(f"{DB_SERVER_URL}/delete_user", data=data)
        except requests.exceptions.RequestException:
            pass  # 실제 환경에서는 적절한 오류 처리가 필요합니다.

        return redirect(url_for("manage_user"))

    try:
        response = requests.get(f"{DB_SERVER_URL}/all_users")
        users = response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        users = []

    return render_template("manage_user.html", users=users)


if __name__ == "__main__":
    app.run("0.0.0.0", port=3000, debug=True)
