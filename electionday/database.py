import json
import sqlite3
from typing import Any, Callable, Generic, Optional, Sequence

import electionday.config as config


# Create database connection.
try:
    CONNECTION: sqlite3.Connection = sqlite3.connect(config.DB_PATH)
except sqlite3.Error as e:
    print(repr(e))
    raise e


def connect(fn: Callable) -> Callable:
    """Decorator to create and close connection while passing the
      connection to the decorated function.

    Creates connection using db path in the config module by default.

    Pass connection rather than cursor; Enables decorated function to
      use commit etc and can choose not to create an explicit cursor.
      However if a cursor is created, it needs to be closed inside the
      decorated function.

    Could take database path as argument, might be merit to do so for
      soliciting testing.

    Args:
        fn (Callable): Decorated function

    Raises:
        sqlite3.Error: Database exception
        Exception: Generic Exception

    Returns:
        Callable: Decorator wrapper function
    """
    def wrapper(*args, **kwargs) -> Any:
        """Decorator wrapper function.

        Using connection in a with block commits queries automatically.

        Raises:
            sqlite3.Error: Database exception
            Exception: Generic Exception

        Returns:
            Any: Query result, if any, or None
        """
        connection: optional[sqlit3.Connection] = None
        try:
            with CONNECTION as connection:
                if args:
                    args = (connection, *args)
                else:
                    kwargs['connection'] = connection
                return fn(*args, **kwargs)
        except sqlite3.Error as e:
            print(repr(e))
            raise e
        except Exception as e:
            print(repr(e))
            raise e
    return wrapper


def connect_with_cursor(fn: Callable):
    """Decorator to create and close connection while passing the
      connection cursor to the decorated function.

    Creates connection using db path in the config module by default.

    Pass connection rather than cursor; Enables decorated function to
      use commit etc and can choose not to create an explicit cursor.
      However if a cursor is created, it needs to be closed inside the
      decorated function.

    Could take database path as argument, might be merit to do so for
      soliciting testing.

    Args:
        fn (Callable): Decorated function
    """
    def wrapper(*args, **kwargs) -> Any:
        """Decorator wrapper function.

        Raises:
            sqlite3.Error: Database exception
            Exception: Generic Exception

        Returns:
            Any: Query result, if any, or None
        """
        cursor: Optional[sqlite3.Cursor] = None
        try:
            with CONNECTION as connection:
                cursor = connection.cursor()
                if args:
                    args = (cursor, *args)
                else:
                    kwargs['cursor'] = cursor
                return fn(*args, **kwargs)
        except sqlite3.Error as e:
            print(repr(e))
            raise e
        except Exception as e:
            print(repr(e))
            raise e
        finally:
            if cursor:
                cursor.close()
    return wrapper


@connect
def create_tables(
    connection: sqlite3.Connection,
    *table_functions: Sequence[Callable],
) -> None:
    """[summary]

    Args:
        connection (sqlite3.Connection): [description]

    Raises:
        sqlite3.Error: Database exception
        Exception: Generic Exception
    """
    cursor: Optional[sqlite3.Cursor] = None
    try:
        cursor = connection.cursor()
        for function in table_functions:
            function(cursor)
        connection.commit()
    except sqlite3.Error as e:
        print(repr(e))
        raise e
    except Exception as e:
        print(repr(e))
        raise e
    finally:
        if cursor:
            cursor.close()


def load_data() -> None:
    """Insert sample data from JSON file.

    Args:
        connection (sqlite3.Connection): Passed via decorator

    Raises:
        Exception: Generic Exception
    """
    # Get sample data.
    try:
        with open(config.DATA_PATH) as f:
            return json.load(f)
    except Exception as e:
        print(repr(e))
        raise e


@connect
def populate_tables(
    connection: sqlite3.Connection, *tables_data) -> None:
    """Populate tables with initial data.

    Args:
        connection (sqlite3.Connection): Database connection

    Raises:
        sqlite3.Error: Database exception
        Exception: Generic Exception
    """
    cursor: Optional[sqlite3.Cursor] = None
    try:
        cursor = connection.cursor()
    except sqlite3.Error as e:
        print(repr(e))
        raise e
    except Exception as e:
        print(repr(e))
        raise e
    try:
        for table_function, data in tables_data:
            table_function(cursor, data)
    finally:
        if cursor:
            cursor.close()
