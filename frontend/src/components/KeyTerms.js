import React from 'react';

const KeyTerms = () => {
  const keyTerms = [
    "machine learning",
    "deep learning",
    "neural networks",
    "natural language processing",
    "computer vision",
    "reinforcement learning",
    "transfer learning",
    "attention mechanisms",
    "transformers",
    "generative models"
  ];

  return (
    <div className="mt-8 w-full max-w-4xl">
      <h2 className="text-xl font-semibold text-gray-200 mb-4">Popular Search Terms</h2>
      <div className="flex flex-wrap gap-2">
        {keyTerms.map((term, index) => (
          <span
            key={index}
            className="px-3 py-1 bg-gray-700 text-gray-200 rounded-full text-sm hover:bg-gray-600 cursor-pointer transition-colors"
            onClick={() => window.location.href = `#search=${encodeURIComponent(term)}`}
          >
            {term}
          </span>
        ))}
      </div>
    </div>
  );
};

export default KeyTerms; 