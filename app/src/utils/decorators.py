import logging
import functools

from bson import json_util
from datetime import datetime, timedelta
from flask import Response, request
from database_management import get_database_session
from src.models.user import User
from src.utils.exceptions import Unauthorized

logger = logging.getLogger(__name__)


def session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        context = get_database_session()
        kwargs["context"] = context
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e
    return wrapper


def http_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            status = getattr(e, "status", 500)
            return Response(status=status, response=json_util.dumps({"error": e.args[0]}))

    return wrapper


def is_authorized(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        context = kwargs.get("context") or get_database_session()
        session_id = request.headers.get("Authorization")

        user = User.get_user_by_session(context, session_id)

        if not session_id:
            raise Unauthorized("You are not allowed to access this.", status=401)

        if not user:
            raise Unauthorized("You are not allowed to access this.", status=401)

        if datetime.now() - user["session_create_time"] > timedelta(minutes=30):
            raise Unauthorized("You are not allowed to access this.", status=401)

        kwargs["user"] = user
        res = func(*args, **kwargs)
        user["session_create_time"] = datetime.now()
        context.users.update_one({"_id": user["_id"]}, {"$set": user})
        return res
    return wrapper


def is_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs["user"]
        print(user)
        if not user.get("admin"):
            raise Unauthorized("You are not allowed to access this.", status=403)
        return func(*args, **kwargs)
    return wrapper


def is_admin_or_self(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs["user"]
        updated_user_id = kwargs["user_id"]
        if not user.get("admin") and updated_user_id != user["_id"]:
            raise Unauthorized("You are not allowed to access this.", status=403)
        return func(*args, **kwargs)
    return wrapper


def action_log(action):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            context = kwargs["context"]
            user = kwargs["user"]
            user_id = user["_id"] if user else None
            # log = ActionLog(user_id=user_id, action=action, body=json_util.dumps(request.json))
            # print(log)
            # todo: come back
            # context.logs.insert(log)
            return res
        return wrapper
    return inner
