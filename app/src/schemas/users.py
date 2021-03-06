from bson import objectid

user_schema = {
    'email': {
        'type': str,
        'min_length': 1,
        'required': True,
        'is_email': True,
    },
    'first_name': {
        'type': str,
        'min_length': 1,
    },
    'last_name': {
        'type': str,
        'min_length': 1,
    },
    'phone': {
        'type': str,
        'min_length': 10,
    },
    'admin': {
        'type': bool,
    },
    'active': {
        'type': bool,
        'default': True
    },
    'password': {
        'type': str,
        'min_length': 5,
        'required': True,
    },
    'companies_id': {
        'type': [objectid.ObjectId],  # fk in mongodb basically
    }
}
