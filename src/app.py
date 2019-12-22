import os
from flask import Flask, request 
from flask_restful import Resource, Api
from dotenv import load_dotenv
from flask_jwt import JWT, jwt_required
from security import  authenticate, identity
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env'))


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development-key')
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = [
            
        ]
class Item(Resource):
    @jwt_required()
    def get(self, name):
        try:
            item = next(filter(lambda x: x['name'] == name, items))
            return item
        except:
            return {'item':None}, 404
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items),None) != None:
            return {'message', f'An item with {name} already exists.'}, 400
        data = request.get_json(silent=True)
        if data is None:
            return {'item':None}, 404
        item = {'name':data['name'], 'price':data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name,items))
        return {'message': 'Item Deleted'}
    
    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':data['name'], 'price':data['price']}
            items.append(item)
        else:
            items.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

