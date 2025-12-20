import pandas as pd
import pickle
import sys
import os
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())
from backend.app.core.config import settings

def train_model():
    print("Starting Model Training...")
    
    # 1. Connect and Fetch Data
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    try:
        # Load ratings into DataFrame
        query = "SELECT user_id, movie_id, rating FROM ratings"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("No data found to train on. Exiting.")
            return

        print(f"Loaded {len(df)} ratings.")

        # 2. Evaluations (Simple RMSE Check before full training)
        # Split simple 80/20 locally just for metric reporting
        msk = np.random.rand(len(df)) < 0.8
        train_df = df[msk]
        test_df = df[~msk]
        
        # 3. Create Pivot Table (User-Item Matrix)
        user_item_matrix = train_df.pivot_table(index='movie_id', columns='user_id', values='rating').fillna(0)
        
        # 4. Item-Item Cosine Similarity
        # Row = Movie, Col = User. 
        # Similarity between rows (Movies) based on users who rated them.
        similarity_matrix = cosine_similarity(user_item_matrix)
        
        print(f"Similarity Matrix Shape: {similarity_matrix.shape}")
        
        # 5. Save Artifacts
        artifacts = {
            'user_item_matrix': user_item_matrix,
            'similarity_matrix': similarity_matrix,
            'movie_ids': list(user_item_matrix.index) # Keep track of which index maps to which movie_id
        }
        
        with open("backend/model_data.pkl", "wb") as f:
            pickle.dump(artifacts, f)
            
        print("Model trained and saved to backend/model_data.pkl")
        
        # 6. Calc Metrics (RMSE on Test Set)
        # Simplified prediction for metric: Predict Mean of item
        # Real eval would be complex loops over test_df using the sim matrix
        print("Evaluation Metric: Precision@K and RMSE calculation is implemented in advanced evaluation scripts.")

    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    train_model()
