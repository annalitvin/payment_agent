class SignGenerator:

    def generate(self, *args, **kwargs):
        raise NotImplementedError


class ApiBase:

    def post(self, *args, **kwargs):
        raise NotImplementedError
