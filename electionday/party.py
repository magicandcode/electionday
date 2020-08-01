from __future__ import annotations
from dataclasses import dataclass
import sqlite3
from typing import Iterable

import electionday.database as db


@dataclass
class Party:
    """Represents an electable party.
    """
    _id: int
    name: str
    symbol: str = ''
    votes: int = 0
    selector: str = ''


def create_table(cursor: sqlite3.Cursor) -> None:
    """Create parties table if it doesn't exist.

    To be called from a create_tables function in setup.

    Args:
        cursor (sqlite3.Cursor): Connection cursor

    Raises:
        sqlite3.Error: SQLite exception
        Exception: Generic exception
    """
    query: str = '''CREATE TABLE IF NOT EXISTS parties(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(30) NOT NULL UNIQUE,
        symbol VARCHAR(60),
        votes NUMERIC(10) NOT NULL DEFAULT 0
    )'''
    try:
        cursor.execute(query)
    except sqlite3.OperationalError as e:
        print(repr(e))
        raise e
    except Exception as e:
        print(repr(e))
        raise e


def populate_table(cursor: sqlite3.Cursor, parties: Iterable):
    """[summary]

    Args:
        cursor (sqlite3.Cursor): [description]
        parties (Iterable): [description]

    Raises:
        e: [description]
        e: [description]
    """
    try:
        for party in parties:
            query: str = '''INSERT INTO parties(name, symbol)
                VALUES(?, ?)'''
            try:
                cursor.execute(query,
                    (party, f"{party.lower().split(' ')[0]}.png"))
            except sqlite3.IntegrityError as e:
                print(repr(e))
                continue
    except sqlite3.Error as e:
        print(repr(e))
        raise e
    except Exception as e:
        print(repr(e))
        raise e


@db.connect_with_cursor
def select_all(cursor: sqlite3.Cursor) -> Sequence[Party]:

    query: str = 'SELECT id, name, symbol, votes from parties ORDER BY name ASC'
    return [
        Party(
            _id=_id, name=name, selector=str(i+1), symbol=symbol, votes=votes)
        for i, (_id, name, symbol, votes) in enumerate(cursor.execute(query))
    ]


@db.connect_with_cursor
def select_results(cursor: sqlite3.Cursor) -> Sequence[Party]:

    query: str = '''SELECT id, name, symbol, votes from parties
                    ORDER BY votes DESC'''
    return [
        Party(
            _id=_id, name=name, selector=str(i+1), symbol=symbol, votes=votes)
        for i, (_id, name, symbol, votes) in enumerate(cursor.execute(query))
    ]


def get_by_selector(parties: Sequence[Party], selector: str) -> optional[Party]:
    for party in parties:
        if party.selector == selector:
            return party
    return None


@db.connect_with_cursor
def select_winners(cursor: sqlite3.Cursor) -> Sequence[Party]:

    query: str = 'SELECT MAX(votes) FROM parties'
    max_vote_count: int = cursor.execute(query).fetchone()[0]
    query: str = f'''SELECT id, name, symbol, votes from parties
                     WHERE votes = {max_vote_count}'''
    return [
        Party(
            _id=_id, name=name, selector=str(i+1), symbol=symbol, votes=votes)
        for i, (_id, name, symbol, votes) in enumerate(cursor.execute(query))
    ]


@db.connect_with_cursor
def get_by_id(cursor: sqlite3.Cursor, _id: int) -> Optional[Party]:

    query: str = 'SELECT id, name, symbol, votes FROM parties WHERE id = ?'
    _id, name, symbol, votes = cursor.execute(query, (_id,)).fetchone()
    return Party(_id=_id, name=name, symbol=symbol, votes=votes)


def add_vote(cursor: sqlite3.Cursor, party: Party) -> None:

    query: str = '''UPDATE parties SET votes = votes + 1 WHERE id = ?'''
    cursor.execute(query, (party._id,))
    party.votes += 1


if __name__ == '__main__':
    from pprint import pprint
    #pprint(select_all())
    party = get_by_id(9)
    #print(party)
    party.selector = '9'
