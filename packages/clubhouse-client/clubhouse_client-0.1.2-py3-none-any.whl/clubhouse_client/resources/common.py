from functools import wraps

import requests


def json_header(func):
    """An internal decorator to keep the json headers tidy"""

    @wraps(func)
    def _exec(*args, **kwargs):
        try:
            kwargs["headers"]["Content-Type"] = "application/json; charset=UTF-8"
        except (KeyError, TypeError) as exc:
            kwargs["headers"] = {}
            kwargs["headers"]["Content-Type"] = "application/json; charset=UTF-8"

        return func(*args, **kwargs)

    return _exec


class ClubhouseResource(object):
    """A generic Clubhouse super-class suitable for sub-classes"""

    def __init__(
        self, api_token, base_target="https://api.clubhouse.io/api/v3", debug=False
    ):
        self.api_token = api_token
        self.base_target = base_target
        self.debug = debug

    @staticmethod
    def pretty_print_request(request):
        """A utility method for formatting prepared requests"""

        # backslashes are disallowed in f-strings, hence \n below
        newline = "\n"
        formatted = f"""{newline}{request.method} {request.url}
{newline.join(f'{k}: {v}' for k,v in request.headers.items())}
{request.body if request.body else '**empty request body**'}{newline}"""
        print(formatted)

    @json_header
    def _request(self, method, endpoint, **kwargs):
        """A generic request method"""

        try:
            kwargs["params"]["token"] = self.api_token
        except (KeyError, TypeError) as exc:
            kwargs["params"] = {}
            kwargs["params"]["token"] = self.api_token

        target = "/".join((self.base_target, endpoint))
        payload = kwargs.get("payload", None)
        request = requests.Request(
            method,
            target,
            headers=kwargs["headers"],
            json=payload,
            params=kwargs["params"],
        )

        prepared_request = request.prepare()

        if self.debug:
            self.pretty_print_request(prepared_request)

        request_session = requests.Session()
        response = request_session.send(prepared_request)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if self.debug:
                print(exc)
        finally:
            request_session.close()
            results = response.json()
            print(results)
            return results

    def _get(self, endpoint, **kwargs):
        """A generic HTTP GET method"""
        return self._request("GET", endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        """A generic HTTP post method"""
        return self._request("POST", endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        """A generic HTTP PUT method"""
        return self._request("PUT", endpoint, **kwargs)
