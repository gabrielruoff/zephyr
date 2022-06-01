from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS

from api_ref import *

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/pos/*": {"origins": "*"}})
cors = CORS(app, resources={r"/data": {"origins": "*"}})


class POS(Resource):
    def post(self, uid):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        body['origin'] = request.remote_addr
        # METHODS
        # -
        # -
        # -
        with pos() as a:
            func = getattr(a, method)
            print('calling method ', end='\t')
            print(func)
            return func(uid, body)


# manage Accounts
class Data(Resource):
    def post(self):
        content = request.get_json()
        # get request method and body
        method, body = content['method'], content['body']
        body['origin'] = request.remote_addr
        # METHODS
        # -
        # -
        # -
        with data() as d:
            func = getattr(d, method)
            print('calling method ', end='\t')
            print(func)
            return func(body)


# add all to API
api.add_resource(POS, '/pos/<uid>')
api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
