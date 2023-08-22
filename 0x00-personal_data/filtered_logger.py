#!/usr/bin/env python3
"""
This module defines a function that returns an obfuscated log message
"""
import re
import logging
import os
import mysql.connector
from typing import List


PII_FIELDS = ("email", "name", "ssn", "password", "phone")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    This function will return a log message that is obfuscated

    Args:
        fields __List[str]__: a list of strings representing
        all fields to obfuscate

        redaction __List[str]__: a string representing by
        what the field will be obfuscated

        message __str__: a string representing the log line

        separator __str__: a string representing by which
        character is separating all fields in the log line (message)

    Returns:
        An obfuscated log msg
    """
    for field in fields:
        message = re.sub(fr'{field}=[^{separator}]+',
                         f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter Class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ';'

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Formates the log record """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Creates and returns a logger"""
    # Create logger with name
    logger = logging.getLogger('user_data')
    # Set logging level
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connects to a database"""
    db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    # Create a MySQL connection
    connection = mysql.connector.connect(
        user=db_username,
        port=3306,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection
