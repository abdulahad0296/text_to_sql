import pandas as pd 
import sqlite3
from sql import init_db

def load_file_to_db(csv_file):
    df=pd.read_csv(csv_file,encoding='ISO-8859-1')

    #While exploring the csv file, we found 1454 null values in Description column and 135080 missing values in CustomerID column
    #So we will drop the rows with missing CustomerID and fill Unknown product at places with missing description

    df = df.dropna(subset=["CustomerID"])
    fill_values={"Description":"Unknown Product"}
    df=df.fillna(value=fill_values)

    #Convert InvoiceDate to DateTime 
    df["InvoiceDate"]=pd.to_datetime(df["InvoiceDate"])

    #Convert CustomerId from float to string 
    df["CustomerID"]=df["CustomerID"].astype(str)

    #Initializing Database and inserting into SQLite
    init_db()
    conn=sqlite3.connect("customers.db")
    df.to_sql("transactions",conn,if_exists="replace", index=False)
    conn.close()

    print("\n Data Insertion Successfull !!!")


if __name__=="__main__":
    init_db()
    load_file_to_db("OnlineRetail.csv")