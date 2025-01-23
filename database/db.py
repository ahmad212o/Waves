import sqlite3
import logging
from contextlib import contextmanager

DB = "./database/search_results.db"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@contextmanager
def get_cursor(connection):
    """
    Context manager for SQLite cursor with exception handling.
    Provides a cursor for database operations and ensures commit/rollback and cursor closing.
    """
    cursor = connection.cursor()
    try:
        logging.info("Starting new database operation.")
        yield cursor
        connection.commit()
        logging.info("Transaction committed.")
    except sqlite3.DatabaseError as e:
        connection.rollback()
        logging.error(f"Database error occurred: {e}")
        raise
    finally:
        cursor.close()
        logging.info("Cursor closed.")


def execute_or_fetch_query(
    query: str,
    params=None,
    db: str = DB,
    fetch: bool = False,
):
    """
    Executes a query or fetches results based on the `fetch` parameter.
    Logs each operation and provides error handling.
    """
    try:
        with sqlite3.connect(db) as con:
            with get_cursor(con) as cur:
                if params:
                    if isinstance(params[0], tuple):
                        cur.executemany(query, params)
                        logging.info(f"Executed multiple queries with parameters.")
                    else:
                        cur.execute(query, params)
                        logging.info(f"Executed query with parameters: {params}")
                else:
                    cur.execute(query)
                    logging.info(f"Executed query without parameters.")
                return cur.fetchall() if fetch else None
    except sqlite3.DatabaseError as e:
        logging.error(f"Error during query execution: {e}")
        return None


def init_db(db=DB):
    """
    Initializes the database by creating tables if they don't exist.
    Logs the database schema creation.
    """
    schema = """
    CREATE TABLE IF NOT EXISTS search_terms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL UNIQUE,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS search_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE,
        snippet TEXT,
        search_term_id INTEGER NOT NULL,
        content_type TEXT,
        FOREIGN KEY (search_term_id) REFERENCES search_terms(id) ON DELETE CASCADE
        );
    """
    try:
        with sqlite3.connect(db) as con:
            with get_cursor(con) as cur:
                cur.executescript(schema)
                logging.info("Database schema created or verified.")
    except sqlite3.DatabaseError as e:
        logging.error(f"Error initializing database: {e}")
