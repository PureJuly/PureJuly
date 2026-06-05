import os
import time
from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.dirname(__file__)}/trashbin.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False, unique=True)

    def __str__(self):
        return f"id: {self.id}, name: {self.name}, pw: {self.pw}, key: {self.key}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {"id": self.id, "name": self.name, "key": self.key}


class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    description = db.Column(db.Text)

    def to_dict(self):
        date = datetime.fromtimestamp(self.created_at).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "id": self.id,
            "created_at": date,
            "type": self.type,
            "user": self.user,
            "description": self.description,
        }


class Bin(db.Model):
    __tablename__ = "bin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    is_full = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_full": self.is_full,
        }


# --- uno calls
@app.route("/open", methods=["GET"])
def open_bin():
    key = request.args.get("key")
    if not key:
        return "invalid input", 400

    user = User.query.filter_by(key=key).first()

    if user:
        user_id = user.id
        log = Log(created_at=int(time.time()), user=user_id, type="open")
        db.session.add(log)
        db.session.commit()

        return "ok", 200
    else:
        return "there's no such user", 200


@app.route("/close", methods=["GET"])
def close_bin():
    key = request.args.get("key")
    if not key:
        log = Log(created_at=int(time.time()), type="close", description="auto closed")

    else:
        user = User.query.filter_by(key=key).first()
        user_id = user.id
        log = Log(created_at=int(time.time()), user=user_id, type="close")

    if user:
        db.session.add(log)
        db.session.commit()

        return "ok", 200
    else:
        return "no", 200


@app.route("/full", methods=["GET"])
def full_bin():
    number = request.args.get("number")
    if not number:
        return "invalid input", 400

    try:
        bin = db.session.get(Bin, number)

        log = Log(
            created_at=int(time.time()), type="full", description=f"full: bin {bin.id}"
        )
        bin.is_full = 1

        db.session.add(log)
        db.session.commit()

        return "ok", 200
    except:
        return "error occurred", 500


@app.route("/empty", methods=["GET"])
def empty_bin():
    number = request.args.get("number")
    if not number:
        return "invalid input", 400

    try:
        bin = db.session.get(Bin, number)

        log = Log(
            created_at=int(time.time()),
            type="empty",
            description=f"empty: bin {bin.id}",
        )
        bin.is_full = 0

        db.session.add(log)
        db.session.commit()

        return "ok", 200
    except:
        return "error occurred", 500


# ------ dashboard (readonly)
@app.route("/logs", methods=["GET"])
def get_logs():
    length = request.args.get("q")
    offset = request.args.get("from")
    log_type = request.args.get("type")
    print(length, offset)
    if not length or not length.isdigit():
        return "invalid input", 400
    if not offset or not offset.isdigit():
        return "invalid input", 400

    if log_type in ["open", "close", "full", "empty", "user_update"]:
        logs = (
            Log.query.order_by(Log.id.desc())
            .filter_by(type=log_type)
            .offset(offset)
            .limit(length)
            .all()
        )
    else:
        logs = Log.query.order_by(Log.id.desc()).offset(offset).limit(length).all()

    logs = [log.to_dict() for log in logs]
    return jsonify(logs), 200


@app.route("/bin_status", methods=["GET"])
def get_bin_status():
    try:
        bins = Bin.query.all()
        bins = [i.to_dict() for i in bins]

        return bins, 200
    except:
        return "error occurred", 500


@app.route("/all_users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    users = [i.to_dict() for i in users]

    return users


# ------ dashboard (write)
# --- user
@app.route("/edit_user", methods=["POST"])
def edit_user():
    try:
        user_id = request.form["id"]
    except KeyError:
        return "invalid request", 400

    new_key: str | None = None
    new_name: str | None = None
    try:
        user = db.session.get(User, user_id)
    except:
        return "there's no such user", 400

    desc = []

    if "name" in request.form:
        new_name = request.form["name"]
        old_name = user.name
        user.name = new_name
        desc.append(f"name changed: ({old_name} -> {new_name})")
    if "key" in request.form:
        new_key = request.form["key"]
        user.key = new_key
        desc.append("key changed")

    if not new_key and not new_name:
        return "incomplete requeset", 400

    try:
        desc = ", ".join(desc)
        log = Log(
            created_at=int(time.time()),
            user=user_id,
            type="user_update",
            description=desc,
        )
        db.session.add(log)
        db.session.commit()
        return "", 200
    except:
        db.session.rollback()
        return "error occured", 500


@app.route("/delete_user", methods=["POST"])
def delete_user():
    try:
        user_id = request.form["id"]
    except KeyError:
        return "invalid request", 400

    try:
        user = db.session.get(User, user_id)
        log = Log(
            created_at=int(time.time()),
            user=user_id,
            type="user_update",
            description=f"user {user_id} deleted",
        )
    except:
        return "there's no such user", 400

    try:
        db.session.add(log)
        db.session.delete(user)
        db.session.commit()
    except:
        db.session.rollback()
        return "error occured", 500


@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        name = request.form["name"]
        key = request.form["key"]
    except KeyError:
        return "invalid request", 400

    user = User(name=name, key=key)

    try:
        db.session.add(user)
        db.session.flush()
        log = Log(
            created_at=int(time.time()),
            user=user.id,
            type="user_update",
            description=f"user {user.id} added",
        )
        db.session.add(log)
        db.session.commit()
        return "user added", 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return "error occured", 500


if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)
