#!/usr/bin/python3
"""
Intilize Storage Type
"""

from os import getenv


storage_t = getenv("CALEN_STORAGE_TYPE")

if storage_t == "db":
    from models.engine.db_storage import DBstorage
    storage = DBstorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
