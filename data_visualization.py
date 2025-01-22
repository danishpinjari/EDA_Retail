# src/data_visualization.py

import matplotlib.pyplot as plt

def plot_total_amount_by_category(total_amount_by_category):
    """
    Plot the total amount by product category.
    
    Parameters:
    total_amount_by_category (pd.Series): Total amount by product category.
    """
    plt.figure(figsize=(12, 10))
    plt.bar(total_amount_by_category.index, total_amount_by_category)
    plt.ylim(140000, max(total_amount_by_category) + 500)
    plt.title('Total Amount by Product Category')
    plt.xlabel('Product Category')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.show()

def plot_total_amount_by_month(monthly_total_amount):
    """
    Plot the total amount by month.
    
    Parameters:
    monthly_total_amount (pd.Series): Total amount by month.
    """
    plt.figure(figsize=(12, 10))
    plt.bar(monthly_total_amount.index, monthly_total_amount)
    plt.ylim(20000, max(monthly_total_amount) + 500)
    plt.title('Total Amount by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.show()
 
