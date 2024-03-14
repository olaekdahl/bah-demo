from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import boto3
import json

app = Flask(__name__)
CORS(app)

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    # Decrypts secret using the associated KMS CMK
    # Depending on whether the secret is a string or binary, one of these fields will be populated
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(decoded_binary_secret)

# Your secret name and region
secret_name = "app"
region_name = "us-east-1"

# Fetch the secret
secret = get_secret(secret_name, region_name)

# Use the secret to connect to MongoDB
username = secret['username']
password = secret['password']
host = secret['host']
database = secret['database']

# Connect to your MongoDB or DocumentDB
connection_string = f"mongodb+srv://{username}:{password}@{host}/{database}"
client = MongoClient(connection_string)
db = client.demo
boardgames = db.boardgames

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "success" }), 200

@app.route('/boardgames', methods=['GET'])
def get_boardgames():
    # Retrieve the first ten records
    try:
        games = list(boardgames.find().limit(10))
        for game in games:
            game['_id'] = str(game['_id'])
        return jsonify(games)
    except Exception as e:
        print(e)
        return jsonify({"error": json.dumps(e, default=str)})

@app.route('/boardgames/<id>', methods=['GET'])
def get_boardgame(id):
    # Retrieve a single document by ID
    try:
        game = boardgames.find_one({'_id': ObjectId(id)})
        if game:
            game['_id'] = str(game['_id'])
            return jsonify(game)
        else:
            return jsonify({"error": "Boardgame not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

# curl -X POST http://localhost:5000/search -H "Content-Type: application/json"  -d '{"name": "Renature"}'

@app.route('/search', methods=['POST'])
def search_boardgames():
    # Find matches based on board game name. Allows wildcards.
    data = request.get_json()
    query_name = data.get('name')
    games = list(boardgames.find({"name": {"$regex": query_name, "$options": "i"}}))
    for game in games:
        game['_id'] = str(game['_id'])
    return jsonify(games)

if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)