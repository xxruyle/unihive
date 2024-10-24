import sqlite3

"""
Decided to go with SQLite for development since
its embedded and thus very easy for everyone to
install. SQLite implements a subset of SQL that
is interoperable with PostgresSQL allowing easy
migration to a more fitting database later.
"""

DATABASE_FILE = "app/database/unihive.db"

connection = sqlite3.connect(DATABASE_FILE)

################################################################################

def query(query, parameters, *, count = None):
    """
    Wrapper function for all database queries. Used
    to abstract away the database & add portability.
    """

    try:
        cursor = connection.cursor()
        result = cursor.execute(query, parameters)
        connection.commit()
    except sqlite3.Error as e:
        print("[QUERY ERROR]", e)
        return False
    finally:
        cursor.close()

    if count is None:
        return result.fetchall()
    else:
        return result.fetchmany(count)

################################################################################

def create_tables():
    """
    Create the database tables. Theoretically,
    only ever needs to be run once per install.
    """

    tables = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY,
            created         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            last_login      TIMESTAMP,
            username        VARCHAR NOT NULL,
            password        VARCHAR NOT NULL,
            profile_picture VARCHAR,
            university      INTEGER
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_post_views (
            id      INTEGER PRIMARY KEY,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            user    INTEGER NOT NULL,
            post    INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_post_likes (
            id      INTEGER PRIMARY KEY,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            is_like BOOL DEFAULT TRUE,
            user    INTEGER NOT NULL,
            post    INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_courses (
            id     INTEGER PRIMARY KEY,
            user   INTEGER NOT NULL,
            course INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS universities (
            id          INTEGER PRIMARY KEY,
            created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            name        VARCHAR NOT NULL,
            description VARCHAR,
            logo        VARCHAR
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS university_moderator (
            id         INTEGER PRIMARY KEY,
            user       INTEGER NOT NULL,
            university INTEGER NOT NULL,
            tier       INTEGER DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS courses (
            id            INTEGER PRIMARY KEY,
            created       TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            name          VARCHAR NOT NULL,
            description   VARCHAR,
            course_number VARCHAR,
            department    INTEGER,
            hours         INTEGER,
            university    INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS course_moderators (
            id     INTEGER PRIMARY KEY,
            user   INTEGER NOT NULL,
            course INTEGER NOT NULL,
            tier   INTEGER DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS departments (
            id           INTEGER PRIMARY KEY,
            created      TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            name         VARCHAR NOT NULL,
            abbreviation VARCHAR,
            university   INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS course_ratings (
            id         INTEGER PRIMARY KEY,
            created    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            user       INTEGER NOT NULL,
            course     INTEGER NOT NULL,
            difficulty REAL,
            grade      INT, -- ENUM
            hours      INT,
            instructor VARCHAR,
            syllabus   VARCHAR
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY,
            created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            title       VARCHAR NOT NULL,
            content     VARCHAR NOT NULL,
            author      INTEGER NOT NULL,
            course      INTEGER NOT NULL,
            likes       INTEGER DEFAULT 0,
            dislikes    INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            is_reply    BOOL DEFAULT FALSE,
            parent      INTEGER DEFAULT NULL
        );
        """
    ]

    try:
        cursor = connection.cursor()
        for table in tables:
            cursor.execute(table)
        connection.commit()
    except sqlite3.Error as e:
        print("[TABLE ERROR]", e)
        return False
    finally:
        cursor.close()
    
    return True

################################################################################

create_tables()