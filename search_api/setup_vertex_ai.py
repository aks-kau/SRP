import os
from google.cloud import aiplatform
from google.cloud.aiplatform import MatchingEngineIndex, MatchingEngineIndexEndpoint
import numpy as np
from typing import List, Dict, Any

def setup_vertex_ai():
    # Initialize Vertex AI
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )

    # Initialize the text embedding model
    model = aiplatform.Model(
        model_name="textembedding-gecko@001",
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    )

    # Create index
    index = MatchingEngineIndex.create(
        display_name="research-papers-index",
        description="Index for research papers semantic search",
        contents_delta_uri=os.getenv("VERTEX_AI_INDEX_BUCKET"),
        dimensions=768,  # Gecko embedding dimension
        index_update_method="streaming"
    )

    # Create endpoint
    endpoint = MatchingEngineIndexEndpoint.create(
        display_name="research-papers-endpoint",
        description="Endpoint for research papers semantic search",
        network=os.getenv("VERTEX_AI_NETWORK")
    )

    # Deploy index to endpoint
    endpoint.deploy_index(
        index=index,
        deployed_index_id="research_papers_index"
    )

    print("Vertex AI setup completed successfully!")
    print(f"Index ID: {index.name}")
    print(f"Endpoint ID: {endpoint.name}")
    print(f"Deployed Index ID: research_papers_index")

if __name__ == "__main__":
    setup_vertex_ai() 