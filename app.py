# pip install Flask pymongo

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import boto3
import json

app = Flask(__name__)

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

def download_s3_file(bucket, key, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, download_path)

# Your secret name and region
secret_name = "app"
region_name = "us-east-1"

# Fetch the secret
secret = get_secret(secret_name, region_name)

# Use the secret to connect to MongoDB
username = secret['username']
password = secret['password']
host = "docdb-2024-03-08-19-04-08.cuvrpg7gj6rj.us-east-1.docdb.amazonaws.com/demodb:27017" #secret['host']

s3_bucket = secret['s3_bucket']
s3_key = secret['s3_key']
# Save the SSL certificate to a file if needed
ssl_cert_file_path = '/home/ec2-user/app/ssl_cert.pem'
download_s3_file(s3_bucket, s3_key, ssl_cert_file_path)

# Connect to your MongoDB or DocumentDB
connection_string = f"mongodb://{username}:{password}@{host}?tls=true&tlsCAFile={ssl_cert_file_path}&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
client = MongoClient(connection_string) #, tlsCAFile=certifi.where())
db = client.demodb
boardgames = db.boardgames

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
        return jsonify({"error":e})

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

# curl -X POST http://localhost:5000/search \
# -H "Content-Type: application/json" \
# -d '{"name": "your_search_term"}'

@app.route('/search', methods=['POST'])
def search_boardgames():
    # Find matches based on board game name. Allows wildcards.
    data = request.get_json()
    query_name = data.get('name', '')
    games = list(boardgames.find({"name": {"$regex": query_name, "$options": "i"}}))
    for game in games:
        game['_id'] = str(game['_id'])
    return jsonify(games)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')