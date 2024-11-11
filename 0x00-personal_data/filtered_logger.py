#!/usr/bin/env python3
"""
    This Module contains a Function filter_datum that returns the log
    message obfuscated
"""
from typing import List
import re


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
