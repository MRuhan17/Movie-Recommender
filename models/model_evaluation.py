"""ML Model Evaluation and Metrics for Movie Recommender"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from typing import Dict, List, Tuple
import pickle
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Comprehensive model evaluation suite"""
    
    def __init__(self, model_path: str):
        self.model = self.load_model(model_path)
        self.metrics = {}
        
    def load_model(self, path: str):
        """Load trained model from pickle file"""
        try:
            with open(path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded from {path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None
            
    def calculate_rmse(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Root Mean Squared Error"""
        return np.sqrt(mean_squared_error(y_true, y_pred))
        
    def calculate_mae(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Error"""
        return mean_absolute_error(y_true, y_pred)
        
    def calculate_precision_at_k(self, y_true: List, y_pred: List, k: int = 10) -> float:
        """Calculate Precision@K for recommendations"""
        if k > len(y_pred):
            k = len(y_pred)
        
        top_k = y_pred[:k]
        relevant = sum([1 for item in top_k if item in y_true])
        return relevant / k if k > 0 else 0.0
        
    def calculate_recall_at_k(self, y_true: List, y_pred: List, k: int = 10) -> float:
        """Calculate Recall@K for recommendations"""
        if k > len(y_pred):
            k = len(y_pred)
            
        top_k = y_pred[:k]
        relevant = sum([1 for item in top_k if item in y_true])
        return relevant / len(y_true) if len(y_true) > 0 else 0.0
        
    def calculate_ndcg(self, y_true: List, y_pred: List, k: int = 10) -> float:
        """Calculate Normalized Discounted Cumulative Gain@K"""
        dcg = 0.0
        for i, item in enumerate(y_pred[:k]):
            if item in y_true:
                dcg += 1.0 / np.log2(i + 2)
        
        idcg = sum([1.0 / np.log2(i + 2) for i in range(min(k, len(y_true)))])
        return dcg / idcg if idcg > 0 else 0.0
        
    def coverage(self, predictions: List[List], n_items: int) -> float:
        """Calculate catalog coverage"""
        unique_items = set()
        for pred_list in predictions:
            unique_items.update(pred_list)
        return len(unique_items) / n_items
        
    def diversity(self, predictions: List[List]) -> float:
        """Calculate average pairwise diversity"""
        diversities = []
        for pred_list in predictions:
            unique = len(set(pred_list))
            diversities.append(unique / len(pred_list) if len(pred_list) > 0 else 0)
        return np.mean(diversities)
        
    def evaluate_model(self, test_data: pd.DataFrame) -> Dict:
        """Run comprehensive evaluation"""
        logger.info("Starting model evaluation...")
        
        # Extract test ratings
        y_true = test_data['rating'].values
        user_ids = test_data['userId'].values
        movie_ids = test_data['movieId'].values
        
        # Make predictions
        predictions = []
        for uid, mid in zip(user_ids, movie_ids):
            try:
                pred = self.model.predict(uid, mid).est
                predictions.append(pred)
            except:
                predictions.append(3.0)  # Default prediction
        
        y_pred = np.array(predictions)
        
        # Calculate metrics
        self.metrics = {
            'RMSE': round(self.calculate_rmse(y_true, y_pred), 4),
            'MAE': round(self.calculate_mae(y_true, y_pred), 4),
            'n_predictions': len(predictions),
            'mean_prediction': round(np.mean(y_pred), 4),
            'std_prediction': round(np.std(y_pred), 4)
        }
        
        logger.info(f"Evaluation complete: {self.metrics}")
feat: Add comprehensive ML model evaluation suite        
    def print_metrics(self):
        """Pretty print evaluation metrics"""
        print("\n" + "="*50)
        print("MODEL EVALUATION METRICS")
        print("="*50)
        for metric, - RMSE and MAE calculation for accuracy
- Precision@K and Recall@K for recommendation quality
- NDCG (Normalized Discounted Cumulative Gain)
- Coverage and diversity metrics
- Model loading and prediction utilities
- Metrics export to filevalue in self.metrics.items():
            print(f"{metric:20s}: {value}")
        print("="*50 + "\n")
        
    def save_metrics(self, filepath: str):
        """Save metrics to file"""
        with open(filepath, 'w') as f:
            f.write("Model Evaluation Metrics\n")
            f.write("=" * 40 + "\n")
            for metric, value in self.metrics.items():
                f.write(f"{metric}: {value}\n")
        logger.info(f"Metrics saved to {filepath}")

if __name__ == "__main__":
    # Example usage
    evaluator = ModelEvaluator('cf_model.pkl')
    print("Model evaluator initialized successfully")
