import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import KeyTerms from "./components/KeyTerms";
import "./App.css";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTimeout, setSearchTimeout] = useState(null);

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    
    if (searchTimeout) {
      clearTimeout(searchTimeout);
    }

    const timeout = setTimeout(() => {
      setError("Search is taking longer than expected. Please try a different search term or try again later.");
      setLoading(false);
    }, 10000);

    setSearchTimeout(timeout);

    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ query }),
        mode: "cors",
      });

      clearTimeout(timeout);
      setSearchTimeout(null);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();

      if (!data.results || !Array.isArray(data.results)) {
        throw new Error("Invalid response format from server");
      }

      setResults(data.results);
    } catch (err) {
      console.error("Search error:", err);
      setError(
        err.message ||
          "Failed to connect to the search server. Please make sure the server is running."
      );
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Research Paper Search</h1>
        <SearchBar onSearch={handleSearch} />
      </header>

      <main className="search-results">
        {loading && (
          <div className="loading-container">
            {/* Will be uncommented when assets are ready
            <img
              src="./assets/loading-scholar.gif"
              alt="Loading..."
              className="loading-animation"
            />
            */}
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <p className="ml-4 text-gray-500">Searching...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p className="font-bold">Error:</p>
            <p>{error}</p>
            <p className="mt-2 text-sm">
              Please make sure the backend server is running at
              http://localhost:5000
            </p>
          </div>
        )}

        {!loading && !error && results.length === 0 && (
          <div className="text-gray-500">
            <p>Enter a search query to find research papers</p>
            <KeyTerms />
          </div>
        )}

        {results.length > 0 && (
          <div>
            <p className="text-gray-500 mb-4">
              Found {results.length} results
            </p>
            {results.map((result, index) => (
              <div key={index} className="paper-card">
                <h3 className="paper-title">{result.title}</h3>
                <div className="paper-meta">
                  <span>Year: {result.year}</span>
                </div>
                <p className="paper-abstract">{result.abstract}</p>
                <div className="flex justify-between items-center">
                  <span className="similarity-badge">
                    Similarity: {(result.similarity * 100).toFixed(1)}%
                  </span>
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="paper-link"
                  >
                    Read paper
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
