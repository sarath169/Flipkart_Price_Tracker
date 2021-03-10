import os
import sys

import mysql.connector
import dotenv

def setup_db(mydb):
    cursor = mydb.cursor()
    cursor.execute('CREATE DATABASE `flipkart_laptops`')
    cursor.execute('''CREATE TABLE `products` (`product_id` INT AUTO_INCREMENT PRIMARY KEY
                                              ,`product_name` VARCHAR(255) UNIQUE)''')
    cursor.execute('''CREATE TABLE `price` (`listed_price` INT NOT NULL
                                           ,`date_time` VARCHAR(255)
                                           ,`product_id` INT
                                           ,FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`));''')
    cursor.execute('''CREATE TABLE `alert` (`user_email` VARCHAR(255) NOT NULL
                                            ,`product_id` INT NOT NULL
                                            ,`threshold` INT NOT NULL
                                            ,FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`) )''')
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
    manage_db()
