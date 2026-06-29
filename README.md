# E-Commerce Database Manager

A Streamlit-powered e-commerce database management system for PostgreSQL. This project provides customer, product, and sales management functionality, plus a sales analytics dashboard and invoice generation.

## Features

- Customer management
  - Add, view, update, delete customers
- Product inventory management
  - Add, view, update, delete products
- Sales management
  - Create sales records
  - View and update sales
  - Generate invoice previews
- Sales analytics
  - Revenue metrics
  - Sales trends over time
  - Top selling products
  - Customer revenue summaries
- PostgreSQL database integration
- Streamlit UI for web-based interaction

## Project Structure

- `app.py` - Streamlit dashboard and UI for managing customers, products, sales, analytics, and reports
- `main.py` - CLI menu for customer, product, and sales management
- `Database.py` - PostgreSQL connection helper using Streamlit secrets
- `Customers.py` - Customer table definitions and CRUD operations
- `Products.py` - Product table definitions and CRUD operations
- `Sales.py` - Sales table definitions, billing, analytics, and CRUD operations
- `SalesItem.py` - Sale item table definitions and invoice item management
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.10+ (or compatible)
- PostgreSQL database
- Streamlit
- pandas
- plotly
- psycopg2-binary

## Installation

1. Clone or download the project.
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a Streamlit secrets file at `.streamlit/secrets.toml` with your PostgreSQL credentials:

```toml
DB_HOST = "your-db-host"
DB_NAME = "your-database-name"
DB_USER = "your-db-user"
DB_PASSWORD = "your-db-password"
DB_PORT = "5432"
```

The app connects to PostgreSQL using these secrets.

## Usage

### Run the Streamlit application

```bash
streamlit run app.py
```

Open the browser link displayed by Streamlit to use the web app.

### Run the CLI menu

```bash
python main.py
```

Use the terminal menu to manage customers, products, and sales if you prefer a command-line interface.

## Database Notes

The app creates the following tables automatically if they do not exist:

- `customers`
- `products`
- `sales`
- `sale_items`

The sales and sale item tables are linked by foreign keys, and the app supports bill generation from sale records plus related items.
