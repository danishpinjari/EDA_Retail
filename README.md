# Retail Sales Analysis Project

## Project Overview
This project aims to analyze retail sales data to extract meaningful insights that can help improve business performance. The analysis includes data cleaning, preprocessing, and visualization using FastAPI for serving results via a web application.

## Project Structure
/retail_sales_analysis_project │
 ├── /data # Raw and processed data files 
 ├── /notebooks # Jupyter notebooks for exploratory analysis 
 ├── /src # Source code for the project 
 ├── /static # Static files (images, CSS, etc.) 
 ├── /templates # HTML templates for rendering pages 
 ├── /js # JavaScript files 
 ├── /reports # Reports generated from analysis 
 ├── requirements.txt # Python packages and versions required 
 └── README.md # Project documentation

## Installation

To run this project, ensure you have Python 3.8 or higher installed. You can create a virtual environment and install the required packages.

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the required packages
pip install -r requirements.txt

# Usage :

To run the FastAPI application, navigate to the src directory and run:

uvicorn app:app --reload
You can access the application at http://127.0.0.1:8000.

# Features
Load and preprocess retail sales data.
Visualize sales trends and patterns.
Serve insights via a web application

# Author
Pinjari Danish Yakub