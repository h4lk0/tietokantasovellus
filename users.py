from secrets import token_hex
from flask import abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["csrf_token"] = token_hex(16)
        return True
    return False

def logout():
    del session["user_id"]
    del session["username"]
    del session ["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT into users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def check_csrf(token):
    if session["csrf_token"] != token:
        abort(403)

def check_admin():
    id = session["user_id"]
    sql = "SELECT is_admin FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    permission = result.fetchone()
    return permission[0]

def user_id():
    return session.get("user_id")
