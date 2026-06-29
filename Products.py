from Database import connection

class Products:
    
    def __init__(self):
        pass
    
    @staticmethod
    def create_table():
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                quantity INTEGER NOT NULL
            )"""
        )
        conn.commit()
        cur.close()
        conn.close()
        
    @staticmethod
    def insert_product(name,description,price,quantity):
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO products (name,description,price,quantity)
            VALUES(%s,%s,%s,%s)
            """,
            (name,description,price,quantity)
        )
        print(">>>>>>>> Insert Products!")
        conn.commit()
        cur.close()
        conn.close()
    
    @staticmethod
    def update_product(product_id, name=None, description=None, price=None, quantity=None):
        conn = connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE id = %s",(product_id,))
        product = cur.fetchone()
        
        if not product:
            print(">>>>> Product not found!")
            cur.close()
            conn.close()
            return
        
        update_field = []
        if name:
            update_field.append(f"name = '{name}'")
        if description:
            update_field.append(f"description = '{description}'")
        if price:
            update_field.append(f"price = '{price}'")
        if quantity:
            update_field.append(f"quantity = '{quantity}'") 
            
        update_query = f"UPDATE products SET {','.join(update_field)} WHERE id = %s"
        cur.execute(update_query,(product_id,))
        conn.commit()
        cur.close()
        conn.close()  
            
    @staticmethod
    def delete_product(product_id):
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM products WHERE id = %s",(product_id,)
        )
        print(">>>>>>> Product Deleted!")
        conn.commit()
        cur.close()
        conn.close()
        
    @staticmethod
    def view_product():
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM products"
        )
        products = cur.fetchall()
        cur.close()
        conn.close()
        return products
        
    @staticmethod
    def view_product_id(product_id):
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE id = %s",(product_id,)
        )
        products = cur.fetchone()
        cur.close()
        conn.close()
        return products
        
    @staticmethod   
    def product_menu():  
        while True:
            print("1. Create Table")
            print("2. Insert Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. View Product")
            print("6. View Product By ID")
            print("0. Exit Product")
                
            choice = input("Enter your choice: ")
            if choice == "1":
                Products().create_table()
                print(">>>>>>> Product Table created!")
            elif choice == "2":
                name = input("Enter name: ")
                description = input("Enter description: ")
                price = input("Enter price: ")
                quantity = input("Enter quantity: ")
                Products().insert_product(name,description,price,quantity)
            elif choice == "3":
                product_id = input("Enter customer id: ")
                name = input("Enter name: ")
                description = input("Enter description: ")
                price = input("Enter price: ")
                quantity = input("Enter quantity: ")
                Products().update_product(product_id, name,description,price,quantity)
                print(">>>>>>> Product Updated!")
            elif choice == "4":
                product_id = input("Enter product id: ")
                Products().delete_product(product_id)
            elif choice == "5":
                products = Products().view_product()
                print(products)
                print(">>>>>>> Product Fetched!")
            elif choice == "6":
                product_id = input("Enter Product id: ")
                products = Products().view_product_id()
                print(products)
                print(">>>>>>> One Product Fetched!")
            elif choice == "0":
                print("Exit...")
                break
            else:
                print("Invalid choice. Please try again.")
                    
# Products().product_menu()