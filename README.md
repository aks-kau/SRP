# Semantic Search for Research Papers

A web application that allows users to search through research papers using semantic search capabilities. The application consists of a Flask backend API and a React frontend.

## Project Structure

```
.
├── frontend/           # React frontend application
├── search_api/        # Flask backend API
└── data/             # Data storage directory
```

## Setup

### Backend (Flask API)

1. Install Python dependencies:

```bash
pip install flask flask-cors sentence-transformers huggingface-hub==0.16.4
```

2. Start the Flask server:

```bash
python search_api/app.py
```

The API will be available at `http://localhost:5000`.

### Frontend (React)

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`.

## Features

- Semantic search through research papers
- Real-time search results
- Paper details including title, authors, and abstract
- Links to full papers
- Modern, responsive UI

## Technologies Used

- Backend:

  - Flask (Python web framework)
  - sentence-transformers (for semantic search)
  - CORS support

- Frontend:
  - React
  - Tailwind CSS
  - Modern ES6+ JavaScript

## API Endpoints

### POST /search

Search for papers based on a query string.

Request body:

```json
{
  "query": "your search query"
}
```

Response:

```json
{
  "results": [
    {
      "title": "Paper Title",
      "authors": "Author Names",
      "abstract": "Paper Abstract",
      "year": 2023,
      "url": "https://example.com/paper"
    }
  ],
  "count": 1
}
```
