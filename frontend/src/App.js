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
      console.log("Sending search request for:", query);
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ query }),
        mode: "cors",
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.error || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();
      console.log("Response data:", data);

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
        <h1 className="text-3xl font-bold mb-8">Semantic Search</h1>
        <SearchBar onSearch={handleSearch} />

        {loading && (
          <div className="mt-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white"></div>
            <p className="mt-2 text-gray-400">Searching...</p>
          </div>
        )}

        {error && (
          <div className="mt-8 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            <p className="font-bold">Error:</p>
            <p>{error}</p>
            <p className="mt-2 text-sm">
              Please make sure the backend server is running at
              http://localhost:5000
            </p>
          </div>
        )}

        {!loading && !error && results.length === 0 && (
          <div className="mt-8 text-gray-400">
            Enter a search query to find research papers
          </div>
        )}

        {results.length > 0 && (
          <div className="mt-8 w-full max-w-4xl">
            <p className="text-gray-400 mb-4">Found {results.length} results</p>
            {results.map((result, index) => (
              <div key={index} className="mb-4 p-4 bg-white rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900">
                  {result.title}
                </h3>
                <p className="text-sm text-gray-600 mt-1">
                  Year: {result.year}
                </p>
                <p className="text-sm text-gray-500 mt-2">{result.abstract}</p>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-sm text-gray-500">
                    Similarity: {(result.similarity * 100).toFixed(1)}%
                  </span>
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Read paper
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
