import bson
from bson import objectid

from src.models.rest import Rest
from src.utils.exceptions import InvalidBody, Conflict


class User_company(Rest):
    @classmethod
    def add_company_to_user(cls, context, body, user_id):
        user = cls.get_user_by_id(context, user_id)  # throws error if no user found

        if body.get("company"):
            company = cls.get_company_by_name(context, body["company"])
        elif body.get("company_id"):
            company = cls.get_company_by_id(context, body["company_id"])
        else:
            raise InvalidBody("No company name or id given (expected fields: company or company_id)", status=400)

        company_id = company.get("_id")
        if not company_id or not objectid.ObjectId.is_valid(company_id):
            raise InvalidBody("Company not found", status=404)

        company_id = objectid.ObjectId(company_id)
        context.users.update_one({"_id": user_id}, {"$addToSet": {"companies_id": company_id}})
        # note that $addToSet adds a value to an array unless the value is already present ^

    @classmethod
    def add_user_to_company(cls, context, body, company_id):
        company = cls.get_company_by_id(context, company_id)  # throws error if no company found

        if body.get("user_email"):
            user = cls.get_user_by_email(context, body["user_email"])
        elif body.get("user_id"):
            user = cls.get_user_by_id(context, body["user_id"])
        else:
            raise InvalidBody("No user email or id given (expected fields: user_email or user_id)", status=400)

        user_id = user.get("_id")
        if not user_id or not objectid.ObjectId.is_valid(user_id):
            raise InvalidBody("User not found", status=404)

        company_id = objectid.ObjectId(company_id)
        context.users.update_one({"_id": user_id}, {"$addToSet": {"companies_id": company_id}})

    # ik that is not dry, but i have circular dependency if i import company/ user
    @classmethod
    def get_company_by_id(cls, context, company_id):
        company = context.companies.find_one({"_id": bson.ObjectId(oid=str(company_id))})
        if not company or not company.get("active"):
            raise Conflict("Company does not exist", status=404)
        return company

    @classmethod
    def get_company_by_name(cls, context, name):
        return context.companies.find_one({"name": name})

    @classmethod
    def get_user_by_id(cls, context, user_id):
        user = context.users.find_one({"_id": bson.ObjectId(oid=str(user_id))})
        if not user or not user.get("active"):
            raise Conflict("User does not exist", status=404)
        return user

    @classmethod
    def get_user_by_email(cls, context, email):
        return context.users.find_one({"email": email})