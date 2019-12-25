from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Name of Item is a required.')
    parser.add_argument('price', type=float, required=True, help='Price of item is a required.')    
  
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item':{'name':row[1], 'price':row[2]}}
        return None
    @classmethod
    def create_item(cls, name, price):
        query = 'INSERT INTO items VALUES (NULL,?, ?)'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()            
        values = (name, price)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
    
    @classmethod
    def update_item(cls, name, price):
        query = 'UPDATE items SET price = ? WHERE name = ?'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()            
        values = (name, price)
        cursor.execute(query,values)
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        query = 'DELETE FROM items WHERE name=?'
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()


    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message':'Item not found.'}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        if self.find_by_name(data['name']):
            return {'message':'Item with same name already exists.'}, 400
        self.create_item(data['name'], data['price'])
        return {'item':{'name':data['name'], 'price':data['price']}}, 201
        


    def delete(self, name):
        data = Item.parser.parse_args()
        if self.find_by_name(data['name']):
            self.delete_item(data['name'])
            return {'message': 'Item Deleted'}
        return {'message':'Item doesn\'t exist.'}, 400
    
    def put(self, name):
        data = Item.parser.parse_args()
        if self.find_by_name(data['name']):
            self.update_item(data['name'],data['price'])
            return {'item':{'name':data['name'],'price':data['price']}}, 200
        self.create_item(data['name'], data['price'])
        return {'item':{data}}, 201


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        data = []
        for row in cursor.execute(query):
            data.append({'name':row[1],'price':row[2]})
        connection.close()
        return {'items':data}
