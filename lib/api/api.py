from flask import Flask
from flask_restful import Api, Resource, request

from api_ref import *

app = Flask(__name__)
api = Api(app)


# manage Accounts
class Accounts(Resource):

    def post(self):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        # METHODS
        # -
        # -
        # -
        with accounts() as a:
            func = getattr(a, method)
            print(func)
            return func(body)


# submit Transactions
class Transactions(Resource):
    def post(self):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        # METHODS
        # -
        # -
        # -
        with transactions() as t:
            func = getattr(a, method)
            print(func)
            return func(body)