import React from "react";

function YearFilter({ yearRange, onYearRangeChange }) {
  const currentYear = new Date().getFullYear();

  const handleMinYearChange = (e) => {
    onYearRangeChange({
      ...yearRange,
      min: Math.min(parseInt(e.target.value), yearRange.max),
    });
  };

  const handleMaxYearChange = (e) => {
    onYearRangeChange({
      ...yearRange,
      max: Math.max(parseInt(e.target.value), yearRange.min),
    });
  };

  return (
    <div className="mt-4 flex items-center space-x-4">
      <div className="flex-1">
        <label
          htmlFor="min-year"
          className="block text-sm font-medium text-gray-700"
        >
          From Year
        </label>
        <input
          type="number"
          id="min-year"
          value={yearRange.min}
          onChange={handleMinYearChange}
          min="1900"
          max={yearRange.max}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        />
      </div>
      <div className="flex-1">
        <label
          htmlFor="max-year"
          className="block text-sm font-medium text-gray-700"
        >
          To Year
        </label>
        <input
          type="number"
          id="max-year"
          value={yearRange.max}
          onChange={handleMaxYearChange}
          min={yearRange.min}
          max={currentYear}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
        />
      </div>
    </div>
  );
}

export default YearFilter;
