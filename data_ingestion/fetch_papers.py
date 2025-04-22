import os
import uuid
import sqlite3
import json
import requests
from tqdm import tqdm
import gzip
from pathlib import Path

# Database file path
DB_FILE = 'papers.db'
DATASET_DIR = 'data'
DATASET_URL = "https://production-media.paperswithcode.com/about/papers-with-abstracts.json.gz"

def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    Path(DATASET_DIR).mkdir(parents=True, exist_ok=True)

def download_dataset():
    """Download the Papers with Code dataset if not already present."""
    dataset_path = os.path.join(DATASET_DIR, "papers-with-abstracts.json.gz")
    
    if os.path.exists(dataset_path):
        print("Dataset already downloaded.")
        return dataset_path
        
    print("Downloading dataset...")
    response = requests.get(DATASET_URL, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    
    with open(dataset_path, 'wb') as f:
        with tqdm(total=total_size, unit='iB', unit_scale=True) as pbar:
            for data in response.iter_content(block_size):
                f.write(data)
                pbar.update(len(data))
    
    return dataset_path

def create_tables(conn):
    """Create necessary tables if they don't exist."""
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                paper_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                abstract TEXT NOT NULL,
                year INTEGER,
                url TEXT
            );
        """)

def load_papers_from_file(file_path, max_papers=1000):
    """Load papers from the downloaded dataset."""
    papers = []
    
    print("Loading papers from dataset...")
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
        
        for paper in tqdm(data[:max_papers], desc="Processing papers"):
            if paper.get('title') and paper.get('abstract'):
                papers.append({
                    'paper_id': str(uuid.uuid4()),
                    'title': paper['title'],
                    'abstract': paper['abstract'],
                    'year': paper.get('year'),
                    'url': paper.get('url', '')
                })
    
    return papers

def insert_papers(conn, papers):
    """Insert papers into the database."""
    with conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO papers (paper_id, title, abstract, year, url)
            VALUES (?, ?, ?, ?, ?)
            """,
            [(p['paper_id'], p['title'], p['abstract'], p.get('year'), p.get('url', '')) for p in papers]
        )

def main():
    try:
        # Create data directory
        ensure_data_dir()
        
        # Download dataset if needed
        dataset_path = download_dataset()
        
        # Connect to the database
        conn = sqlite3.connect(DB_FILE)
        
        # Create tables
        create_tables(conn)
        
        # Load and insert papers
        papers = load_papers_from_file(dataset_path, max_papers=1000)
        
        if papers:
            # Insert papers into the database
            insert_papers(conn, papers)
            print(f"Successfully inserted {len(papers)} papers into the database.")
            print(f"Database file created at: {os.path.abspath(DB_FILE)}")
        else:
            print("No papers were loaded from the dataset.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main() 