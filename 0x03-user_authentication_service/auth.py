#!/usr/bin/env python3
"""
    This module contains the authorization methods
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
        This method is used to hash the password

        Arguments:
            password: This is rthe password to be hashed

        Return: this method return the hashed password in the using
                bcrypt
    """
    b_password = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b_password, salt)

    return hashed_password
