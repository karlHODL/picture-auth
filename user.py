"""A class that can represent a user."""

class User:
    """A representation of a user"""
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key