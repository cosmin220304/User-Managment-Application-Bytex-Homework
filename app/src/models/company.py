import bson

from src.adapters.company import CompanyAdapter
from src.models.rest import Rest
from src.utils.exceptions import Conflict
from src.utils.validators import validate_company_schema


class Company(CompanyAdapter, Rest):
    @classmethod
    def get_companies(cls, context, request):
        search = cls.get_search(request)
        offset, limit = cls.get_pagination(request)
        companies = [company for company in context.companies.find(search).skip(offset).limit(limit)]
        total = len(companies)
        return cls.to_json(total, context, companies)

    @classmethod
    def populate_company(cls, context, company):
        employees = context.users.find({"companies_id": bson.ObjectId(oid=str(company["_id"]))})
        company["employees_ids"] = [str(employee["_id"]) for employee in employees]
        print(company["employees_ids"])
        return company

    @classmethod
    def create_company(cls, context, body):
        validate_company_schema(body, action_type="CREATE")
        if cls.get_company_by_name(context, body.get("name")):
            raise Conflict("This company name already exists", status=409)
        company = Company()
        company.to_object(body)
        context.companies.insert(company.__dict__)

    @classmethod
    def update_company(cls, context, body, company_id):
        validate_company_schema(body, action_type="UPDATE")
        company = cls.get_company_by_id(context, company_id)
        updated_company = Company()
        updated_company.to_object(body)
        context.companies.update_one({"_id": company["_id"]}, {"$set": updated_company.__dict__})

    @classmethod
    def deactivate_company(cls, context, company_id):
        company = cls.get_company_by_id(context, company_id)
        company["active"] = False
        context.companies.update_one({"_id": company["_id"]}, {"$set": company})

    @classmethod
    def get_company_by_id(cls, context, company_id):
        company = context.companies.find_one({"_id": bson.ObjectId(oid=str(company_id))})
        if not company or not company.get("active"):
            raise Conflict("Company does not exist", status=404)
        return company

    @classmethod
    def get_company_by_name(cls, context, name):
        return context.companies.find_one({"name": name})
