import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import "./App.css";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error("Search failed");
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-3xl font-bold mb-8">Semantic Search</h1>
        <SearchBar onSearch={handleSearch} />

        {loading && (
          <div className="mt-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
          </div>
        )}

        {error && <div className="mt-8 text-red-500">{error}</div>}

        {!loading && !error && results.length === 0 && (
          <div className="mt-8 text-gray-400">
            Enter a search query to find research papers
          </div>
        )}

        {results.length > 0 && (
          <div className="mt-8 w-full max-w-4xl">
            {results.map((result, index) => (
              <div key={index} className="mb-4 p-4 bg-white rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900">
                  {result.title}
                </h3>
                <p className="text-sm text-gray-600 mt-1">{result.authors}</p>
                <p className="text-sm text-gray-500 mt-2">{result.abstract}</p>
                <a
                  href={result.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-block"
                >
                  Read paper
                </a>
              </div>
            ))}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
