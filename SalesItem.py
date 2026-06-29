from Database import con

class SaleItems:
    
    @staticmethod
    def create_table():
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                
                CONSTRAINT fk_sales_items_sale
                FOREIGN KEY (sale_id)
                REFERENCES sales(id)
                ON DELETE CASCADE,
                
                CONSTRAINT fk_sales_items_product
                FOREIGN KEY (product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
            )"""
        )
        con.commit()
        cur.close()

    @staticmethod
    def add_sale_item(sale_id, product_id, quantity, price):
        cur = con.cursor()
        cur.execute(
            """INSERT INTO sale_items (sale_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
            """,
            (sale_id, product_id, quantity, price)
        )
        con.commit()
        cur.close()

    @staticmethod
    def get_sale_items_by_sale(sale_id):
        cur = con.cursor()
        cur.execute("SELECT * FROM sale_items WHERE sale_id = %s", (sale_id,))
        items = cur.fetchall()
        cur.close()
        return items
        