import os
import sys

import mysql.connector
import dotenv

def setup_db(mydb):
    cursor = mydb.cursor()
    cursor.execute('create database flipkart_laptops')
    cursor.execute('''CREATE TABLE products (product_id INT AUTO_INCREMENT PRIMARY KEY
                                              ,product_name VARCHAR(255) UNIQUE)''')
    cursor.execute('''CREATE TABLE price (listed_price INT NOT NULL
                                           ,date_time VARCHAR(255)
                                           ,product_id INT
                                           ,FOREIGN KEY (product_id) REFERENCES products(product_id));''')
    cursor.execute('''create table alert (user_email VARCHAR(255) not null
                                            ,product_id INT not null
                                            ,threshold int not null
                                            ,FOREIGN KEY (product_id) REFERENCES products(product_id) )''')
def manage_db():
    dotenv.load_dotenv()
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    setup_db(mydb)

if __name__ == '__main__':
    '''main function'''
    manage_db()
