# pip install Flask pymongo

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi

app = Flask(__name__)

# Connect to DocumentDB
client = MongoClient('mongodb+srv://<username>:<password>@docdb-2024-03-08-19-04-08.cuvrpg7gj6rj.us-east-1.docdb.amazonaws.com:27017/demodb?ssl=true&ssl_ca_certs=certifi.where()')
db = client.demodb
boardgames = db.boardgames

@app.route('/boardgames', methods=['GET'])
def get_boardgames():
    # Retrieve the first ten records
    games = list(boardgames.find().limit(10))
    for game in games:
        game['_id'] = str(game['_id'])
    return jsonify(games)

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
    app.run(debug=True)
