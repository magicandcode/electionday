from dataclasses import dataclass
import sqlite3
from typing import Iterable, Optional

import electionday.database as db
import electionday.party as party
import electionday.voter as voter

@dataclass
class Voter:
    """Represents a registered voter.
    """
    _id: int
    name: str
    voter_id: str
    has_voted: bool = False


def create_table(cursor: sqlite3.Cursor) -> None:
    """Create parties table if it doesn't exist.

    To be called from a create_tables function in setup.

    Args:
        cursor (sqlite3.Cursor): Connection cursor

    Raises:
        sqlite3.Error: SQLite exception
        Exception: Generic exception
    """
    query: str = '''CREATE TABLE IF NOT EXISTS voters(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(60) NOT NULL,
        voter_id VARCHAR(12) NOT NULL UNIQUE,
        has_voted NUMERIC(1) NOT NULL DEFAULT 0
    )'''
    try:
        cursor.execute(query)
    except sqlite3.OperationalError as e:
        print(repr(e))
        raise e
    except Exception as e:
        print(repr(e))
        raise e


def populate_table(cursor: sqlite3.Cursor, voters: Iterable):

    try:
        for voter_id, name in voters:
            query: str = (f"""INSERT INTO voters(name, voter_id)
                VALUES(?, ?)""")
            try:
                cursor.execute(query, (name, voter_id))
            except sqlite3.IntegrityError:
                continue
    except sqlite3.Error as e:
        print(repr(e))
        raise e
    except Exception as e:
        print(repr(e))
        raise e


@db.connect_with_cursor
def is_valid(cursor: sqlite3.Cursor, name: str, voter_id: str) -> bool:

    query: str = 'SELECT name FROM voters WHERE voter_id = ?'
    try:
        return (name.lower()
            == cursor.execute(query, (voter_id,)).fetchone()[0].lower())
    except TypeError:
        False


@db.connect_with_cursor
def get_by_voter_id(cursor: sqlite3.Cursor, voter_id: str) -> Optional[Voter]:

    query: str = '''SELECT id, name, has_voted FROM voters WHERE voter_id = ?'''
    _id, name, has_voted = cursor.execute(query, (voter_id,)).fetchone()
    return Voter(_id=_id, name=name, voter_id=voter_id, has_voted=bool(int(has_voted)))


def vote(cursor: sqlite3.Cursor, voter: Voter) -> None:

    query: str = '''UPDATE voters SET has_voted = 1 WHERE id = ?'''
    cursor.execute(query, (voter._id,))
    voter.has_voted = True


if __name__ == '__main__':
    from pprint import pprint
    print(is_valid('Chandra', '1014'))
    voter = get_by_voter_id('1014')
    pprint(voter)
    print(vote(voter))
    pprint(voter)
