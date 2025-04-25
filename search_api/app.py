import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3
import numpy as np
from typing import List, Dict, Any
from transformers import AutoTokenizer, AutoModel
import torch
import traceback
import datetime
import pickle
from pathlib import Path

app = Flask(__name__)
# Update CORS configuration to allow all origins during development
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize model variables
model_name = "sentence-transformers/all-MiniLM-L6-v2"
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
print("Model loaded successfully")

# Cache for embeddings
EMBEDDINGS_CACHE_FILE = "paper_embeddings.pkl"
paper_embeddings = None
paper_data = None

# Get the absolute path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'papers.db')

def load_embeddings():
    global paper_embeddings, paper_data
    if Path(EMBEDDINGS_CACHE_FILE).exists():
        print("Loading cached embeddings...")
        with open(EMBEDDINGS_CACHE_FILE, 'rb') as f:
            cache_data = pickle.load(f)
            paper_embeddings = cache_data['embeddings']
            paper_data = cache_data['data']
        print(f"Loaded {len(paper_data)} cached embeddings")
    else:
        print("Generating embeddings cache...")
        print(f"Using database at: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT paper_id, title, abstract, year FROM papers")
        papers = cursor.fetchall()
        conn.close()

        paper_texts = [f"{p[1]} {p[2]}" for p in papers]
        paper_embeddings = get_embeddings(paper_texts)
        paper_data = papers

        # Save to cache
        with open(EMBEDDINGS_CACHE_FILE, 'wb') as f:
            pickle.dump({
                'embeddings': paper_embeddings,
                'data': paper_data
            }, f)
        print(f"Cached {len(paper_data)} embeddings")

# Load embeddings on startup
load_embeddings()

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "status": "ok",
        "message": "Semantic Search API is running",
        "endpoints": {
            "/test": "Test endpoint",
            "/search": "Search endpoint (POST)"
        }
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "ok",
        "message": "Server is running",
        "timestamp": datetime.datetime.now().isoformat()
    })

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Get embeddings for a list of texts using transformers."""
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=128)
    with torch.no_grad():
        model_output = model(**encoded_input)
        embeddings = model_output.last_hidden_state.mean(dim=1).numpy().tolist()
    return embeddings

def search_similar(text: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Search for similar texts using embeddings."""
    print(f"Searching for: {text}")
    query_embedding = get_embeddings([text])[0]
    
    try:
        if paper_embeddings is None or paper_data is None:
            load_embeddings()
        
        print("Calculating similarities...")
        # Normalize the query embedding
        query_norm = np.linalg.norm(query_embedding)
        query_embedding = query_embedding / query_norm if query_norm > 0 else query_embedding
        
        # Calculate normalized similarities
        similarities = []
        for pe in paper_embeddings:
            # Normalize paper embedding
            paper_norm = np.linalg.norm(pe)
            paper_embedding = pe / paper_norm if paper_norm > 0 else pe
            # Calculate cosine similarity (dot product of normalized vectors)
            similarity = np.dot(query_embedding, paper_embedding)
            # Ensure similarity is between 0 and 1
            similarity = max(0, min(1, similarity))
            similarities.append(similarity)
        
        sorted_indices = np.argsort(similarities)[::-1]
        results = []
        for idx in sorted_indices[:num_results]:
            paper = paper_data[idx]
            results.append({
                'paper_id': paper[0],
                'title': paper[1],
                'abstract': paper[2],
                'year': paper[3],
                'url': f"https://arxiv.org/abs/{paper[0]}",  # Construct arXiv URL
                'similarity': float(similarities[idx])
            })
        
        print(f"Returning {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Error in search_similar: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return []

@app.route('/search', methods=['POST', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        print("Received search request")
        data = request.get_json()
        print(f"Request data: {data}")
        query = data.get('query', '').lower()
        
        if not query:
            return jsonify({"error": "Query is required"}), 400

        results = search_similar(query)
        response = {
            'results': results,
            'count': len(results)
        }
        print(f"Sending response: {json.dumps(response, indent=2)}")
        return jsonify(response)
                
    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True) 