import os

from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS

from api_ref import *

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/Account/*": {"origins": "*"}})
cors = CORS(app, resources={r"/Transactions/*": {"origins": "*"}})


# manage Accounts
class Accounts(Resource):
    def post(self, username):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        body['origin'] = request.remote_addr
        # METHODS
        # -
        # -
        # -
        with accounts() as a:
            func = getattr(a, method)
            print('calling method ', end='\t')
            print(func)
            return func(username, body)


# submit Transactions
class Transactions(Resource):
    def post(self, username):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        body['origin'] = request.remote_addr
        # METHODS
        # -
        # -
        # -
        with transactions() as t:
            func = getattr(t, method)
            print('calling method ', end='\t')
            print(func)
            return func(username, body)


# add all to API
api.add_resource(Accounts, '/Account/<username>')
api.add_resource(Transactions, '/Transactions/<username>')

if __name__ == '__main__':
    context = (os.environ.get('CERTFILE'), os.environ.get('CERT_KEYFILE'))
    print(context)
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
