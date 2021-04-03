from src.schemas.companies import company_schema


class CompanyAdapter:
    @staticmethod
    def to_json(total, results):
        return {
            "total": total,
            "items": [
                {
                    "_id": company["_id"],
                    "name": company.get("name", ""),
                    "street": company.get("street", ""),
                    "city": company.get("city", ""),
                    "country": company.get("country", ""),
                } for company in results if company.get("active")
            ]
        }

    def to_object(self, body):
        for key, value in body.items():
            if key in company_schema.keys():
                setattr(self, key, value)
