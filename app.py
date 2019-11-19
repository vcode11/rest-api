from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [
            
        ]
class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item':None}, 404
    
    def post(self, name):
        item = {'name':name, 'price': 12.00}
        items.append(item)
        return item, 201

api.add_resource(Item, '/item/<string:name>')


if __name__ == '__main__':
    app.run(debug=True, port=5000)

