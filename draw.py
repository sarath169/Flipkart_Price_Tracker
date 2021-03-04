import os
import sys

import mysql.connector
import matplotlib.pyplot as plt
import dotenv
import logging

dotenv.load_dotenv()

def product_id_input(sql,pid):
    cursor=sql.cursor()
    logging.info("connection is done")
    query ='''select * from price where product_id = %s'''
    cursor.execute(query,(pid,))
    data=cursor.fetchall()
    return data

def connection():
    sql = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return sql

def main():
    pid = sys.argv[1]
    sql=connection()
    result = product_id_input(sql,pid)
    price=[result[0][0]]
    datetime=[result[0][1]]
    for i in range(1,len(result)):
        if result[i][0]!=result[i-1][0]:
            price.append(result[i][0])
            datetime.append(result[i][1])
    plt.plot( datetime,price)
    plt.xlabel('Datetime')
    plt.ylabel('Price')
    plt.xticks(rotation = 0)
    plt.show()

if __name__ == '__main__':
    main()
