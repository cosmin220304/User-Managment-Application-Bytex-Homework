import bson

from src.schemas.companies import company_schema


class CompanyAdapter:
    @classmethod
    def to_json(cls, total, context, results):
        return {
            "total": total,
            "items": [
                {
                    "_id": str(company["_id"]),
                    "name": company.get("name", ""),
                    "street": company.get("street", ""),
                    "city": company.get("city", ""),
                    "country": company.get("country", ""),
                    "employees_ids": cls.get_employees_for_company(context, company)
                } for company in results if company.get("active")
            ]
        }

    @classmethod
    def get_employees_for_company(cls, context, company):
        employees = context.users.find({"companies_id": bson.ObjectId(oid=str(company["_id"]))})
        return [str(employee["_id"]) for employee in employees]

    def to_object(self, body):
        for key, value in body.items():
            if key in company_schema.keys():
                setattr(self, key, value)
