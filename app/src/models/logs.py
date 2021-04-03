from src.adapters.logs import LogsAdapter
from src.models.rest import Rest


class Logs(LogsAdapter, Rest):
    @classmethod
    def get_logs(cls, context, request):
        search = cls.get_search(request)
        offset, limit = cls.get_pagination(request)
        logs = [log for log in context.logs.find(search).skip(offset).limit(limit)]
        total = len(logs)
        return Logs().to_json(total, logs)
