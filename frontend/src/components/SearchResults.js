import React from "react";

function SearchResults({ results }) {
  if (results.length === 0) {
    return (
      <div className="mt-8 text-center text-gray-500">
        No results found. Try a different search query.
      </div>
    );
  }

  return (
    <div className="mt-8 space-y-6">
      {results.map((result) => (
        <div
          key={result.paper_id}
          className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {result.title}
          </h3>
          <div className="flex items-center text-sm text-gray-500 mb-3">
            <span>Published: {result.year}</span>
            <span className="mx-2">•</span>
            <span>Similarity: {(1 - result.similarity).toFixed(2)}</span>
          </div>
          <p className="text-gray-600">{result.snippet}</p>
        </div>
      ))}
    </div>
  );
}

export default SearchResults;
