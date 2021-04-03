from src.schemas.users import user_schema
from src.schemas.companies import company_schema
from src.utils.exceptions import InvalidBody


def validate_user_schema(body):
    validate_schema(body, user_schema)


def validate_company_schema(body):
    validate_schema(body, company_schema)


def validate_schema(body, schema):
    for field, restriction in schema.items():
        body_value = body.get(field)
        if not body_value:
            if 'required' in restriction:
                raise InvalidBody(f"{field} is required", status=400)
            if 'default' in restriction:
                body[field] = restriction['default']
            continue

        if not isinstance(body_value, restriction['type']):
            wanted_type = restriction['type'].__name__
            received_type = type(body.get(field)).__name__
            raise InvalidBody(f"{field} is of type {wanted_type} but received {received_type}", status=400)

        if 'min_length' in restriction:
            print(restriction['min_length'])
            if len(body_value) < restriction['min_length']:
                raise InvalidBody(f"{field} should be at least {restriction['min_length']}", status=400)
