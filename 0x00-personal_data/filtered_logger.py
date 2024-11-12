#!/usr/bin/env python3
"""
    This Module contains a Function filter_datum that returns the log
    message obfuscated
"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """
        This function returns the log message obfuscated

        Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be
                obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
    """
    for key in fields:
        message = re.sub(fr'{key}=[^ {seperator}]+', f"{key}={redaction}",
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """This is the intialization of the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """This method is used to format the logging"""
        msg = super().format(record)
        final_message = filter_datum(self.fields, self.REDACTION, msg,
                                     self.SEPARATOR)
        return final_message
