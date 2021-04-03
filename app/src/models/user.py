import datetime
import bson

from src.adapters.user import UserAdapter
from src.models.rest import Rest
from src.models.user_company import User_company
from src.utils.exceptions import Conflict, HTTPException
from src.utils.validators import validate_user_schema


class User(UserAdapter, Rest):
    @classmethod
    def get_users(cls, context, request):
        search = cls.get_search(request)
        offset, limit = cls.get_pagination(request)
        users = [user for user in context.users.find(search).skip(offset).limit(limit)]
        total = len(users)
        return cls.to_json(total, context, users)

    @classmethod
    def create_user(cls, context, body):
        validate_user_schema(body, action_type="CREATE")
        if cls.get_user_by_email(context, body.get("email")):
            raise Conflict("This email address is already used", status=409)
        user = User()
        user.to_object(body)
        context.users.insert(user.__dict__)

    @classmethod
    def update_user(cls, context, body, user_id):
        validate_user_schema(body, action_type="UPDATE")
        user = cls.get_user_by_id(context, user_id)
        updated_user = User()
        updated_user.to_object(body)
        if updated_user:
            context.users.update_one({"_id": user["_id"]}, {"$set": updated_user.__dict__})

    @classmethod
    def deactivate_user(cls, context, user_id):
        user = cls.get_user_by_id(context, user_id)
        user["active"] = False
        context.users.update_one({"_id": user["_id"]}, {"$set": user})

    @classmethod
    def add_company(cls, context, body, user_id):
        User_company.add_company_to_user(context, body, user_id)

    @classmethod
    def get_user_by_id(cls, context, user_id):
        user = context.users.find_one({"_id": bson.ObjectId(oid=str(user_id))})
        if not user or not user.get("active"):
            raise Conflict("User does not exist", status=404)
        return user

    @classmethod
    def get_user_by_email(cls, context, email):
        return context.users.find_one({"email": email})

    @classmethod
    def get_user_by_session(cls, context, session_id):
        return context.users.find_one({"session": session_id})

    @classmethod
    def login(cls, context, body):
        user = cls.get_user_by_email(context, body.get("email"))
        if not user or not user.get("active"):
            raise HTTPException("The email or the password is incorrect", status=400)

        password, _ = cls.generate_password(body.get("password"), user["salt"].encode("utf-8"))
        if password != user["password"]:
            raise HTTPException("The email or the password is incorrect", status=400)

        session_id = cls.generate_session()
        user["session"] = session_id
        user["session_create_time"] = datetime.datetime.now()

        context.users.update_one({"_id": user["_id"]}, {"$set": user})
        return session_id

    @classmethod
    def logout(cls, context, session_id):
        user = cls.get_user_by_session(context, session_id)
        if not user:
            raise HTTPException("User not found", status=400)
        user["session"] = None
        context.users.update_one({"_id": user["_id"]}, {"$set": user})
