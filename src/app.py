from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import os
from fastapi import Request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the FastAPI app
app = FastAPI()

# Load dataset with error handling
try:
    ds = pd.read_csv('data/raw/retail_sales_dataset.csv')
    logging.info("Dataset loaded successfully.")
except FileNotFoundError:
    logging.error("Dataset not found in the specified path!")
    raise HTTPException(status_code=500, detail="Dataset not found")

# Process the dataset
ds['Date'] = pd.to_datetime(ds['Date'])
ds['Month'] = ds['Date'].dt.month_name()

# Set up static files for CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_html(request: Request):
    # Pass data to the template for rendering
    return templates.TemplateResponse("index.html", {"request": request})

# Define models for API responses
class Insights(BaseModel):
    total_sales: float
    average_age: float
    male_count: int
    female_count: int

class SalesByCategory(BaseModel):
    labels: list
    data: list

class SalesByMonth(BaseModel):
    labels: list
    data: list

class Transaction(BaseModel):
    transaction_id: int
    date: str
    customer_id: str
    gender: str
    age: int
    product_category: str
    quantity: int
    price_per_unit: float
    total_amount: float

# Main route with welcome message
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "Welcome to the Retail Sales Analysis API!"

# Get insights: total sales, average age, gender distribution
@app.get("/insights", response_model=Insights)
async def get_insights():
    try:
        total_sales = ds['Total Amount'].sum()
        average_age = ds['Age'].mean()
        male_count = ds['Gender'].value_counts().get('Male', 0)
        female_count = ds['Gender'].value_counts().get('Female', 0)
        
        return Insights(
            total_sales=total_sales,
            average_age=average_age,
            male_count=male_count,
            female_count=female_count
        )
    except Exception as e:
        logging.error("Error fetching insights: %s", e)
        raise HTTPException(status_code=500, detail="Error fetching insights")

# Sales data by product category
@app.get("/sales/category", response_model=SalesByCategory)
async def get_sales_by_category():
    try:
        category_sales = ds.groupby('Product Category')['Total Amount'].sum()
        
        return SalesByCategory(
            labels=category_sales.index.tolist(),
            data=category_sales.values.tolist()
        )
    except Exception as e:
        logging.error("Error fetching sales by category: %s", e)
        raise HTTPException(status_code=500, detail="Error fetching sales by category")

# Sales data by month
@app.get("/sales/month", response_model=SalesByMonth)
async def get_sales_by_month():
    try:
        month_sales = ds.groupby('Month')['Total Amount'].sum()
        
        return SalesByMonth(
            labels=month_sales.index.tolist(),
            data=month_sales.values.tolist()
        )
    except Exception as e:
        logging.error("Error fetching sales by month: %s", e)
        raise HTTPException(status_code=500, detail="Error fetching sales by month")

# Get all transactions
@app.get("/transactions", response_model=list[Transaction])
async def get_transactions():
    try:
        transactions = ds.to_dict(orient='records')
        
        return [
            Transaction(
                transaction_id=trans['Transaction ID'],
                date=trans['Date'].strftime('%Y-%m-%d'),
                customer_id=trans['Customer ID'],
                gender=trans['Gender'],
                age=trans['Age'],
                product_category=trans['Product Category'],
                quantity=trans['Quantity'],
                price_per_unit=trans['Price per Unit'],
                total_amount=trans['Total Amount']
            ) for trans in transactions
        ]
    except Exception as e:
        logging.error("Error fetching transactions: %s", e)
        raise HTTPException(status_code=500, detail="Error fetching transactions")

# Get a specific transaction by ID
@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    try:
        transaction = ds[ds['Transaction ID'] == transaction_id]
        
        if transaction.empty:
            raise HTTPException(status_code=404, detail=f"Transaction with ID {transaction_id} not found")
        
        trans = transaction.iloc[0].to_dict()
        
        return Transaction(
            transaction_id=trans['Transaction ID'],
            date=trans['Date'].strftime('%Y-%m-%d'),
            customer_id=trans['Customer ID'],
            gender=trans['Gender'],
            age=trans['Age'],
            product_category=trans['Product Category'],
            quantity=trans['Quantity'],
            price_per_unit=trans['Price per Unit'],
            total_amount=trans['Total Amount']
        )
    except Exception as e:
        logging.error("Error fetching transaction ID %s: %s", transaction_id, e)
        raise HTTPException(status_code=500, detail="Error fetching transaction")
