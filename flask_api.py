import os
import sys

import dotenv
import mysql.connector

from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_cors import CORS

dotenv.load_dotenv()
def connection():
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return mydb

def flask(mydb):
    cursor=mydb.cursor()
    app = Flask(__name__,template_folder='/home/sarath/Documents/Flipkart_Price_Tracker')
    CORS(app)

    @app.route('/prod_details')
    def prod_details():
        cursor.execute("SELECT * FROM products order by product_id")
        data = cursor.fetchall()
        return jsonify(data)

    @app.route('/success/')
    def success():
        cursor.execute("SELECT * FROM alert order by product_id")
        data = cursor.fetchall()
        return jsonify(data)


    @app.route('/register',methods = ['POST'])
    def register():
       if request.method == 'POST':
          email= request.form['email']
          pid=request.form['products']
          threshold=request.form['threshold']
          query='''INSERT INTO alert VALUES (%s,%s,%s)'''
          cursor.execute(query,(email,pid,threshold,))
          mydb.commit()
          return redirect(url_for('success'))
       else:
          return redirect(url_for('success'))
    return app

if __name__ == '__main__':
    mydb=connection()
    app=flask(mydb)
    app.run()
