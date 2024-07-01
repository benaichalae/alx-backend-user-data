#!/usr/bin/env python3
""" Protecting PII """

from typing import List
import logging
import re
from mysql.connector import connect, MySQLConnection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Returns the log message obfuscated """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f"{m.group(0).split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializes class instance """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Returns logger object """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    """ Connects to MySQL server with environmental vars """
    config = {
        'user': environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        'password': environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        'host': environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        'database': environ.get("PERSONAL_DATA_DB_NAME")
    }
    return connect(**config)


def main() -> None:
    """ Retrieves all rows in the users table and logs each row """
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()

    for row in cursor.fetchall():
        row_dict = dict(zip(['name', 'email', 'phone', 'ssn', 'password', 'ip', 'last_login', 'user_agent'], row))
        log_message = '; '.join([f"{key}={value}" for key, value in row_dict.items()])
        logger.info(log_message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
