import re

from src.schemas.users import user_schema
from src.schemas.companies import company_schema
from src.utils.exceptions import InvalidBody
from bson import objectid


def validate_user_schema(body, action_type):
    validate_schema(body, user_schema, action_type)


def validate_company_schema(body, action_type):
    validate_schema(body, company_schema, action_type)


def validate_schema(body, schema, action_type):
    for field, restriction in schema.items():
        body_value = body.get(field)

        if not body_value:
            if action_type == 'CREATE':  # required/default is for when field has no value
                if 'required' in restriction:
                    raise InvalidBody(f"{field} is required", status=400)
                if 'default' in restriction:
                    body[field] = restriction['default']
            continue

        if restriction['type'] == [objectid.ObjectId]:
            mongodb_ids = []

            if not isinstance(body_value, list):
                raise InvalidBody(f"{field} should be an array of mongodb objectId", status=400)
            for string_id in body_value:
                if not objectid.ObjectId.is_valid(string_id):
                    raise InvalidBody(f"{field} has an invalid mongodb objectId", status=400)
                mongodb_ids.append(objectid.ObjectId(string_id))

            body[field] = mongodb_ids
            continue

        if not isinstance(body_value, restriction['type']):
            wanted_type = restriction['type'].__name__
            received_type = type(body_value).__name__
            raise InvalidBody(f"{field} is of type {wanted_type} but received {received_type}", status=400)

        if 'min_length' in restriction:
            if len(body_value) < restriction['min_length']:
                raise InvalidBody(f"{field} should be at least {restriction['min_length']}", status=400)

        if restriction.get("is_email"):
            email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
            result = re.search(email_regex, body_value)
            if not result:
                raise InvalidBody(f"Email address is not valid for field {field}", status=400)
