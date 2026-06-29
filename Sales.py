from Database import con

class Sales:
    def __init__(self):
        pass
    
    @staticmethod
    def create_table():
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS sales(
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                
                CONSTRAINT fk_sales_customer
                FOREIGN KEY (customer_id)
                REFERENCES customers(id)
                ON DELETE CASCADE
            )"""
        )
        con.commit()
        cur.close()

    @staticmethod
    def insert_sale(customer_id, date, total_amount):
        cur = con.cursor()
        cur.execute(
            """INSERT INTO sales (customer_id, date, total_amount)
            VALUES (%s,%s,%s)
            """,
            (customer_id, date, total_amount)
        )
        con.commit()
        cur.close()
        
    @staticmethod
    def generate_bill(sale_id):
        cur = con.cursor()
        cur.execute(
            """SELECT s.id, s.customer_id, s.date, s.total_amount, c.name, c.contact
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            WHERE s.id = %s""",
            (sale_id,)
        )
        sale = cur.fetchone()
        if not sale:
            cur.close()
            return None

        cur.execute(
            """SELECT si.id, si.product_id, p.name, si.quantity, si.price
            FROM sale_items si
            JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = %s
            ORDER BY si.id""",
            (sale_id,)
        )
        items = cur.fetchall()
        cur.close()

        computed_total = sum(float(item[3]) * float(item[4]) for item in items)
        return {
            "sale_id": sale[0],
            "customer_id": sale[1],
            "customer_name": sale[4],
            "customer_contact": sale[5],
            "date": sale[2],
            "stored_total": float(sale[3]),
            "items": [
                {
                    "id": item[0],
                    "product_id": item[1],
                    "product_name": item[2],
                    "quantity": item[3],
                    "price": float(item[4]),
                    "line_total": round(float(item[3]) * float(item[4]), 2),
                }
                for item in items
            ],
            "computed_total": round(computed_total, 2),
        }

    @staticmethod
    def update_sale(sale_id, customer_id=None, date=None, total_amount=None):
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM sales WHERE id = %s",(sale_id,)
        )
        sale = cur.fetchone()
        if not sale:
            print(">>>>>> Sale not found!")
            cur.close()
            return
        
        update_fields = []
        if customer_id:
            update_fields.append(f"customer_id = '{customer_id}'")
        if date:
            update_fields.append(f"date = '{date}'")
        if total_amount:
            update_fields.append(f"total_amount = '{total_amount}'")
        
        sales_query = f"UPDATE sales SET {','.join(update_fields)} WHERE id = %s"
        cur.execute(sales_query,(sale_id))
        con.commit()
        cur.close()
     
    @staticmethod
    def delete_sale(sale_id):
        cur = con.cursor()
        cur.execute(
            "DELETE FROM sales WHERE id = %s",(sale_id,)
        )
        con.commit()
        cur.close() 

    @staticmethod
    def view_sales():
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM sales"
        )
        sales = cur.fetchall()
        cur.close()
        return sales

    @staticmethod
    def view_sale_id(sale_id):
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM sales WHERE id = %s",(sale_id,)
        )
        sale = cur.fetchone()
        cur.close()
        return sale

    # Analytical Queries
    @staticmethod
    def total_sales_by_date(start_date,end_date):
        cur = con.cursor()
        cur.execute(
            "SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s",(start_date,end_date)
        )
        total_sales = cur.fetchone()
        cur.close()
        return total_sales

    @staticmethod
    def get_top_selling_products():
        cur = con.cursor()
        cur.execute(
            """SELECT product_id, SUM(quantity) AS total_quantity
            FROM sale_items
            GROUP BY product_id
            ORDER BY total_quantity DESC
            LIMIT 5
            """
        )
        total_products = cur.fetchall()
        cur.close()
        return total_products
    
    @staticmethod
    def get_seles_by_customer(customer_id):
        cur = con.cursor()
        cur.execute("SELECT * FROM sales WHERE customer_id = %s",(customer_id,))
        sales = cur.fetchone()
        cur.close()
        return sales
    
    @staticmethod   
    def sale_menu():  
        while True:
            print("1. Create Table")
            print("2. Insert Sales")
            print("3. Update Sales")
            print("4. Delete Sales")
            print("5. View Sales")
            print("6. View Sales By ID")
            print("7. Generate Bill")
            print("8. Total Sale By Date")
            print("9. Top 5 Selling Products")
            print("10. Sales By Customer")
            print("0. Exit Sale")
            
            choice = input("Enter your choice: ")
            if choice == "1":
                Sales().create_table()
                print(">>>>>>> Sales Table created!")
            elif choice == "2":
                customer_id = input("Enter Customer ID: ")
                date = input("Enter sales date: ")
                total_amount = input("Enter Sales Amount: ")
                Sales().insert_sale(customer_id, date, total_amount)
                print(">>>>>>>>> Insert sale!")
            elif choice == "3":
                sale_id = input("Enter sales ID: ")
                customer_id = input("Enter Customer ID: ")
                date = input("Enter sales date: ")
                total_amount = input("Enter Sales Amount: ")
                Sales().update_sale(sale_id, customer_id, date, total_amount)
                print(">>>>>>> Sales Updated!")
            elif choice == "4":
                sale_id = input("Enter product id: ")
                Sales().delete_sale(sale_id)
                print(">>>>>>> Sales Deleted!")
            elif choice == "5":
                sales = Sales().view_sales()
                print(sales)
                print(">>>>>>> Sales Fetched!")
            elif choice == "6":
                sale_id = input("Enter Product id: ")
                sales = Sales().view_sale_id(sale_id)
                print(sales)
                print(">>>>>>> One Sales Fetched!")
            elif choice == "7":
                sale_id = input("Enter Product id: ")
                bill = Sales().generate_bill(sale_id)
                print(bill)
                print(">>>>>>> Generate Sales Bill!")
            elif choice == "8":
                start_date = input("Enter Start date: ")
                end_date = input("Enter End date: ")
                sales = Sales().total_sales_by_date(start_date, end_date)
                print(sales)
                print(">>>>>>> Total Sales!")
            elif choice == "9":
                products = Sales().get_top_selling_products()
                print(products)
                print(">>>>>>> Top 5 selling Product!")
            elif choice == "10":
                customer_id = input("Enter Customer id: ")
                customer = Sales().get_seles_by_customer(customer_id)
                print(customer)
                print(">>>>>>> Sales By Customer!")
            elif choice == "0":
                print("Exit...")
                break
            else:
                print("Invalid choice. Please try again.")
                
# Sales().sale_menu()