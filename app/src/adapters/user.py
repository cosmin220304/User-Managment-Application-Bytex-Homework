import bcrypt
import hashlib

from numpy import random
from binascii import a2b_qp
from src.utils.exceptions import Unauthorized
from src.schemas.users import user_schema

class UserAdapter:

    @staticmethod
    def to_json(total, results):
        return {
            "total": total,
            "items": [
                {
                    "_id": user["_id"],
                    "email": user.get("email", ""),
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                } for user in results if user.get("active")
            ]
        }

    def to_object(self, body):
        for key, value in body.items():
            if key == "password":
                password, salt = self.generate_password(value)
                self.password = password
                self.salt = salt
            elif key == "admin":
                raise Unauthorized("You are not allowed to change this.", status=403)
            elif key in user_schema.keys():
                setattr(self, key, value)

    @staticmethod
    def generate_password(password, salt=None):
        if salt is None:
            salt = bcrypt.gensalt()
        password = bcrypt.hashpw(a2b_qp(password), salt)
        return password.decode("utf-8"), salt.decode("utf-8")

    @staticmethod
    def generate_session():
        return hashlib.sha256(random.bytes(1024)).hexdigest()
