class MissingApiKeyError(Exception):
    pass


class GandiAuth:
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, req):
        if not self.api_key:
            raise MissingApiKeyError()

        req.headers["Authorization"] = "Apikey {}".format(self.api_key)
        return req
