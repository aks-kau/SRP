import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3
import numpy as np
from typing import List, Dict, Any
import traceback
import datetime
from vertex_ai_config import initialize_vertex_ai, get_embeddings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from vertexai.language_models import TextGenerationModel

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Update CORS configuration to allow all origins during development
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Vertex AI
print("Initializing Vertex AI...")
try:
    project_id, location = initialize_vertex_ai()
    print(f"Vertex AI initialized with project {project_id} in {location}")
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")
    print("Falling back to local embeddings...")
    # You can add fallback to local embeddings here if needed

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Vertex AI text generation model
print("Initializing Vertex AI text generation model...")
generation_model = None

# Try loading the explicitly supported version
try:
    print("Trying to initialize text-bison@001 model...")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Use explicit project and location
    model_name = "text-bison@001"
    generation_model = TextGenerationModel.from_pretrained(model_name)
    print(f"Successfully initialized model: {model_name}")
except Exception as e:
    print(f"Failed to initialize model: {e}")
    generation_model = None

if not generation_model:
    print("Warning: Text generation model initialization failed. Paper generation feature will be disabled.")

# Database configuration
DB_FILE = 'papers.db'

def get_db_connection():
    return sqlite3.connect(DB_FILE)

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "status": "ok",
        "message": "Semantic Search API is running",
        "endpoints": {
            "/test": "Test endpoint",
            "/search": "Search endpoint (POST)",
            "/generate_paper": "Generate paper endpoint (POST)"
        }
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "ok",
        "message": "Server is running",
        "timestamp": datetime.datetime.now().isoformat()
    })

def search_similar(text: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Search for similar texts using embeddings."""
    print(f"Searching for: {text}")
    
    try:
        # Get embedding for the query
        query_embedding = model.encode(text)
        
        print("Connecting to database...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT paper_id, title, abstract, year, url FROM papers")
        papers = cursor.fetchall()
        print(f"Found {len(papers)} papers in database")
        
        print("Calculating similarities...")
        paper_texts = [f"{p[1]} {p[2]}" for p in papers]  # title + abstract
        paper_embeddings = model.encode(paper_texts)
        
        # Calculate similarities
        similarities = [np.dot(query_embedding, pe) for pe in paper_embeddings]
        
        # Get top results
        top_indices = np.argsort(similarities)[-num_results:][::-1]
        results = []
        for idx in top_indices:
            paper = papers[idx]
            results.append({
                'paper_id': paper[0],
                'title': paper[1],
                'abstract': paper[2],
                'year': paper[3],
                'url': paper[4],
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

        results = search_similar(query, num_results=5)
        
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

@app.route('/generate_paper', methods=['POST'])
def generate_paper():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        outline = data.get('outline', [])
        
        if not topic:
            return jsonify({"error": "Topic is required"}), 400
            
        if not generation_model:
            return jsonify({
                "error": "Paper generation is currently unavailable",
                "details": "The text generation service requires Google Cloud credentials. Please check your environment variables and ensure you have set up Google Cloud authentication properly.",
                "required_vars": [
                    "GOOGLE_CLOUD_PROJECT",
                    "GOOGLE_APPLICATION_CREDENTIALS",
                    "QUOTA_PROJECT_ID"
                ]
            }), 503
            
        # Generate paper sections based on outline
        sections = []
        for section in outline:
            prompt = f"""Write a detailed research paper section about {topic} focusing on {section}.
            The section should be well-researched, academic in tone, and include relevant citations.
            Format the response in markdown."""
            
            # Use the model with explicit parameters and proper error handling
            try:
                response = generation_model.predict(
                    prompt,
                    temperature=0.2,
                    max_output_tokens=1024,
                    top_p=0.8,
                    top_k=40
                )
                
                sections.append({
                    "title": section,
                    "content": response.text
                })
            except Exception as predict_error:
                print(f"Error during prediction for section '{section}': {predict_error}")
                sections.append({
                    "title": section,
                    "content": f"**Error generating content for this section:** {str(predict_error)}"
                })
            
        return jsonify({
            "topic": topic,
            "sections": sections
        })
        
    except Exception as e:
        print(f"Error in generate_paper endpoint: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({
            "error": "Failed to generate paper",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True) 