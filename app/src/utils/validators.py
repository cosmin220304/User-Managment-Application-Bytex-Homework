import re

from src.utils.exceptions import InvalidBody


def validate_user_body(body):
    validate_email(body.get("email"))
    validate_password(body.get("password"))


def validate_password(password):
    if not password:
        raise InvalidBody("You must provide a password", status=400)


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    result = re.search(regex, email)
    if not result:
        raise InvalidBody("Email address is not valid", status=400)

