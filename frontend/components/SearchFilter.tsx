'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';

interface FilterOptions {
  searchQuery: string;
  selectedGenres: string[];
  minRating: number;
  yearRange: { min: number; max: number };
}

const GENRES = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Romance', 'Thriller', 'Adventure'];
const YEARS = Array.from({ length: 30 }, (_, i) => 2024 - i);

interface SearchFilterProps {
  onFilterChange: (filters: FilterOptions) => void;
}

export default function SearchFilter({ onFilterChange }: SearchFilterProps) {
  const [filters, setFilters] = useState<FilterOptions>({
    searchQuery: '',
    selectedGenres: [],
    minRating: 0,
    yearRange: { min: 1990, max: 2024 }
  });

  const handleSearchChange = (query: string) => {
    const newFilters = { ...filters, searchQuery: query };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const toggleGenre = (genre: string) => {
    const newGenres = filters.selectedGenres.includes(genre)
      ? filters.selectedGenres.filter(g => g !== genre)
      : [...filters.selectedGenres, genre];
    const newFilters = { ...filters, selectedGenres: newGenres };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleRatingChange = (rating: number) => {
    const newFilters = { ...filters, minRating: rating };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="sticky top-0 z-40 bg-gray-900 border-b border-gray-700 py-6 px-4"
    >
      <div className="container mx-auto">
        {/* Search Bar */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="🔍 Search movies..."
            value={filters.searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none transition"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Genres Filter */}
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-3">🎬 Genres</label>
            <div className="flex flex-wrap gap-2">
              {GENRES.map((genre) => (
                <motion.button
                  key={genre}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => toggleGenre(genre)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition ${
                    filters.selectedGenres.includes(genre)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  {genre}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Rating Filter */}
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-3">⭐ Min Rating</label>
            <input
              type="range"
              min="0"
              max="10"
              step="0.5"
              value={filters.minRating}
              onChange={(e) => handleRatingChange(parseFloat(e.target.value))}
feat: Implement Search & Filter component for movies            />
            <p className="text-xs text-gray-400 mt-2">{filters.minRating.toFixed(1)}+</p>
          </div>

          {/* Year Filter */}
          <div>
            <label className="block text-sm font-semibold text-gray-3- Text search bar for movie titles
- Genre multi-select filter (8 genres)
- Rating range slider (0-10)
- Year filter dropdown (30 years)
- Sticky header that stays visible while scrolling00 mb-3">📅 Year</label>
            <select
              defaultValue="2024"
              className="w-full px-3 py-2 bg-gray-800 text-white rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none"
            >
              {YEARS.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
