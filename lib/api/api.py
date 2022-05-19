from flask import Flask
from flask_restful import Api, Resource, request

from api_ref import *

app = Flask(__name__)
api = Api(app)


# manage Accounts
class Accounts(Resource):

    def post(self, username):
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
            return func(username, body)


# submit Transactions
class Transactions(Resource):
    def post(self, username):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        # METHODS
        # -
        # -
        # -
        with transactions() as t:
            func = getattr(t, method)
            print(func)
            return func(username, body)


# add all to API
api.add_resource(Accounts, '/Accounts/<username>')
api.add_resource(Accounts, '/Transactions/<username>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
