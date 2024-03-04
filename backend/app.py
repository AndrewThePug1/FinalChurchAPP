from flask import Flask, jsonify
import chromadb
import os
import hashlib
import json  # Added import for json

app = Flask(__name__)

PERSISTENCE_PATH = "chroma_data"
chroma_client = chromadb.PersistentClient(path=PERSISTENCE_PATH)

# Ensure collection exists
try:
    collection = chroma_client.get_collection(name="song_collection")
except Exception as e:
    print(f"Collection not found, creating a new one... Error: {e}")
    collection = chroma_client.create_collection(name="song_collection")

def generate_hash(metadata, lyrics):
    hash_input = json.dumps(metadata, sort_keys=True) + lyrics
    return hashlib.sha256(hash_input.encode()).hexdigest()

if __name__ == '__main__':
    # Testing retrieval by hash on startup
    test_hash = '677daa1089464d4474876130c793da18cd30c8e3f649074a876cd691ff13a05d'

    # Adjusted retrieval logic based on ChromaDB capabilities
    try:
        # Assuming the hash is stored in metadata, attempting to query based on metadata
        # Note: Adjust the query as per the actual structure and capabilities of ChromaDB
        query_result = collection.query(
            query_texts=[""],  # Provide an empty query text to satisfy the requirement
            n_results=1,  # Assuming you only want one result
            where={"hash": test_hash}  # Using the where filter to search by hash
        )
        if query_result and query_result['documents']:
            print(f"Found song with hash {test_hash}")
        else:
            print(f"No song found with hash {test_hash}")
    except Exception as e:
        print(f"Error retrieving song by hash at startup: {e}")

    app.run(debug=True)
