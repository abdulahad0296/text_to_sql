import sqlite3
def read_sql_query(sql,db):
    connn=sqlite3.connect(db)
    cur=connn.cursor()
    cur.execute(sql)

    #retrieving column names
    column=[description[0] for description in cur.description] 
    rows=cur.fetchall()

    connn.commit()
    connn.close()

    for i in rows:
        print(i)
    return column,rows