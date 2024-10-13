# src/app.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import pandas as pd
from src.data_processing import load_data, preprocess_data
from src.data_visualization import plot_total_amount_by_category, plot_total_amount_by_month

# Initialize the FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load and preprocess data
file_path = 'data/raw/retail_sales_dataset.csv'
data = load_data(file_path)
processed_data = preprocess_data(data)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def show_results(request: Request):
    # Basic analysis results
    total_amount_by_category = processed_data.groupby('Product Category')['Total Amount'].sum()
    monthly_total_amount = processed_data.groupby('Month')['Total Amount'].sum().sort_values()

    # Plot the visualizations
    plot_total_amount_by_category(total_amount_by_category)
    plot_total_amount_by_month(monthly_total_amount)

    return templates.TemplateResponse("results.html", {"request": request, 
                                                        "total_amount_by_category": total_amount_by_category,
                                                        "monthly_total_amount": monthly_total_amount})
