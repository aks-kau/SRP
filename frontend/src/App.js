import React, { useState, useEffect } from 'react';
import './App.css';
// import KeyTerms from './components/KeyTerms';
// import loadingAnimation from './assets/loading.gif';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [keyTerms, setKeyTerms] = useState([]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);
    setKeyTerms([]);

    try {
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Search request failed');
      }

      const data = await response.json();
      setResults(data.results);
      if (data.key_terms) {
        setKeyTerms(data.key_terms);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Semantic Paper Search</h1>
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your search query..."
            className="search-input"
          />
          <button type="submit" className="search-button" disabled={loading}>
            Search
          </button>
        </form>
      </header>

      <main className="search-results">
        {error && <div className="error-message">{error}</div>}
        
        {loading && (
          <div className="loading-container">
            {/* <img src={loadingAnimation} alt="Loading..." className="loading-animation" /> */}
            <p>Searching...</p>
          </div>
        )}

        {results.length > 0 && (
          <>
            {/* {keyTerms.length > 0 && <KeyTerms terms={keyTerms} />} */}
            
            {results.map((result, index) => (
              <div key={index} className="paper-card">
                <h2 className="paper-title">{result.title}</h2>
                <div className="paper-meta">
                  <span>Year: {result.year}</span>
                  <span className="similarity-badge">
                    Similarity: {(result.similarity * 100).toFixed(1)}%
                  </span>
                </div>
                <p className="paper-abstract">{result.abstract}</p>
                <a href={result.url} className="paper-link" target="_blank" rel="noopener noreferrer">
                  Read Paper
                </a>
              </div>
            ))}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
