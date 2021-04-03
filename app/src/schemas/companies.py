from bson import objectid

company_schema = {
    'name': {
        'type': str,
        'min_length': 1,
        'required': True,
    },
    'street': {
        'type': str,
        'min_length': 1,
    },
    'city': {
        'type': str,
        'min_length': 1,
    },
    'country': {
        'type': str,
        'min_length': 1,
    },
    'active': {
        'type': bool,
        'default': True
    }
}
