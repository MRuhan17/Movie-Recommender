'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import MovieCard from './MovieCard';

interface Movie {
  id: number;
  title: string;
  posterUrl: string;
  rating: number;
  mlConfidence: number;
  releaseYear: number;
  genres: string[];
}

export default function HomeDashboard() {
  const [trendingMovies, setTrendingMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulated API call - replace with actual backend
    const fetchTrendingMovies = async () => {
      try {
        // const response = await fetch('/api/movies/trending');
        // const data = await response.json();
        // setTrendingMovies(data);
        
        // Mock data for demonstration
        const mockMovies: Movie[] = [
          {
            id: 1,
            title: 'Inception',
            posterUrl: 'https://image.tmdb.org/t/p/w500/9gk7adHYeDMPS6ivNEmZwtI91a0.jpg',
            rating: 8.8,
            mlConfidence: 0.92,
            releaseYear: 2010,
            genres: ['Sci-Fi', 'Action', 'Thriller']
          },
          {
            id: 2,
            title: 'The Dark Knight',
            posterUrl: 'https://image.tmdb.org/t/p/w500/qJ2tW6WMCd7CKF81ChzWQKc67Il.jpg',
            rating: 9.0,
            mlConfidence: 0.89,
            releaseYear: 2008,
            genres: ['Action', 'Crime', 'Drama']
          },
          {
            id: 3,
            title: 'Interstellar',
            posterUrl: 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCu244MyJgZy.jpg',
            rating: 8.6,
            mlConfidence: 0.95,
            releaseYear: 2014,
            genres: ['Sci-Fi', 'Drama', 'Adventure']
          },
          {
            id: 4,
            title: 'Pulp Fiction',
            posterUrl: 'https://image.tmdb.org/t/p/w500/3W7v0eIac2zGmBRgHd2LYNQDMoD.jpg',
            rating: 8.9,
            mlConfidence: 0.87,
            releaseYear: 1994,
            genres: ['Crime', 'Drama']
          },
          {
            id: 5,
            title: 'Fight Club',
            posterUrl: 'https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PchJ.jpg',
            rating: 8.8,
            mlConfidence: 0.91,
            releaseYear: 1999,
            genres: ['Drama', 'Thriller']
          },
          {
            id: 6,
            title: 'The Matrix',
            posterUrl: 'https://image.tmdb.org/t/p/w500/f89U3ADr1oRoRCRn/NxjRHtRnr63v0eeEEQIaXEJWgIJ.jpg',
            rating: 8.7,
            mlConfidence: 0.93,
            releaseYear: 1999,
            genres: ['Sci-Fi', 'Action']
          }
        ];
        
        setTrendingMovies(mockMovies);
      } catch (error) {
        console.error('Failed to fetch movies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrendingMovies();
  }, []);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 pb-20">
      {/* Hero Section */}
      <div className="relative h-96 bg-gradient-to-r from-blue-600 to-purple-700 overflow-hidden">
        <div className="absolute inset-0 opacity-30 bg-pattern" />
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative h-full flex flex-col justify-center items-center text-center px-4"
        >
          <h1 className="text-5xl font-bold text-white mb-4">🎭 Movie Recommender</h1>
          <p className="text-xl text-gray-100 max-w-2xl">Discover movies tailored to your taste using AI and sentiment analysis</p>
        </motion.div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        {/* Section Title */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="mb-12"
        >
          <h2 className="text-4xl font-bold text-white mb-2">🔥 Trending Now</h2>
          <p className="text-gray-400">Browse trending movies with ML-powered recommendations</p>
        </motion.div>

        {/* Loading State */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <motion.div
                key={i}
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="h-96 bg-gray-700 rounded-lg"
              />
            ))}
          </div>
        ) : (
          /* Movie Grid */
          <motion.div
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
            variants={container}
            initial="hidden"
            animate="show"
          >
            {trendingMovies.map((movie) => (
              <motion.div key={movie.id} variants={item}>
                <MovieCard {...movie} />
              </motion.div>
            ))}
          </motion.div>
        )}
      </div>
    </div>
  );
}
