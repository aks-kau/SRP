import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/search', methods=['POST', 'OPTIONS'])
def search():
    # Handle preflight request
    if request.method == 'OPTIONS':
        return '', 200

    try:
        print("Received search request")  # Debug log
        data = request.get_json()
        print(f"Request data: {data}")  # Debug log
        query = data.get('query', '').lower()
        
        if not query:
            print("Empty query received")  # Debug log
            return jsonify({"error": "Query is required"}), 400

        # Sample data (we'll use this instead of a database)
        papers = [
            {
                "title": "Deep Learning in Neural Networks",
                "authors": "John Smith, Jane Doe",
                "abstract": "This paper explores the fundamentals of deep learning in neural networks.",
                "year": 2023,
                "url": "https://example.com/paper1"
            },
            {
                "title": "Machine Learning Applications",
                "authors": "Alice Johnson",
                "abstract": "A comprehensive review of machine learning applications in various fields.",
                "year": 2022,
                "url": "https://example.com/paper2"
            },
            {
                "title": "Artificial Intelligence Ethics",
                "authors": "Bob Wilson, Carol Brown",
                "abstract": "Discussion of ethical considerations in AI development and deployment.",
                "year": 2023,
                "url": "https://example.com/paper3"
            }
        ]
        
        # Simple text search
        results = []
        for paper in papers:
            text = (paper['title'] + ' ' + paper['abstract']).lower()
            if query in text:
                results.append({
                    'title': paper['title'],
                    'authors': paper['authors'],
                    'abstract': paper['abstract'],
                    'year': paper['year'],
                    'url': paper['url']
                })
        
        print(f"Found {len(results)} results for query: {query}")  # Debug log
        response = jsonify({
            'results': results,
            'count': len(results)
        })
        return response
                
    except Exception as e:
        print(f"Error processing request: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")  # Debug log
    app.run(host='0.0.0.0', port=5000, debug=True) 