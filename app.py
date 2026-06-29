import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Database import connection
from Customers import Customers
from Products import Products
from Sales import Sales
from SalesItem import SaleItems

# Page configuration
st.set_page_config(
    page_title="E-Commerce Database Management System",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main-title {
            color: #2c3e50;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 10px;
            color: #155724;
        }
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 10px;
            color: #721c24;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tables_initialized' not in st.session_state:
    st.session_state.tables_initialized = False

# Initialize tables if they don't exist
def initialize_tables():
    try:
        Customers.create_table()
        Products.create_table()
        Sales.create_table()
        SaleItems.create_table()
        
        # Fix sequences for all tables
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT setval('customers_id_seq', COALESCE((SELECT MAX(id) FROM customers), 0))")
        cur.execute("SELECT setval('products_id_seq', COALESCE((SELECT MAX(id) FROM products), 0))")
        cur.execute("SELECT setval('sales_id_seq', COALESCE((SELECT MAX(id) FROM sales), 0))")
        cur.execute("SELECT setval('sale_items_id_seq', COALESCE((SELECT MAX(id) FROM sale_items), 0))")
        conn.commit()
        cur.close()
        conn.close()
        
        st.session_state.tables_initialized = True
        return True
    except Exception as e:
        st.error(f"Error initializing tables: {e}")
        return False

# Sidebar Navigation
st.sidebar.markdown("# 🛍️ E-Commerce Management System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select a Module:",
    ["📊 Dashboard", "👥 Customers", "📦 Products", "💳 Sales", "⚙️ Settings"]
)

st.sidebar.markdown("---")
st.sidebar.info("👨‍💼 Database Management System\nManage your e-commerce database efficiently")

# ======================== DASHBOARD PAGE ========================
if page == "📊 Dashboard":
    st.markdown("<h1 class='main-title'>📊 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.tables_initialized:
        initialize_tables()
    
    try:
        # Get data for metrics
        customers = Customers.get_all_customers()
        products = Products.view_product()
        sales = Sales.view_sales()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Customers", len(customers) if customers else 0, delta="Active")
        
        with col2:
            st.metric("📦 Total Products", len(products) if products else 0, delta="In Stock")
        
        with col3:
            st.metric("💳 Total Sales", len(sales) if sales else 0, delta="Transactions")
        
        with col4:
            total_revenue = sum([sale[3] for sale in sales]) if sales else 0
            st.metric("💰 Total Revenue", f"${total_revenue:.2f}", delta="Income")
        
        st.markdown("---")
        
        # Display tables
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔝 Recent Customers")
            if customers:
                df_customers = pd.DataFrame(customers, columns=['ID', 'Name', 'Contact'])
                st.dataframe(df_customers.tail(5), use_container_width=True, hide_index=True)
            else:
                st.info("No customers found")
        
        with col2:
            st.subheader("🔝 Recent Products")
            if products:
                df_products = pd.DataFrame(products, columns=['ID', 'Name', 'Description', 'Price', 'Quantity'])
                st.dataframe(df_products.tail(5), use_container_width=True, hide_index=True)
            else:
                st.info("No products found")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

# ======================== CUSTOMERS PAGE ========================
elif page == "👥 Customers":
    st.markdown("<h1 class='main-title'>👥 Customers Management</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.tables_initialized:
        initialize_tables()
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Customer", "📋 View Customers", "✏️ Update/Delete"])
    
    # Add Customer
    with tab1:
        st.subheader("Add New Customer")
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name", key="new_customer_name")
        
        with col2:
            customer_contact = st.text_input("Contact Number", key="new_customer_contact")
        
        if st.button("➕ Add Customer", key="add_customer_btn"):
            if customer_name and customer_contact:
                try:
                    Customers.insert_customer(customer_name, customer_contact)
                    st.success(f"✅ Customer '{customer_name}' added successfully!")
                except Exception as e:
                    st.error(f"Error adding customer: {e}")
            else:
                st.warning("Please fill all fields")
    
    # View Customers
    with tab2:
        st.subheader("All Customers")
        try:
            customers = Customers.get_all_customers()
            if customers:
                df_customers = pd.DataFrame(customers, columns=['ID', 'Name', 'Contact'])
                st.dataframe(df_customers, use_container_width=True, hide_index=True)
                st.info(f"Total Customers: {len(customers)}")
            else:
                st.info("No customers found")
        except Exception as e:
            st.error(f"Error fetching customers: {e}")
    
    # Update/Delete Customer
    with tab3:
        try:
            customers = Customers.get_all_customers()
            if customers:
                customer_options = {f"ID: {c[0]} - {c[1]}": c[0] for c in customers}
                selected_customer = st.selectbox("Select Customer", customer_options.keys())
                customer_id = customer_options[selected_customer]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("New Name (leave empty to keep current)", key="update_name")
                
                with col2:
                    new_contact = st.text_input("New Contact (leave empty to keep current)", key="update_contact")
                
                col_update, col_delete = st.columns(2)
                
                with col_update:
                    if st.button("✏️ Update Customer"):
                        try:
                            Customers.update_customer(customer_id, new_name if new_name else None, new_contact if new_contact else None)
                            st.success("✅ Customer updated successfully!")
                        except Exception as e:
                            st.error(f"Error updating customer: {e}")
                
                with col_delete:
                    if st.button("🗑️ Delete Customer"):
                        try:
                            Customers.delete_customer(customer_id)
                            st.success("✅ Customer deleted successfully!")
                        except Exception as e:
                            st.error(f"Error deleting customer: {e}")
            else:
                st.info("No customers found")
        except Exception as e:
            st.error(f"Error: {e}")

# ======================== PRODUCTS PAGE ========================
elif page == "📦 Products":
    st.markdown("<h1 class='main-title'>📦 Products Management</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.tables_initialized:
        initialize_tables()
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Product", "📋 View Products", "✏️ Update/Delete"])
    
    # Add Product
    with tab1:
        st.subheader("Add New Product")
        
        product_name = st.text_input("Product Name", key="new_product_name")
        product_description = st.text_area("Product Description", key="new_product_desc")
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_price = st.number_input("Price ($)", min_value=0.0, format="%.2f", key="new_product_price")
        
        with col2:
            product_quantity = st.number_input("Quantity", min_value=0, step=1, key="new_product_qty")
        
        if st.button("➕ Add Product", key="add_product_btn"):
            if product_name and product_description and product_price and product_quantity:
                try:
                    Products.insert_product(product_name, product_description, product_price, product_quantity)
                    st.success(f"✅ Product '{product_name}' added successfully!")
                except Exception as e:
                    st.error(f"Error adding product: {e}")
            else:
                st.warning("Please fill all fields")
    
    # View Products
    with tab2:
        st.subheader("All Products")
        try:
            products = Products.view_product()
            if products:
                df_products = pd.DataFrame(products, columns=['ID', 'Name', 'Description', 'Price', 'Quantity'])
                st.dataframe(df_products, use_container_width=True, hide_index=True)
                st.info(f"Total Products: {len(products)}")
            else:
                st.info("No products found")
        except Exception as e:
            st.error(f"Error fetching products: {e}")
    
    # Update/Delete Product
    with tab3:
        try:
            products = Products.view_product()
            if products:
                product_options = {f"ID: {p[0]} - {p[1]}": p[0] for p in products}
                selected_product = st.selectbox("Select Product", product_options.keys())
                product_id = product_options[selected_product]
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("New Name (leave empty to keep current)", key="update_prod_name")
                    new_description = st.text_area("New Description (leave empty to keep current)", key="update_prod_desc")
                
                with col2:
                    new_price = st.number_input("New Price (0 to keep current)", min_value=0.0, format="%.2f", key="update_prod_price")
                    new_quantity = st.number_input("New Quantity (-1 to keep current)", min_value=-1, step=1, key="update_prod_qty")
                
                col_update, col_delete = st.columns(2)
                
                with col_update:
                    if st.button("✏️ Update Product"):
                        try:
                            Products.update_product(
                                product_id,
                                name=new_name if new_name else None,
                                description=new_description if new_description else None,
                                price=new_price if new_price > 0 else None,
                                quantity=new_quantity if new_quantity >= 0 else None
                            )
                            st.success("✅ Product updated successfully!")
                        except Exception as e:
                            st.error(f"Error updating product: {e}")
                
                with col_delete:
                    if st.button("🗑️ Delete Product"):
                        try:
                            Products.delete_product(product_id)
                            st.success("✅ Product deleted successfully!")
                        except Exception as e:
                            st.error(f"Error deleting product: {e}")
            else:
                st.info("No products found")
        except Exception as e:
            st.error(f"Error: {e}")

# ======================== SALES PAGE ========================
elif page == "💳 Sales":
    st.markdown("<h1 class='main-title'>💳 Sales Management</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.tables_initialized:
        initialize_tables()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["➕ Add Sale", "📋 View Sales", "📊 Analytics", "✏️ Update/Delete", "🧾 Generate Bill"])
    
    # Add Sale
    with tab1:
        st.subheader("Create New Sale")
        
        try:
            customers = Customers.get_all_customers()
            if customers:
                customer_options = {f"ID: {c[0]} - {c[1]}": c[0] for c in customers}
                selected_customer = st.selectbox("Select Customer", customer_options.keys(), key="sale_customer")
                customer_id = customer_options[selected_customer]
                
                sale_date = st.date_input("Sale Date", datetime.now().date())
                total_amount = st.number_input("Total Amount ($)", min_value=0.0, format="%.2f")
                
                if st.button("➕ Create Sale"):
                    try:
                        Sales.insert_sale(customer_id, sale_date, total_amount)
                        st.success("✅ Sale created successfully!")
                    except Exception as e:
                        st.error(f"Error creating sale: {e}")
            else:
                st.info("Please add customers first")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # View Sales
    with tab2:
        st.subheader("All Sales")
        try:
            sales = Sales.view_sales()
            if sales:
                df_sales = pd.DataFrame(sales, columns=['ID', 'Customer ID', 'Date', 'Total Amount'])
                st.dataframe(df_sales, use_container_width=True, hide_index=True)
                st.info(f"Total Sales: {len(sales)} | Total Revenue: ${sum([s[3] for s in sales]):.2f}")
            else:
                st.info("No sales found")
        except Exception as e:
            st.error(f"Error fetching sales: {e}")
    
    # Analytics
    with tab3:
        st.subheader("📊 Sales Analytics & Visualizations")
        
        try:
            sales = Sales.view_sales()
            customers = Customers.get_all_customers()
            products = Sales.get_top_selling_products()
            
            if sales:
                # Create DataFrame for sales data
                df_sales = pd.DataFrame(sales, columns=['ID', 'Customer ID', 'Date', 'Total Amount'])
                
                # Convert Date to datetime
                df_sales['Date'] = pd.to_datetime(df_sales['Date'])
                
                st.markdown("---")
                
                # Row 1: Key Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💳 Total Sales", len(df_sales))
                with col2:
                    st.metric("💰 Total Revenue", f"${df_sales['Total Amount'].sum():.2f}")
                with col3:
                    st.metric("📊 Avg Sale Amount", f"${df_sales['Total Amount'].mean():.2f}")
                
                st.markdown("---")
                
                # Row 2: Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📈 Sales Trend Over Time**")
                    # Group by date and sum amounts
                    sales_by_date = df_sales.groupby('Date')['Total Amount'].sum().reset_index()
                    fig_trend = px.line(sales_by_date, x='Date', y='Total Amount', 
                                       title='Sales Amount Over Time',
                                       markers=True,
                                       line_shape='linear')
                    fig_trend.update_layout(height=400)
                    st.plotly_chart(fig_trend, use_container_width=True)
                
                with col2:
                    st.write("**📊 Sales Distribution**")
                    fig_dist = px.histogram(df_sales, x='Total Amount', nbins=10,
                                           title='Sales Amount Distribution',
                                           color_discrete_sequence=['#667eea'])
                    fig_dist.update_layout(height=400)
                    st.plotly_chart(fig_dist, use_container_width=True)
                
                st.markdown("---")
                
                # Row 3: Top Products
                if products:
                    st.write("**🏆 Top 5 Selling Products**")
                    df_products = pd.DataFrame(products, columns=['Product ID', 'Total Quantity'])
                    fig_products = px.bar(df_products, x='Product ID', y='Total Quantity',
                                         title='Top Selling Products by Quantity',
                                         color='Total Quantity',
                                         color_continuous_scale='Viridis')
                    fig_products.update_layout(height=400)
                    st.plotly_chart(fig_products, use_container_width=True)
                
                st.markdown("---")
                
                # Row 4: Sales by Date Range Analysis
                st.write("**📅 Sales by Date Range**")
                col1, col2 = st.columns(2)
                
                with col1:
                    start_date = st.date_input("Start Date", df_sales['Date'].min().date())
                with col2:
                    end_date = st.date_input("End Date", df_sales['Date'].max().date())
                
                if st.button("📊 Analyze Period"):
                    try:
                        # Filter data by date range
                        filtered_sales = df_sales[(df_sales['Date'].dt.date >= start_date) & 
                                                 (df_sales['Date'].dt.date <= end_date)]
                        
                        if len(filtered_sales) > 0:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Sales Count", len(filtered_sales))
                            with col2:
                                st.metric("Total Amount", f"${filtered_sales['Total Amount'].sum():.2f}")
                            with col3:
                                st.metric("Average Amount", f"${filtered_sales['Total Amount'].mean():.2f}")
                            
                            # Line chart for period
                            sales_period = filtered_sales.groupby('Date')['Total Amount'].sum().reset_index()
                            fig_period = px.area(sales_period, x='Date', y='Total Amount',
                                                title='Sales During Selected Period',
                                                fill='tozeroy')
                            st.plotly_chart(fig_period, use_container_width=True)
                        else:
                            st.info("No sales found in this date range")
                    except Exception as e:
                        st.error(f"Error analyzing period: {e}")
                
                st.markdown("---")
                
                # Row 5: Customer Analysis
                st.write("**👥 Sales by Customer**")
                sales_by_customer = df_sales.groupby('Customer ID')['Total Amount'].agg(['sum', 'count']).reset_index()
                sales_by_customer.columns = ['Customer ID', 'Total Revenue', 'Number of Sales']
                
                # Join with customer names
                if customers:
                    customer_dict = {c[0]: c[1] for c in customers}
                    sales_by_customer['Customer Name'] = sales_by_customer['Customer ID'].map(customer_dict)
                
                fig_customers = px.bar(sales_by_customer, x='Customer ID', y='Total Revenue',
                                      title='Total Revenue by Customer',
                                      color='Total Revenue',
                                      color_continuous_scale='Blues',
                                      hover_data=['Number of Sales'])
                st.plotly_chart(fig_customers, use_container_width=True)
                
                st.markdown("---")
                
                # Detailed Statistics Table
                st.write("**📋 Detailed Sales Statistics**")
                st.dataframe(sales_by_customer, use_container_width=True, hide_index=True)
                
            else:
                st.info("No sales data available. Add some sales first!")
        except Exception as e:
            st.error(f"Error loading analytics: {e}")
    
    # Update/Delete Sale
    with tab4:
        try:
            sales = Sales.view_sales()
            if sales:
                sale_options = {f"ID: {s[0]} - Customer: {s[1]} - Date: {s[2]}": s[0] for s in sales}
                selected_sale = st.selectbox("Select Sale", sale_options.keys())
                sale_id = sale_options[selected_sale]
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_customer_id = st.number_input("New Customer ID (0 to keep current)", min_value=0)
                    new_date = st.date_input("New Date", datetime.now().date())
                
                with col2:
                    new_amount = st.number_input("New Amount (0 to keep current)", min_value=0.0, format="%.2f")
                
                col_update, col_delete = st.columns(2)
                
                with col_update:
                    if st.button("✏️ Update Sale"):
                        try:
                            Sales.update_sale(
                                sale_id,
                                customer_id=new_customer_id if new_customer_id > 0 else None,
                                date=new_date,
                                total_amount=new_amount if new_amount > 0 else None
                            )
                            st.success("✅ Sale updated successfully!")
                        except Exception as e:
                            st.error(f"Error updating sale: {e}")
                
                with col_delete:
                    if st.button("🗑️ Delete Sale"):
                        try:
                            Sales.delete_sale(sale_id)
                            st.success("✅ Sale deleted successfully!")
                        except Exception as e:
                            st.error(f"Error deleting sale: {e}")
            else:
                st.info("No sales found")
        except Exception as e:
            st.error(f"Error: {e}")

    # Generate Bill
    with tab5:
        st.subheader("🧾 Generate Bill")
        try:
            sales = Sales.view_sales()
            if not sales:
                st.info("No sales found. Create a sale first.")
            else:
                sale_options = {f"ID: {s[0]} - Customer: {s[1]} - Date: {s[2]}": s[0] for s in sales}
                selected_sale = st.selectbox("Select Sale", sale_options.keys(), key="bill_sale_select")
                sale_id = sale_options[selected_sale]

                products = Products.view_product()
                if not products:
                    st.info("No products found. Add products first.")
                else:
                    product_options = {p[1]: p[0] for p in products}
                    selected_product_name = st.selectbox("Select Product", list(product_options.keys()), key="bill_product_select")
                    product_id = product_options[selected_product_name]

                    default_price = next(p[3] for p in products if p[1] == selected_product_name)
                    quantity = st.number_input("Quantity", min_value=1, step=1, key="bill_quantity")
                    price = st.number_input("Unit Price", min_value=0.0, value=float(default_price), format="%.2f", key="bill_price")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("➕ Add Item to Bill"):
                            try:
                                SaleItems.add_sale_item(sale_id, product_id, int(quantity), float(price))
                                st.success("✅ Item added to bill")
                            except Exception as e:
                                st.error(f"Error adding item: {e}")
                    with col2:
                        if st.button("🧾 Preview Bill"):
                            try:
                                bill = Sales.generate_bill(sale_id)
                                if bill:
                                    st.markdown(f"### Invoice #{bill['sale_id']}")
                                    st.write(f"**Customer:** {bill['customer_name']}")
                                    st.write(f"**Contact:** {bill['customer_contact']}")
                                    st.write(f"**Date:** {bill['date']}")

                                    if bill['items']:
                                        bill_df = pd.DataFrame(bill['items'])
                                        st.dataframe(
                                            bill_df[['product_name', 'quantity', 'price', 'line_total']],
                                            use_container_width=True,
                                            hide_index=True
                                        )
                                        st.success(f"Total Amount: ${bill['computed_total']:.2f}")
                                    else:
                                        st.info("No items added to this bill yet")
                                else:
                                    st.warning("No bill data found")
                            except Exception as e:
                                st.error(f"Error generating bill: {e}")
        except Exception as e:
            st.error(f"Error loading bill section: {e}")

# ======================== SETTINGS PAGE ========================
elif page == "⚙️ Settings":
    st.markdown("<h1 class='main-title'>⚙️ Settings</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Initialize/Reset Tables", use_container_width=True):
            if initialize_tables():
                st.success("✅ Database tables initialized successfully!")
            else:
                st.error("❌ Error initializing tables")
    
    with col2:
        if st.button("📊 Check Database Status", use_container_width=True):
            try:
                conn = connection()
                cur = conn.cursor()
                cur.execute("SELECT version();")
                version = cur.fetchone()
                cur.close()
                conn.close()
                st.success(f"✅ Database Connected!\nVersion: {version[0]}")
            except Exception as e:
                st.error(f"❌ Database Connection Error: {e}")
    
    st.markdown("---")
    st.subheader("About")
    st.info("""
    **E-Commerce Database Manager v1.0**
    
    A comprehensive database management system for e-commerce operations.
    
    **Features:**
    - 👥 Customer Management
    - 📦 Product Inventory
    - 💳 Sales Transactions
    - 📊 Analytics & Reporting
    
    **Database:** PostgreSQL
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>E-Commerce Database Manager | Built by Soumendra Barick with Streamlit</p>",
    unsafe_allow_html=True
)
        
