import sqlite3
from constants import (USER_DB_FILE, DATABASES_PATH, USER_ID_KEY, USERNAME_KEY, PASSWORD_KEY,)
from typing import Optional
from user import User
import uuid
import os
from passlib.hash import pbkdf2_sha256

KEYS_TABLE = 'keys'
USER_TABLE = 'users'

KEYS_TABLE_INIT = f'''CREATE TABLE {KEYS_TABLE} (
                {USER_ID_KEY} text PRIMARY KEY,
                {USERNAME_KEY} text NOT NULL)'''

USER_TABLE_INIT = f'''CREATE TABLE {USER_TABLE} (
                {USERNAME_KEY} text PRIMARY KEY,
                {PASSWORD_KEY} text NOT NULL,
                {USER_ID_KEY} text NOT NULL)'''

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password, password_hash):
    return pbkdf2_sha256.verify(password, password_hash)

def get_con():
    database_path = os.path.join(DATABASES_PATH, USER_DB_FILE)
    db_con = sqlite3.connect(database_path)
    return (db_con, db_con.cursor(),)

def get_user(auth_key) -> Optional[User]:
    db_con, cursor = get_con()

    AUTH_USER_TEMP = f"SELECT {USERNAME_KEY} FROM {KEYS_TABLE} WHERE {USER_ID_KEY} = ?"

    cursor.execute(AUTH_USER_TEMP, (auth_key,))
    result = cursor.fetchone()

    db_con.close()

    if not result:
        return None

    return User(result[0], auth_key)

def user_exists(username) -> bool:
    db_con, cursor = get_con()

    USER_EXISTS_TEMP = f"SELECT {USERNAME_KEY} FROM {USER_TABLE} WHERE {USERNAME_KEY} = ?"

    cursor.execute(USER_EXISTS_TEMP, (username,))
    result = cursor.fetchone()

    db_con.close()

    if not result:
        return False

    return True

def register_user(username, password) -> Optional[User]:
    db_con, cursor = get_con()

    USER_INSERT_TEMP = f"INSERT INTO {USER_TABLE} ({USERNAME_KEY}, {PASSWORD_KEY}, {USER_ID_KEY}) VALUES (?, ?, ?)"
    KEY_INSERT_TEMP = f"INSERT INTO {KEYS_TABLE} ({USER_ID_KEY}, {USERNAME_KEY}) VALUES (?, ?)"

    if user_exists(username):
        return None

    auth_key = str(uuid.uuid4())

    cursor.execute(USER_INSERT_TEMP, (username, hash_password(password), auth_key,))
    cursor.execute(KEY_INSERT_TEMP, (auth_key, username,))

    db_con.commit()
    db_con.close()

    return User(username, auth_key)

def authenticate_user(username, password) -> Optional[User]:
    db_con, cursor = get_con()

    USER_AUTH_TEMP = f"SELECT {PASSWORD_KEY}, {USER_ID_KEY} FROM {USER_TABLE} WHERE {USERNAME_KEY} = ?"

    cursor.execute(USER_AUTH_TEMP, (username,))
    result = cursor.fetchone()

    db_con.close()

    if result is None:
        return None

    if not verify_password(password, result[0]):
        return None

    return User(username, result[1])

def initialize() -> None:
    try:
        os.mkdir(DATABASES_PATH)
    except:
        pass

    db_con, cursor = get_con()

    try:
        cursor.execute(KEYS_TABLE_INIT)
    except:
        pass

    try:
        cursor.execute(USER_TABLE_INIT)
    except:
        pass

    db_con.commit()
    db_con.close()
