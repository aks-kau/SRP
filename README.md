# Research Paper Semantic Search Engine

A sophisticated web application that enables users to search through academic research papers using advanced semantic search capabilities. The application leverages modern AI technologies to understand and match search queries with relevant research papers, providing a more intuitive and effective search experience than traditional keyword-based search.

## Project Description

This application transforms how researchers and academics discover relevant papers by implementing semantic search technology. Instead of relying on exact keyword matches, it understands the meaning and context of search queries to find the most relevant papers, even when the exact terms aren't present in the text.

### Key Features

- **Semantic Search**: Advanced natural language understanding to find relevant papers based on meaning, not just keywords
- **Real-time Results**: Instant feedback as you type your search query
- **Paper Details**: Comprehensive view of each paper including:
  - Title and publication year
  - Abstract with key information
  - Similarity score showing relevance
  - Direct link to the full paper
- **Smart Suggestions**: Key terms and popular search topics to help guide research
- **Responsive Design**: Optimized for all devices from desktop to mobile
- **Academic Theme**: Professional, scholarly interface designed for researchers
- **Performance Optimized**: Cached embeddings and efficient search algorithms
- **Error Handling**: Graceful handling of timeouts and connection issues

## Technology Stack

### Frontend
- **Framework**: React.js
- **Styling**: 
  - Tailwind CSS
  - Custom CSS with CSS variables
  - Google Fonts (Merriweather, Open Sans)
- **State Management**: React Hooks
- **UI Components**: Custom-built components
- **Animation**: CSS animations and transitions
- **Responsive Design**: Mobile-first approach

### Backend
- **Framework**: Flask (Python)
- **AI/ML**:
  - Hugging Face Transformers
  - Sentence Transformers (all-MiniLM-L6-v2 model)
  - PyTorch for model inference
- **API**:
  - RESTful endpoints
  - CORS support
  - JSON request/response handling
- **Performance**:
  - Embedding caching
  - Efficient similarity calculations
  - Request timeout handling

### Database
- **Type**: SQLite
- **Schema**: 
  - Papers table with metadata
  - Efficient indexing for quick lookups
- **Storage**: Local file-based storage

### Development Tools
- **Version Control**: Git
- **Package Management**:
  - npm (Node.js)
  - pip (Python)
- **Development Environment**:
  - VS Code recommended
  - Python virtual environment
  - Node.js environment

### Google Technologies Integration
- **Google Fonts**: 
  - Merriweather for headings
  - Open Sans for body text
- **Google Cloud Integration** (Future Enhancements):
  - Cloud Storage for paper database
  - Cloud Functions for scalable search
  - BigQuery for analytics
  - Cloud Vision API for paper image processing
  - Cloud Natural Language API for enhanced semantic understanding

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm 6+
- Git

### Installation
1. Clone the repository
2. Set up the backend (see Backend Setup)
3. Set up the frontend (see Frontend Setup)

### Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python search_api/app.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## Future Enhancements
1. User authentication and personalized search
2. Paper recommendations based on search history
3. Integration with academic databases
4. Citation network visualization
5. Advanced filtering and sorting options
6. Export search results functionality
7. Collaborative research features

## Contributing
Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Project Structure

```
.
├── frontend/           # React frontend application
│   ├── src/
│   │   ├── assets/    # Visual assets and images
│   │   │   ├── header-bg.jpg    # Header background (1920x400px)
│   │   │   ├── paper-icon.png   # Paper icon (64x64px)
│   │   │   ├── loading-scholar.gif  # Loading animation (200x200px)
│   │   │   └── README.md        # Assets documentation
│   │   ├── components/  # React components
│   │   ├── App.js      # Main application component
│   │   └── App.css     # Application styles
├── search_api/        # Flask backend API
└── data/             # Data storage directory
```

## Features

- Semantic search through research papers
- Real-time search results
- Paper details including title, authors, and abstract
- Links to full papers
- Modern, responsive UI with academic theme
- Key terms suggestions for search
- Visual feedback during search operations

## Technologies Used

- Backend:
  - Flask (Python web framework)
  - sentence-transformers (for semantic search)
  - CORS support

- Frontend:
  - React
  - Tailwind CSS
  - Modern ES6+ JavaScript
  - Google Fonts (Merriweather, Open Sans)
  - Responsive design

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
      "url": "https://example.com/paper",
      "similarity": 0.85
    }
  ],
  "count": 1
}
```

## Assets

The application uses several visual assets located in `frontend/src/assets/`:

1. `header-bg.jpg`: A scholarly background image for the header
2. `paper-icon.png`: A document icon for search results
3. `loading-scholar.gif`: An academic-themed loading animation

See `frontend/src/assets/README.md` for detailed specifications and guidelines for these assets.
