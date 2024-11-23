# Filename: db.py
# Description: This module contains DB related logic
# Inputs: N/A
# Output: N/A
# Authors: Andrew Ward
# Creation Date: 10/24/2024

import sqlite3

"""
Decided to go with SQLite for development since
its embedded and thus very easy for everyone to
install. SQLite implements a subset of SQL that
is interoperable with PostgresSQL allowing easy
migration to a more fitting database later.
"""

DATABASE_FILE = "app/database/unihive.db"

# Create a connection to the database housed inside the database file.
connection = sqlite3.connect(DATABASE_FILE, check_same_thread = False)

################################################################################

def query(query: str, parameters: tuple = tuple(), *, count: int = None):
    """
    Wrapper function for all database queries. Used
    to abstract away the database & add portability.

    :param query: SQL query to execute safely.
    :param parameters: Injection proof params.
    :param count: Number of rows to fetch for.
    """

    try:
        cursor = connection.cursor()               # Create a database cursor
        result = cursor.execute(query, parameters) # Execute the query safely
        connection.commit()                        # Commit the changes to DB

        if count is None:                  # If the count was not set
            return result.fetchall()       # Fetch every row in query
        if count == 1:                     # If the count was set one
            return result.fetchone()       # Fetch a single query row
        else:                              # If count was other value
            return result.fetchmany(count) # Fetch desired row amount

    except sqlite3.Error as e:
        # If the query encounters an error,
        # print the error and return false.
        print("[QUERY ERROR]", e)
        return False

    finally:
        # Always close the database cursor.
        cursor.close()

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
            username        VARCHAR UNIQUE NOT NULL,
            password        VARCHAR NOT NULL,
            profile_picture VARCHAR
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
            post    INTEGER NOT NULL,
            UNIQUE(user, post) ON CONFLICT REPLACE
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
            name        VARCHAR UNIQUE NOT NULL,
            acronym     VARCHAR UNIQUE,
            description VARCHAR,
            logo        VARCHAR
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_universities (
            id         INTEGER PRIMARY KEY,
            user       INTEGER NOT NULL,
            university INTEGER NOT NULL
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
            university    INTEGER NOT NULL,
            popularity_score INTEGER DEFAULT 0 
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
            author_id   INTEGER NOT NULL, 
            course      INTEGER NOT NULL,
            likes       INTEGER DEFAULT 0,
            dislikes    INTEGER DEFAULT 0,
            reply_count INTEGER DEFAULT 0,
            is_reply    BOOL DEFAULT FALSE,
            parent      INTEGER DEFAULT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS syllabus (
            id          INTEGER PRIMARY KEY,
            coursename  VARCHAR NOT NULL,
            filename    VARCHAR NOT NULL,
            file        BLOB NOT NULL 
        );
        """

    ]

    try:
        # Create database cursor
        cursor = connection.cursor()

        for table in tables:      # For every table listed above,
            cursor.execute(table) # Create the table for the DB.

        # Commit query to database.
        connection.commit()

    except sqlite3.Error as e:
        # If the query encounters an error,
        # print the error and return false.
        print("[TABLE ERROR]", e)
        return False

    finally:
         # Always close the database cursor.
        cursor.close()

    # Return True on success
    return True

################################################################################

# Initialize the tables on load
create_tables()
