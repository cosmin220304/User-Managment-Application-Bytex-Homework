import bcrypt
import hashlib
import bson

from numpy import random
from binascii import a2b_qp
from src.models.company import Company
from src.utils.exceptions import Unauthorized
from src.schemas.users import user_schema


class UserAdapter:
    @classmethod
    def to_json(cls, total, context, results):
        return {
            "total": total,
            "items": [
                {
                    "_id": str(user["_id"]),
                    "email": user.get("email", ""),
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                    "companies": cls.get_companies_for_user(context, user)
                } for user in results if user.get("active")
            ]
        }

    @classmethod
    def get_companies_for_user(cls, context, user):
        companies = []

        for company_id in user.get("companies_id", []):
            company = context.companies.find_one({"_id": bson.ObjectId(oid=str(company_id))})
            if company:
                companies.append(company)

        total = len(companies)
        company_details = Company()
        return company_details.to_json(total, context, companies)

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
