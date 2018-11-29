from .constants import (QUEUE_FILE, FILES_PATH, DATABASES_PATH, \
                        DOC_ID_KEY, USER_ID_KEY, USERNAME_KEY, \
                        DOC_NAME_KEY, EXTENSION_KEY, DOUBLE_SIDED_KEY, \
                        COLOR_KEY, COPIES_KEY, PRINTER_STATUS_KEY,)
from .document import (Document, get_doc_name,)
from .print_settings import (PrintSettings,)
from .user import (User,)

from typing import (Optional, Tuple, List,)
from werkzeug.utils import (secure_filename,)
import enum
import sqlite3
import os
import uuid

valid_extensions = ['doc', 'docx', 'txt', 'pdf']

START_POSITION_KEY = 'start_pos'
CURRENT_POSITION_KEY = 'pos'

QUEUE_TABLE = 'queue'
SETTINGS_TABLE = 'settings'
DOCUMENT_LOADING_TABLE = 'loading'
PRINTER_STATUS_TABLE = 'status'


QUEUE_TABLE_INIT = f'''CREATE TABLE {QUEUE_TABLE} (
            {DOC_ID_KEY} text PRIMARY KEY,
            {USER_ID_KEY} text NOT NULL,
            {USERNAME_KEY} text NOT NULL,
            {DOC_NAME_KEY} text NOT NULL,
            {EXTENSION_KEY} text NOT NULL,
            {START_POSITION_KEY} INTEGER NOT NULL,
            {CURRENT_POSITION_KEY} INTEGER NOT NULL)'''

SETTINGS_TABLE_INIT = f'''CREATE TABLE {SETTINGS_TABLE} (
            {DOC_ID_KEY} text PRIMARY KEY,
            {DOUBLE_SIDED_KEY} INTEGER NOT NULL,
            {COLOR_KEY} INTEGER NOT NULL,
            {COPIES_KEY} INTEGER NOT NULL)'''

DOCUMENT_LOADING_TABLE_INIT = f'''CREATE TABLE {DOCUMENT_LOADING_TABLE} (
            {USER_ID_KEY} text PRIMARY KEY,
            {USERNAME_KEY} text NOT NULL,
            {DOC_ID_KEY} text NOT NULL,
            {DOC_NAME_KEY} text NOT NULL,
            {EXTENSION_KEY} text NOT NULL)'''

PRINTER_STATUS_TABLE_INIT = f'''CREATE TABLE {PRINTER_STATUS_TABLE} (
            {PRINTER_STATUS_KEY} INTEGER PRIMARY KEY)'''


class DocumentIndex(enum.Enum):
    DOC_ID_INDEX = 0
    USER_ID_INDEX = 1
    USERNAME_INDEX = 2
    DOC_NAME_INDEX = 3
    EXTENSION_INDEX = 4
    START_POSITION_INDEX = 5
    CURRENT_POSITION_INDEX = 6

class SettingsIndex(enum.Enum):
    DOC_ID_INDEX = 0
    DOUBLE_SIDED_INDEX = 1
    COLOR_INDEX = 2
    COPIES_INDEX = 3

class LoadingIndex(enum.Enum):
    USER_ID_INDEX = 0
    USERNAME_INDEX = 1
    DOC_ID_INDEX = 2
    DOC_NAME_INDEX = 3
    EXTENSION_INDEX = 4

def validate_file(filename: str) -> Optional[Tuple[str, str]]:
    filename = secure_filename(filename)
    _, extension = os.path.splitext(filename)
    extension = extension[1:]
    if not extension in valid_extensions:
        return None

    return (filename, extension,)

def get_con():
    database_path = os.path.join(DATABASES_PATH, QUEUE_FILE)
    db_con = sqlite3.connect(database_path)
    return (db_con, db_con.cursor(),)

def remove_file(document: Document) -> bool:
    filepath = os.path.join(FILES_PATH, document.get_saved_name())
    os.remove(filepath)
    return True

def load_doc(user: User, doc_name: str) -> Optional[str]:

    FETCH_DOC = f"SELECT * FROM {DOCUMENT_LOADING_TABLE} WHERE {USER_ID_KEY} = ?"
    LOAD_DOC = f"INSERT INTO {DOCUMENT_LOADING_TABLE} ({USER_ID_KEY}, {USERNAME_KEY}, {DOC_ID_KEY}, {DOC_NAME_KEY}, {EXTENSION_KEY}) VALUES (?, ?, ?, ?, ?)"
    UPDATE_DOC = f"UPDATE {DOCUMENT_LOADING_TABLE} SET ({DOC_ID_KEY}, {DOC_NAME_KEY}, {EXTENSION_KEY}) = (?, ?, ?) WHERE {USER_ID_KEY} = (?)"

    file_tuple = validate_file(doc_name)

    if not file_tuple:
        return None

    db_con, cursor = get_con()

    filename, extension = file_tuple

    cursor.execute(FETCH_DOC, (user.user_id,))
    loaded_doc = cursor.fetchone()

    doc_id = str(uuid.uuid4())

    if not loaded_doc:
        cursor.execute(LOAD_DOC, (user.user_id, user.username, doc_id, filename, extension,))
    else:
        delete_extension = loaded_doc[LoadingIndex.EXTENSION_INDEX.value]
        delete_doc_id = loaded_doc[LoadingIndex.DOC_ID_INDEX.value]
        delete_filename = get_doc_name(delete_doc_id, delete_extension)
        delete_filepath = os.path.join(FILES_PATH, delete_filename)
        os.remove(delete_filepath)

        cursor.execute(UPDATE_DOC, (doc_id, filename, extension, user.user_id,))

    db_con.commit()
    db_con.close()

    return get_doc_name(doc_id, extension)

def unload_doc(user: User, settings: PrintSettings) -> Optional[Document]:
    db_con, cursor = get_con()

    FETCH_DOC = f"SELECT * FROM {DOCUMENT_LOADING_TABLE} WHERE {USER_ID_KEY} = ?"
    REMOVE_FROM_LOADING = f"DELETE FROM {DOCUMENT_LOADING_TABLE} WHERE {USER_ID_KEY} = ?"

    cursor.execute(FETCH_DOC, (user.user_id,))
    loaded_doc = cursor.fetchone()

    if not loaded_doc:
        db_con.close()
        return None

    cursor.execute(REMOVE_FROM_LOADING, (user.user_id,))

    db_con.commit()
    db_con.close()

    document = Document( \
        loaded_doc[LoadingIndex.USERNAME_INDEX.value], loaded_doc[LoadingIndex.USER_ID_INDEX.value], \
        loaded_doc[LoadingIndex.DOC_NAME_INDEX.value], loaded_doc[LoadingIndex.EXTENSION_INDEX.value], \
        loaded_doc[LoadingIndex.DOC_ID_INDEX.value], settings, 0)

    return document


def get_len() -> int:
    db_con, cursor = get_con()

    GET_DOC_IDS = f"SELECT {DOC_ID_KEY} FROM {QUEUE_TABLE}"

    cursor.execute(GET_DOC_IDS)
    response = cursor.fetchall()

    db_con.close()

    return len(response)

def tuple_to_doc(doc_tuple, settings_tuple) -> Document:
    settings = PrintSettings( \
        int(settings_tuple[SettingsIndex.DOUBLE_SIDED_INDEX.value]), \
        settings_tuple[SettingsIndex.COPIES_INDEX.value], \
        bool(settings_tuple[SettingsIndex.COLOR_INDEX.value]))

    cur_pos = doc_tuple[DocumentIndex.CURRENT_POSITION_INDEX.value] + 1
    start_pos = doc_tuple[DocumentIndex.START_POSITION_INDEX.value] + 1

    progress = ((start_pos - cur_pos) / start_pos) * 100

    return Document( \
        doc_tuple[DocumentIndex.USERNAME_INDEX.value], \
        doc_tuple[DocumentIndex.USER_ID_INDEX.value], \
        doc_tuple[DocumentIndex.DOC_NAME_INDEX.value], \
        doc_tuple[DocumentIndex.EXTENSION_INDEX.value], \
        doc_tuple[DocumentIndex.DOC_ID_INDEX.value], \
        settings, \
        progress)

def get_queue(user: Optional[User] = None) -> List[Document]:
    db_con, cursor = get_con()

    GET_DOC_QUEUE = f"SELECT * FROM {QUEUE_TABLE}"
    GET_SETTING_QUEUE = f"SELECT * FROM {SETTINGS_TABLE}"

    cursor.execute(GET_DOC_QUEUE)
    doc_response = cursor.fetchall()

    cursor.execute(GET_SETTING_QUEUE)
    settings_response = cursor.fetchall()

    db_con.close()

    doc_list = []
    for doc_tuple in doc_response:
        settings_tuple = next(x for x in settings_response if doc_tuple[DocumentIndex.DOC_ID_INDEX.value] == x[SettingsIndex.DOC_ID_INDEX.value])
        doc_list.append(tuple_to_doc(doc_tuple, settings_tuple))

    if not user:
        return doc_list
    else:
        return [doc for doc in doc_list if doc.user_id == user.user_id]

def top() -> Optional[Document]:
    if get_len() <= 0:
        return None

    db_con, cursor = get_con()

    GET_TOP_QUEUE = f"SELECT * FROM {QUEUE_TABLE} WHERE {CURRENT_POSITION_KEY}=0"
    GET_MATCHING_SETTINGS = f"SELECT * FROM {SETTINGS_TABLE} WHERE {DOC_ID_KEY}=?"

    cursor.execute(GET_TOP_QUEUE)
    doc_result = cursor.fetchone()

    cursor.execute(GET_MATCHING_SETTINGS, (doc_result[DocumentIndex.DOC_ID_INDEX.value],))
    settings_result = cursor.fetchone()

    db_con.close()

    return tuple_to_doc(doc_result, settings_result)

def pop() -> None:
    queue_top = top()
    if not queue_top:
        return None
    remove_file(queue_top)

    db_con, cursor = get_con()

    DELETE_FROM_QUEUE = f"DELETE FROM {QUEUE_TABLE} WHERE {DOC_ID_KEY}=?"
    DELETE_FROM_SETTINGS = f"DELETE FROM {SETTINGS_TABLE} WHERE {DOC_ID_KEY}=?"
    MOVE_FORWARD_IN_QUEUE = f"UPDATE {QUEUE_TABLE} SET {CURRENT_POSITION_KEY} = {CURRENT_POSITION_KEY} - 1"

    cursor.execute(DELETE_FROM_QUEUE, (queue_top.doc_id,))
    cursor.execute(DELETE_FROM_SETTINGS, (queue_top.doc_id,))
    cursor.execute(MOVE_FORWARD_IN_QUEUE)

    db_con.commit()
    db_con.close()

def add_to_queue(document: Document) -> None:
    db_con, cursor = get_con()

    QUEUE_INSERT = f'''INSERT INTO {QUEUE_TABLE} (
                        {DOC_ID_KEY}, {USER_ID_KEY}, {USERNAME_KEY}, {DOC_NAME_KEY},
                        {EXTENSION_KEY}, {START_POSITION_KEY}, {CURRENT_POSITION_KEY})
                        VALUES (?, ?, ?, ?, ?, ?, ?)'''

    SETTINGS_INSERT = f'''INSERT INTO {SETTINGS_TABLE} (
                        {DOC_ID_KEY}, {DOUBLE_SIDED_KEY}, {COLOR_KEY},
                        {COPIES_KEY}) VALUES (?, ?, ?, ?)'''

    settings = document.settings
    queue_len = get_len()

    cursor.execute(QUEUE_INSERT, (document.doc_id, document.user_id, document.username, document.name, document.ext, queue_len, queue_len,))
    cursor.execute(SETTINGS_INSERT, (document.doc_id, int(settings.double_sided), int(settings.color), settings.copies,))

    db_con.commit()
    db_con.close()

def delete_doc(user: User, doc_id: str) -> bool:
    db_con, cursor = get_con()

    FIND_DOC = f"SELECT * FROM {QUEUE_TABLE} WHERE {DOC_ID_KEY} = ?"
    GET_MATCHING_SETTINGS = f"SELECT * FROM {SETTINGS_TABLE} WHERE {DOC_ID_KEY}=?"
    DELETE_FROM_QUEUE = f"DELETE FROM {QUEUE_TABLE} WHERE {DOC_ID_KEY} = ?"
    DELETE_FROM_SETTINGS = f"DELETE FROM {SETTINGS_TABLE} WHERE {DOC_ID_KEY} = ?"
    ADJUST_POSITION = f"UPDATE {QUEUE_TABLE} SET {CURRENT_POSITION_KEY} = {CURRENT_POSITION_KEY} - 1 WHERE {CURRENT_POSITION_KEY} > ?"

    cursor.execute(FIND_DOC, (doc_id,))
    doc_info = cursor.fetchone()

    if doc_info is None or doc_info[DocumentIndex.USER_ID_INDEX.value] != user.user_id:
        return False

    cursor.execute(GET_MATCHING_SETTINGS, (doc_info[DocumentIndex.DOC_ID_INDEX.value],))
    settings_info = cursor.fetchone()

    remove_file(tuple_to_doc(doc_info, settings_info))

    cursor.execute(DELETE_FROM_QUEUE, (doc_id,))
    cursor.execute(DELETE_FROM_SETTINGS, (doc_id,))
    cursor.execute(ADJUST_POSITION, (doc_info[DocumentIndex.CURRENT_POSITION_INDEX.value],))

    db_con.commit()
    db_con.close()

    return True

def update_status(status: bool) -> None:
    db_con, cursor = get_con()

    UPDATE_STATUS = f"UPDATE {PRINTER_STATUS_TABLE} SET {PRINTER_STATUS_KEY} = ?"

    cursor.execute(UPDATE_STATUS, (int(status),))

    db_con.commit()
    db_con.close()

def get_status() -> bool:
    db_con, cursor = get_con()

    GET_STATUS = f"SELECT {PRINTER_STATUS_KEY} FROM {PRINTER_STATUS_TABLE}"

    cursor.execute(GET_STATUS)
    status = cursor.fetchone()

    db_con.close()

    return bool(status[0])

def initialize() -> None:
    try:
        os.mkdir(DATABASES_PATH)
    except:
        pass

    db_con, cursor = get_con()
    try:
        cursor.execute(QUEUE_TABLE_INIT)
    except:
        pass

    try:
        cursor.execute(SETTINGS_TABLE_INIT)
    except:
        pass

    try:
        cursor.execute(DOCUMENT_LOADING_TABLE_INIT)
    except:
        pass

    try:
        cursor.execute(PRINTER_STATUS_TABLE_INIT)
        INSERT_TRUE = f"INSERT INTO {PRINTER_STATUS_TABLE} ({PRINTER_STATUS_KEY}) VALUES (0)"
        cursor.execute(INSERT_TRUE)
    except:
        pass

    db_con.commit()
    db_con.close()
