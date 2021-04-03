user_schema = {
    'email': {
        'type': 'string',
        'minlength': 1,
        'required': True,
    },
    'firstName': {
        'type': 'string',
        'minlength': 1,
    },
    'lastName': {
        'type': 'string',
        'minlength': 1,
    },
    'phone': {
        'type': 'string',
        'minlength': 10,
    },
    'admin': {
        'type': 'bool',
        'default': False
    },
    'active': {
        'type': 'bool',
        'default': True
    },
    'password': {
        'type': 'bool',
        'minlength': 5,
        'required': True,
    },
}
