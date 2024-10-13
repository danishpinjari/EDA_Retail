# src/config.py

import os

class Config:
    """
    Configuration class to store paths and other settings for the project.
    """

    # Path to the raw data file
    RAW_DATA_PATH = os.path.join("data", "raw", "retail_sales_dataset.csv")
    
    # Path to the processed data file
    PROCESSED_DATA_PATH = os.path.join("data", "processed", "processed_data.csv")
    
    # Output directory for visualizations
    OUTPUT_VISUALIZATION_DIR = os.path.join("static", "images")

    # Other configuration variables
    # Example: set a random seed for reproducibility
    RANDOM_SEED = 42
    
    # Example: define a list of product categories for analysis
    PRODUCT_CATEGORIES = ['Beauty', 'Clothing', 'Electronics', 'Home', 'Sports']
