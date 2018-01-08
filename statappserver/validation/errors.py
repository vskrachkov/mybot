"""
    module: errors.py

    Defines all specific errors that can be raised in validation package
"""

class ValidationError(Exception):
    message = 'Validation error'

    def __init__(self, message):
        self.message = message
