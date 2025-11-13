import pandas as pd
import os

def load_datasets(data_dir="data"):
    """Load MovieLens datasets from the data directory.
    
    Args:
        data_dir (str): Path to the data directory. Defaults to "data".
    
    Returns:
        tuple: (ratings DataFrame, movies DataFrame)
    """
    ratings = pd.read_csv(os.path.join(data_dir, "ratings.csv"))
    movies = pd.read_csv(os.path.join(data_dir, "movies.csv"))
    return ratings, movies