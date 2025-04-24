import os
from google.cloud import aiplatform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_vertex_ai():
    """Initialize Vertex AI with project and location."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set")
    
    aiplatform.init(project=project_id, location=location)
    return project_id, location

def get_embedding_model():
    """Get the Vertex AI text embedding model."""
    return aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@001")

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Get embeddings for a list of texts using Vertex AI."""
    model = get_embedding_model()
    embeddings = []
    
    # Process texts in batches to avoid rate limits
    batch_size = 5
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.get_embeddings(batch)
        embeddings.extend([e.values for e in batch_embeddings])
    
    return embeddings 