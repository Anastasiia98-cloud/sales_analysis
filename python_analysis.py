import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def load_sales_data(filepath):
    """Load sales data from a text file."""
    # Read the CSV-formatted text file
    df = pd.read_csv(filepath)
    
    # Convert date strings to datetime objects
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate total sales amount
    df['total_sales'] = df['units'] * df['price_per_unit']
    
    return df

def analyze_sales(df):
    """Perform basic analysis on the sales data."""
    # Summary statistics
    total_revenue = df['total_sales'].sum()
    avg_units_per_transaction = df['units'].mean()
    
    # Group by region
    region_sales = df.groupby('region')['total_sales'].sum().sort_values(ascending=False)
    
    # Group by product
    product_sales = df.groupby('product')['total_sales'].sum().sort_values(ascending=False)
    
    # Group by month
    df['month'] = df['date'].dt.strftime('%Y-%m')
    monthly_sales = df.groupby('month')['total_sales'].sum()
    
    return {
        'total_revenue': total_revenue,
        'avg_units': avg_units_per_transaction,
        'region_sales': region_sales,
        'product_sales': product_sales,
        'monthly_sales': monthly_sales
    }

def visualize_data(analysis_results):
    """Create visualizations for the analyzed data."""
    # Create a figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot sales by region
    analysis_results['region_sales'].plot(kind='bar', ax=axs[0, 0], color='skyblue')
    axs[0, 0].set_title('Sales by Region')
    axs[0, 0].set_ylabel('Total Sales ($)')
    
    # Plot sales by product
    analysis_results['product_sales'].plot(kind='bar', ax=axs[0, 1], color='lightgreen')
    axs[0, 1].set_title('Sales by Product')
    axs[0, 1].set_ylabel('Total Sales ($)')
    
    # Plot monthly sales
    analysis_results['monthly_sales'].plot(kind='line', marker='o', ax=axs[1, 0], color='coral')
    axs[1, 0].set_title('Monthly Sales Trend')
    axs[1, 0].set_ylabel('Total Sales ($)')
    
    # Plot units sold by product (from the original dataframe)
    df.groupby('product')['units'].sum().plot(kind='pie', ax=axs[1, 1], autopct='%1.1f%%')
    axs[1, 1].set_title('Units Sold by Product')
    
    # Adjust layout and save figure
    plt.tight_layout()
    plt.savefig('sales_analysis.png')
    plt.show()

if __name__ == "__main__":
    # File path
    file_path = "sales_data.txt"
    
    # Load and analyze data
    df = load_sales_data(file_path)
    results = analyze_sales(df)
    
    # Print summary
    print(f"Sales Analysis Summary:")
    print(f"---------------------")
    print(f"Total Revenue: ${results['total_revenue']:,.2f}")
    print(f"Average Units per Transaction: {results['avg_units']:.2f}")
    print("\nSales by Region:")
    print(results['region_sales'])
    print("\nSales by Product:")
    print(results['product_sales'])
    print("\nMonthly Sales:")
    print(results['monthly_sales'])
    
    # Create visualizations
    visualize_data(results)