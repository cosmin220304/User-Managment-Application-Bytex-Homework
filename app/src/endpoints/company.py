from bson import json_util
from flask import request, Blueprint, Response

from src.models.company import Company
from src.utils.decorators import session, http_handling, is_authorized, is_admin_or_self, is_admin, action_log

company_bp = Blueprint('companies', __name__, url_prefix='/companies')


@company_bp.route('', methods=['GET'])
@http_handling
@session
@is_authorized
def get_companies(context, user):
    companies = Company.get_companies(context, request)
    return Response(content_type='application/json', status=200, response=json_util.dumps(companies))


@company_bp.route('', methods=['POST'])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="CREATE COMPANY")
def post_company(context, user):
    body = request.json
    Company.create_company(context, body)
    return Response(status=201, response="Resource created")


@company_bp.route('/<company_id>', methods=['PUT'])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="UPDATE COMPANY")
def put_company(context, company_id, user):
    body = request.json
    Company.update_company(context, body, company_id)
    return Response(status=200, response="Resource updated")


@company_bp.route('/<company_id>', methods=['DELETE'])
@http_handling
@session
@is_authorized
@is_admin
@action_log(action="DELETE COMPANY")
def delete_company(context, company_id, user):
    Company.deactivate_company(context, company_id)
    return Response(status=200, response="Resource deleted")
