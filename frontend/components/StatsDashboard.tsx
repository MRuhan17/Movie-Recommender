'use client';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const GENRE_DATA = [
  { name: 'Sci-Fi', value: 35, color: '#3B82F6' },
  { name: 'Action', value: 25, color: '#10B981' },
  { name: 'Drama', value: 20, color: '#F59E0B' },
  { name: 'Thriller', value: 15, color: '#EF4444' },
  { name: 'Comedy', value: 5, color: '#8B5CF6' }
];

const CONFIDENCE_DATA = [
  { range: '0-20%', count: 5 },
  { range: '20-40%', count: 12 },
  { range: '40-60%', count: 25 },
  { range: '60-80%', count: 38 },
  { range: '80-100%', count: 45 }
];

const ACCURACY_DATA = [
  { month: 'Jan', accuracy: 78 },
  { month: 'Feb', accuracy: 82 },
  { month: 'Mar', accuracy: 85 },
  { month: 'Apr', accuracy: 87 },
  { month: 'May', accuracy: 89 },
  { month: 'Jun', accuracy: 91 }
];

export default function StatsDashboard() {
  const [stats] = useState({
    totalMoviesWatched: 127,
    avgRating: 8.2,
    topGenre: 'Sci-Fi',
    modelAccuracy: 91,
    avgConfidence: 0.86
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-16">
      <div className="container mx-auto px-4">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
          <h2 className="text-4xl font-bold text-white mb-3">📊 Your Movie Stats</h2>
          <p className="text-gray-400">Visualize your taste profile and ML model predictions</p>
        </motion.div>

        {/* Key Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-12">
          {[
            { label: 'Movies Watched', value: stats.totalMoviesWatched, icon: '🎬' },
            { label: 'Avg Rating', value: stats.avgRating.toFixed(1), icon: '⭐' },
            { label: 'Top Genre', value: stats.topGenre, icon: '🎭' },
            { label: 'Model Accuracy', value: `${stats.modelAccuracy}%`, icon: '🤖' },
            { label: 'Avg Confidence', value: `${(stats.avgConfidence * 100).toFixed(0)}%`, icon: '📈' }
          ].map((stat, i) => (
            <motion.div key={i} whileHover={{ y: -4 }} className="bg-gradient-to-br from-gray-800 to-gray-900 p-6 rounded-lg border border-gray-700">
              <div className="text-3xl mb-2">{stat.icon}</div>
              <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
              <div className="text-sm text-gray-400">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Genre Preferences */}
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-2xl font-bold text-white mb-6">Genre Preferences</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={GENRE_DATA} cx="50%" cy="50%" outerRadius={100} dataKey="value" label>
                  {GENRE_DATA.map((entry, index) => (<Cell key={index} fill={entry.color} />))}
                </Pie>
                <Tooltip contentStyle={{ background: '#1F2937', border: 'none' }} />
              </PieChart>
            </ResponsiveContainer>
          </motion.div>

          {/* ML Confidence Distribution */}
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-2xl font-bold text-white mb-6">ML Confidence Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={CONFIDENCE_DATA}>
                <XAxis dataKey="range" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip contentStyle={{ background: '#1F2937', border: 'none' }} />
                <Bar dataKey="count" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Model Accuracy Trend */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-gray-800 p-6 rounded-lg border border-gray-700 lg:col-span-2">
            <h3 className="text-2xl font-bold text-white mb-6">Model Accuracy Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={ACCURACY_DATA}>
                <XAxis dataKey="month" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip contentStyle={{ background: '#1F2937', border: 'none' }} />
                <Line type="monotone" dataKey="accuracy" stroke="#10B981" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
