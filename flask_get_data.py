import os
import sys

import dotenv
import mysql.connector

from flask import Flask, request, render_template

dotenv.load_dotenv()
mydb = mysql.connector.connect(
host=os.getenv('mysql_host'),
user=os.getenv('mysql_user'),
password=os.getenv('db_pwd'),
database=os.getenv('db')
)
cursor=mydb.cursor()
app = Flask(__name__,template_folder='Flipkart_Price_Tracker')

@app.route('/')
def index():
    return render_template('/home/sarath/Documents/Flipkart_Price_Tracker/index.html')
@app.route('/prod_details')
def prod_details():
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    return render_template('prod_details.html', data=data)

if __name__ == '__main__':
   app.run()
