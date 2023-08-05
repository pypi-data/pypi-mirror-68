import os

from .resources.stories import Stories
from .resources.iterations import Iterations


class Client(object):
    """
    The Client for clubhouse.io. In keeping with the official API
    documentation, this client reads from the CLUBHOUSE_API_TOKEN
    environment variable. You may also explicitly provide one.

    USAGE:
    from clubhouse_client import Client

    # implicitly reading from $CLUBHOUSE_API_TOKEN
    clubhouse = Client()

    # explicitly providing an `api_token`
    clubhouse = Client(api_token='00000000-1111-2222-3333-444444444444')
    """
    def __init__(self, api_token=os.environ.get("CLUBHOUSE_API_TOKEN"), debug=False):
        self.stories = Stories(api_token, debug=debug)
