from bson import json_util
from flask import request, Blueprint, Response

from src.models.logs import Logs
from src.utils.decorators import session, http_handling, is_authorized, is_admin

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')


@logs_bp.route('', methods=['GET'])
@http_handling
@session
@is_authorized
@is_admin
def get_logs(context, user):
    companies = Logs.get_logs(context, request)
    return Response(content_type='application/json', status=200, response=json_util.dumps(companies))
