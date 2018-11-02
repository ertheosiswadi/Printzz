import sqlite3
from constants import DB_FILE
from typing import Optional
from user import User
import uuid

KEYS_TABLE='''CREATE TABLE keys (
            auth_key text PRIMARY KEY,
            uname text NOT NULL)'''

USER_TABLE = '''CREATE TABLE users (
            uname text PRIMARY KEY,
            pwd text NOT NULL,
            auth_key text NOT NULL)'''

def hash_password(password):
    return password

def get_user(auth_key) -> Optional[User]:
    db_con = sqlite3.connect(DB_FILE)

    AUTH_USER_TEMP = "SELECT uname FROM keys WHERE auth_key=?"

    cursor = db_con.cursor()
    cursor.execute(AUTH_USER_TEMP, (auth_key,))
    result = cursor.fetchone()

    db_con.close()

    if not result:
        return None

    return User(result[0], auth_key)

def user_exists(username) -> bool:
    db_con = sqlite3.connect(DB_FILE)

    USER_EXISTS_TEMP = "SELECT uname FROM users WHERE uname=?"

    cursor = db_con.cursor()
    cursor.execute(USER_EXISTS_TEMP, (username,))
    result = cursor.fetchone()

    db_con.close()

    if not result:
        return False

    return True

def register_user(username, password) -> Optional[str]:
    db_con = sqlite3.connect(DB_FILE)

    USER_INSERT_TEMP = "INSERT INTO users (uname, pwd, auth_key) VALUES (?, ?, ?)"
    KEY_INSERT_TEMP = "INSERT INTO keys (auth_key, uname) VALUES (?, ?)"

    if user_exists(username):
        return None

    auth_key = str(uuid.uuid4())

    cursor = db_con.cursor()
    cursor.execute(USER_INSERT_TEMP, (username, hash_password(password), auth_key,))
    cursor.execute(KEY_INSERT_TEMP, (auth_key, username,))

    db_con.commit()
    db_con.close()

    return User(username, auth_key)

def authenticate_user(username, password) -> Optional[User]:
    db_con = sqlite3.connect(DB_FILE)

    USER_AUTH_TEMP = "SELECT pwd, auth_key FROM users WHERE uname=?"

    cursor = db_con.cursor()
    cursor.execute(USER_AUTH_TEMP, (username,))
    result = cursor.fetchone()

    db_con.close()

    if result is None:
        return None

    if hash_password(password) != result[0]:
        return None

    return User(username, result[1])

def initialize():
    db_con = sqlite3.connect(DB_FILE)

    c = db_con.cursor()
    try:
        c.execute(KEYS_TABLE)
    except:
        pass

    try:
        c.execute(USER_TABLE)
    except:
        pass

    db_con.commit()
    db_con.close()
