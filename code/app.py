from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'IAMTHEKIDYOUKNOWWHATIMEAN'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

Items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name']==name, Items), None)
        return {'item': item}, 200 if item == None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, Items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        Items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': Items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
