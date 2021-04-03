class LogsAdapter:
    @staticmethod
    def to_json(total, results):
        return {
            "total": total,
            "items": [
                {
                    "_id": str(log["_id"]),
                    "user_id": str(log.get("user_id", "")),
                    "action": log.get("action"),
                    "body": log.get("body"),
                } for log in results
            ]
        }
