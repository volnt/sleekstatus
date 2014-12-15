"""
Misc utils module

Contains the Mail class, the is_authenticated decorator and
the str_to_none function.
"""
from app.utils.mail import send_email
from app.utils.is_authenticated import is_authenticated
from app.utils.str_to_none import str_to_none

__all__ = ["send_email", "is_authenticated", "str_to_none"]
