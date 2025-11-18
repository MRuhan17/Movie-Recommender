// Utility functions for Movie Recommender UI

// Format rating to 1 decimal place
export const formatRating = (rating: number): string => {
  return rating.toFixed(1);
};

// Format ML confidence as percentage
export const formatConfidence = (confidence: number): string => {
  return `${(confidence * 100).toFixed(0)}%`;
};

// Get confidence color based on value
export const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) return 'text-green-400';
  if (confidence >= 0.6) return 'text-blue-400';
  if (confidence >= 0.4) return 'text-yellow-400';
  return 'text-red-400';
};

// Format genre list (max 3)
export const formatGenres = (genres: string[], max: number = 3): string[] => {
  return genres.slice(0, max);
};

// Get TMDB poster URL
export const getTMDBPosterUrl = (posterPath: string, size: string = 'w500'): string => {
  return `https://image.tmdb.org/t/p/${size}${posterPath}`;
};

// Truncate text with ellipsis
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

// Calculate stats from array
export const calculateStats = (values: number[]) => {
  if (values.length === 0) return { min: 0, max: 0, avg: 0, median: 0 };
  
  const sorted = [...values].sort((a, b) => a - b);
  const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
  const median = sorted[Math.floor(sorted.length / 2)];
  
  return {
    min: sorted[0],
    max: sorted[sorted.length - 1],
    avg: parseFloat(avg.toFixed(2)),
    median
  };
};

// Debounce function for search
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

// Format large numbers (e.g., 1000 -> 1K)
export const formatNumber = (num: number): string => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
};

// Get rating badge color
export const getRatingBadgeColor = (rating: number): string => {
feat: Add comprehensive utility functions for UI  if (rating >= 7.0) return 'bg-yellow-500';
  if (rating >= 6.0) return 'bg-orange-500';
  return 'bg-red-500';
};

// Classify rating
export const getRatin- Format rating, confidence, and numbers
- TMDB poster URL builder
- Statistical calculations (min, max, avg, median)
- Debounce function for search optimization
- Color helpers for ratings and confidence
- API error handling utilitiesgLabel = (rating: number): string => {
  if (rating >= 8.5) return 'Excellent';
  if (rating >= 7.5) return 'Great';
  if (rating >= 6.5) return 'Good';
  if (rating >= 5.0) return 'Average';
  return 'Poor';
};

// API error handler
export const handleAPIError = (error: any): string => {
  if (error.response) {
    return error.response.data.message || 'Server error occurred';
  } else if (error.request) {
    return 'No response from server';
  }
  return error.message || 'An unexpected error occurred';
};
