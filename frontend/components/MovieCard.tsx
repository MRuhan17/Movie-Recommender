'use client';

import { motion } from 'framer-motion';
import Image from 'next/image';
import React from 'react';

interface MovieCardProps {
  id: number;
  title: string;
  posterUrl: string;
  rating: number;
  mlConfidence: number;
  releaseYear: number;
  genres: string[];
}

export default function MovieCard({
  id,
  title,
  posterUrl,
  rating,
  mlConfidence,
  releaseYear,
  genres,
}: MovieCardProps) {
  return (
    <motion.div
      whileHover={{ y: -8, boxShadow: '0 20px 40px rgba(0,0,0,0.3)' }}
      transition={{ duration: 0.3 }}
      className="group relative w-full rounded-lg overflow-hidden bg-gray-800 shadow-lg hover:shadow-2xl cursor-pointer"
    >
      {/* Poster Image */}
      <div className="relative h-72 w-full overflow-hidden bg-gradient-to-br from-gray-700 to-gray-900">
        <Image
          src={posterUrl}
          alt={title}
          fill
          className="object-cover group-hover:scale-110 transition-transform duration-300"
          priority
        />
        {/* Rating Badge */}
        <div className="absolute top-3 right-3 bg-yellow-500 text-gray-900 px-3 py-1 rounded-full font-bold text-sm">
          ★ {rating.toFixed(1)}
        </div>
        {/* ML Confidence Badge */}
        <div className="absolute top-3 left-3 bg-blue-600 text-white px-3 py-1 rounded-full font-semibold text-xs">
          ML: {(mlConfidence * 100).toFixed(0)}%
        </div>
      </div>

      {/* Content Section */}
      <div className="p-4 bg-gray-800">
        <h3 className="text-lg font-bold text-white truncate mb-1">{title}</h3>
        <p className="text-gray-400 text-sm mb-3">{releaseYear}</p>

        {/* Genres */}
        <div className="flex flex-wrap gap-2 mb-3">
          {genres.slice(0, 3).map((genre) => (
            <span
              key={genre}
              className="text-xs bg-gray-700 text-gray-200 px-2 py-1 rounded"
            >
              {genre}
            </span>
          ))}
        </div>

        {/* Sentiment Indicator */}
        <div className="flex items-center gap-2">
          <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              whileInView={{ width: `${mlConfidence * 100}%` }}
              transition={{ duration: 0.6 }}
              className="h-full bg-gradient-to-r from-green-400 to-blue-500"
            />
          </div>
          <span className="text-xs text-gray-400">Match</span>
        </div>
      </div>
    </motion.div>
  );
}
