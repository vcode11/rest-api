from flask import Flask, request 
from flask_restful import Resource, Api

app = Flask(__name__)
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

