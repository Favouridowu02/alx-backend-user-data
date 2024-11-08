#!/usr/bin/env python3
"""
    This Module contains a Function filter_datum that returns the log
    message obfuscated
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, seperator: str) -> 
