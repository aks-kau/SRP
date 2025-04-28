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

app = Flask(__name__)
# Update CORS configuration to allow all origins during development
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize model variables
model_name = "sentence-transformers/all-MiniLM-L6-v2"
print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
print("Model loaded successfully")

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
        print("Connecting to database...")
        conn = sqlite3.connect('papers.db')
        cursor = conn.cursor()
        cursor.execute("SELECT paper_id, title, abstract, year FROM papers")
        papers = cursor.fetchall()
        print(f"Found {len(papers)} papers in database")
        
        print("Calculating similarities...")
        paper_texts = [f"{p[1]} {p[2]}" for p in papers]  # title + abstract
        paper_embeddings = get_embeddings(paper_texts)
        similarities = [np.dot(query_embedding, pe) for pe in paper_embeddings]
        
        sorted_indices = np.argsort(similarities)[::-1]
        results = []
        for idx in sorted_indices[:num_results]:
            results.append({
                'paper_id': papers[idx][0],
                'title': papers[idx][1],
                'abstract': papers[idx][2],
                'year': papers[idx][3],
                'url': f"https://arxiv.org/abs/{papers[idx][0]}",  # Construct arXiv URL
                'similarity': float(similarities[idx])
            })
        
        print(f"Returning {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Error in search_similar: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return []
    finally:
        if 'conn' in locals():
            conn.close()

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