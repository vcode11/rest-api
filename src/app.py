import os
from flask import Flask 
from flask_restful import Resource, Api
from dotenv import load_dotenv
from flask_jwt import JWT
from security import  authenticate, identity
from user import UserRegister
from items import Item, ItemList

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.env'))


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development-key')
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

