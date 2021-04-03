import json
from flask import Blueprint, Response, request
from src.utils.decorators import session, http_handling

from src.models.user import User

login_bp = Blueprint('authorization', __name__, url_prefix='/')


@login_bp.route('login', methods=['POST'])
@session
@http_handling
def login(context):
    session_id = User.login(context, request.json)
    return Response(response=json.dumps({"session_id": session_id}), status=200)


@login_bp.route('logout', methods=['POST'])
@session
@http_handling
def logout(context):
    session_id = request.headers.get('Authorization')
    User.logout(context, session_id)
    return Response(response=json.dumps({'message': 'Logged out successfully'}), status=200)
