import sqlite3
def init_db():
    conn=sqlite3.connect("customers.db")
    cursor=conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
                   InvoiceNo TEXT,
                   StockCode TEXT,
                   Description TEXT,
                   Quantity INTEGER,
                   InvoiceDate TEXT,
                   UnitPrice TEXT,
                   CustomerID TEXT,
                   Country TEXT
                   )
                   """)
    conn.commit()
    conn.close()