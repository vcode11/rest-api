from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__)

stores = [
            {
                'name':'My Wonderful store',
                'items':[
                        {
                            'name':'My item',
                            'price':15.99,
                        },
                    ]
            },
        
        ]

@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name: }
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json(force=True)
    new_store  = {
        'name':request_data['name'],
        'items': [],
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    #if the store name matches return it
    #if no mathces return an error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message':'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store_dict = store
            store['items'].append(
                        {
                            'name':request_data['name'], 
                            'price':request_data['price']
                        }
                    )
            stores.remove(store_dict)
            stores.append(store)
            return jsonify(store)
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message': 'store not found'})
        

if __name__ == '__main__':
    app.run(debug=True)
