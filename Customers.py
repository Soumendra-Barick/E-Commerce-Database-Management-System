from Database import connection

class Customers:
    
    def __init__(self):
        pass
        # self.name = name,
        # self.contact = contact
    
    @staticmethod
    def create_table():
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                contact VARCHAR(15) NOT NULL
            )"""
        )
        conn.commit()
        cur.close()
        conn.close()
    
    @staticmethod  
    def insert_customer(name, contact):
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO customers (name,contact)
            VALUES (%s,%s)""",(name,contact)
        )
        conn.commit()
        cur.close()
        conn.close()
    
    @staticmethod
    def update_customer(customer_id, name=None, contact=None):
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE id = %s",(customer_id,))
        customer = cur.fetchone()
        
        if not customer:
            print(">>>>>> Customer not found!")
            cur.close()
            conn.close()
            return
        
        update_fields = []
        if name:
            update_fields.append(f"name = '{name}'")
        if contact:
            update_fields.append(f"contact = '{contact}'")
            
        update_query = f"UPDATE customers SET {','.join(update_fields)} WHERE id = %s"
        cur.execute(
            update_query,(customer_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
    
    @staticmethod
    def delete_customer(customer_id):
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM customers WHERE id = %s",(customer_id,)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_all_customers():
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM customers"
        )
        customers = cur.fetchall()   
        cur.close()
        conn.close()
        return customers
     
    @staticmethod   
    def customer_menu():
    
        while True:
            print("1. Create Table")
            print("2. Insert Customer")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. View Customer")
            print("0. Exit Customer")
            
            choice = input("Enter your choice: ")
            if choice == "1":
                Customers().create_table()
                print(">>>>>>> Customer Table created!")
            elif choice == "2":
                name = input("Enter name: ")
                contact = input("Enter contact: ")
                Customers().insert_customer(name,contact)
                print(">>>>>>> Customer Inserted!")
            elif choice == "3":
                customer_id = input("Enter customer id: ")
                name = input("Enter name: ")
                contact = input("Enter contact: ")
                Customers().update_customer(customer_id, name, contact)
                print(">>>>>>> Customer Updated!")
            elif choice == "4":
                customer_id = input("Enter customer id: ")
                Customers().delete_customer(customer_id)
                print(">>>>>>> Customer Delete!")
            elif choice == "5":
                customers = Customers().get_all_customers()
                print(customers)
                print(">>>>>>> Customer Fetched!")
            elif choice == "0":
                print("Exit...")
                break
            else:
                print("Invalid choice. Please try again.")
                
# Customers().customer_menu()