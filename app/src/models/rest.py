class Rest:
    @classmethod
    def add_search(cls, request):
        search = request.args.get('search')
        if not search:
            return {}
        return {"$text": {"$search": f"{search}"}}

    @classmethod
    def add_pagination(cls, request):
        page = request.args.get('page')
        limit = request.args.get('limit')
        if not page or not limit:
            return 0, 20
        limit = int(limit)
        offset = (int(page) - 1) * limit
        return offset, limit

