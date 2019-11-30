import os
from flask import Flask, request 
from flask_restful import Resource, Api
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env'))
app.secret_key = os.environ.get('SECRET_KEY', 'development-key')
print(app.secret_key)
api = Api(app)

items = [
            
        ]
class Item(Resource):
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
        if data in None:
            return {'item':None}, 404
        item = {'name':data['name'], 'price':data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items':items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

