from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

# POST = used to receive data
# GET = used to send data back only


# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    # Iterate over get_stores
    # If the store name matches, return it
    # If none match, return an error
    for store in stores:
        if(store['name'] == name):
            return jsonify(store)
    return jsonify({'message': 'No stores found with that name'})

# GET /store
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if(store['name']==name):
            new_item={
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if(store['name'] == name):
            return jsonify(store['items'])
    return jsonify({'message': 'No items found for that store'})

app.run(port=5000)
