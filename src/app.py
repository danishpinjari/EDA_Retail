from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import pandas as pd
from src.data_processing import load_data, preprocess_data
from src.data_visualization import plot_total_amount_by_category, plot_total_amount_by_month
from pydantic import BaseModel
from fastapi import HTTPException

app = FastAPI()

# Load the dataset
ds = pd.read_csv('data/raw/retail_sales_dataset.csv')
ds['Date'] = pd.to_datetime(ds['Date'])
ds['Month'] = ds['Date'].dt.month_name()

# Set up static files (for CSS and JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def read_html():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

# Define a model for insights
class Insights(BaseModel):
    total_sales: float
    average_age: float
    male_count: int
    female_count: int

# Define a model for sales by category
class SalesByCategory(BaseModel):
    labels: list
    data: list

# Define a model for sales by month
class SalesByMonth(BaseModel):
    labels: list
    data: list

# Define a model for transactions
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

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "Welcome to the Retail Sales Analysis API!"

@app.get("/insights", response_model=Insights)
async def get_insights():
    total_sales = ds['Total Amount'].sum()
    average_age = ds['Age'].mean()
    male_count = ds['Gender'].value_counts().get('Male', 0)
    female_count = ds['Gender'].value_counts().get('Female', 0)
    
    return Insights(total_sales=total_sales, average_age=average_age, male_count=male_count, female_count=female_count)

@app.get("/sales/category", response_model=SalesByCategory)
async def get_sales_by_category():
    category_sales = ds.groupby('Product Category')['Total Amount'].sum()
    return SalesByCategory(labels=category_sales.index.tolist(), data=category_sales.values.tolist())

@app.get("/sales/month", response_model=SalesByMonth)
async def get_sales_by_month():
    month_sales = ds.groupby('Month')['Total Amount'].sum()
    return SalesByMonth(labels=month_sales.index.tolist(), data=month_sales.values.tolist())

@app.get("/transactions", response_model=list[Transaction])
async def get_transactions():
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

# Endpoint to get a specific transaction by Transaction ID
@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    transaction = ds[ds['Transaction ID'] == transaction_id]
    
    if transaction.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
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