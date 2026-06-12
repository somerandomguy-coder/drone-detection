import os
from os import environ
from uuid import uuid4

import aiosqlite
import dotenv

dotenv.load_dotenv()

DATABASE_PATH = environ.get("database_path", "app/database.db")

print(f"Database configuration:\n: database_path {DATABASE_PATH}")


async def initialize_database():
    if not os.path.exists(DATABASE_PATH):
        print("database file not existed, creating new file")
    async with aiosqlite.connect(DATABASE_PATH) as conn:
        await conn.executescript("""PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS USERS (
        id TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS PREDICTION (
        path INTEGER PRIMARY KEY,
        prediction TEXT,
        user_id TEXT,
        FOREIGN KEY (user_id) REFERENCES USERS(id) ON DELETE CASCADE
        );
        """)
        await conn.commit()


async def save_prediction(id, filepath, result):
    if filepath is None:
        raise Exception()

    async with aiosqlite.connect(DATABASE_PATH) as conn:
        await conn.execute(
            """
        INSERT into USERS(id) VALUES (?);
            """,
            (id,),
        )
        await conn.execute(
            """
        INSERT into PREDICTION(user_id, path, prediction) VALUES (?, ?, ?);
        """,
            (
                id,
                filepath,
                result,
            ),
        )
        await conn.commit()
    return 0
