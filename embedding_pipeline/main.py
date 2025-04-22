import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from google.cloud import aiplatform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'dbname': os.getenv('DB_NAME')
}

# Initialize Vertex AI
aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))

def get_papers_batch(conn, batch_size=100):
    """Fetch a batch of papers that don't have embeddings yet."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT p.paper_id, p.abstract
            FROM papers p
            LEFT JOIN paper_embeddings pe ON p.paper_id = pe.paper_id
            WHERE pe.paper_id IS NULL
            LIMIT %s
        """, (batch_size,))
        return cur.fetchall()

def generate_embeddings(texts):
    """Generate embeddings using Vertex AI textembedding-gecko model."""
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings(texts)
    return [e.values for e in embeddings]

def update_embeddings(conn, paper_embeddings):
    """Update the embeddings in the database."""
    with conn.cursor() as cur:
        for paper_id, embedding in paper_embeddings:
            cur.execute("""
                INSERT INTO paper_embeddings (paper_id, embedding)
                VALUES (%s, %s)
                ON CONFLICT (paper_id) DO UPDATE
                SET embedding = EXCLUDED.embedding
            """, (paper_id, embedding))
        conn.commit()

def process_batch(request):
    """Cloud Function entry point."""
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_PARAMS)
        
        # Get a batch of papers
        papers = get_papers_batch(conn)
        
        if not papers:
            return json.dumps({"message": "No papers to process"})
        
        # Generate embeddings
        texts = [p['abstract'] for p in papers]
        embeddings = generate_embeddings(texts)
        
        # Update database
        paper_embeddings = [(p['paper_id'], e) for p, e in zip(papers, embeddings)]
        update_embeddings(conn, paper_embeddings)
        
        return json.dumps({
            "message": f"Processed {len(papers)} papers",
            "status": "success"
        })
        
    except Exception as e:
        return json.dumps({
            "message": str(e),
            "status": "error"
        })
    finally:
        if 'conn' in locals():
            conn.close() 