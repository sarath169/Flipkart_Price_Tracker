import datetime
import os


import requests
import logging
import mysql.connector
import dotenv

from bs4 import BeautifulSoup
from openpyxl import Workbook
from mysql.connector import Error
from mysql.connector import errorcode

from constants import *


def scraper(link):
    #
    laptops=[]
    log_info=[]
    for i in range(1,5):
        source = requests.get(link+str(i)).text
        soup = BeautifulSoup(source,'lxml')
        for div in soup.find_all(class_='_1fQZEK'):
            # print(div1.prettify())
            name = div.find('div',class_="_4rR01T").text
            if div.find('div',class_='_3LWZlK'):
                ratings=div.find('div',class_='_3LWZlK').text
            else:
                ratings="NA"
            list_price = div.find('div',class_="_30jeq3 _1_WHN1").text
            if div.find('div',class_='_3I9_wc _27UcVY'):
                actual_price = div.find('div',class_='_3I9_wc _27UcVY').text
            else:
                actual_price=list_price
            date_time=datetime.datetime.now()
            laptops.append([name,ratings,list_price,actual_price,date_time])
    return laptops
def inserting(laptops):
    # try:
    dotenv.load_dotenv()
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    cursor=mydb.cursor()
    n=len(laptops)
    for i in range(n):
        logging.info('executed times',i)
        name=str(laptops[i][0])
        list_price=int(laptops[i][2][1:].replace(',',''))
        date=str(laptops[i][4])
        date=date[6:16]
        cursor.execute("SELECT product_id FROM products WHERE product_name = %s",(name,))
        res=cursor.fetchone()
        pid=None
        if res:
            pid=res[0]
        query='''INSERT INTO price (listed_price,date_time, product_id) VALUES (%s,%s,%s)'''
        logging.info("person id is",pid)
        if pid:
            logging.info("in the if statement",pid)
            cursor.execute(query,(list_price,date,pid,))
            mydb.commit()
        else:
            logging.info("else block",i)
            q1="INSERT INTO products (product_name) VALUES (%s)"
            cursor.execute(q1,(name,))
            mydb.commit()
            cursor.execute("SELECT product_id FROM products WHERE product_name = %s",(name,))
            res=cursor.fetchone()
            pid=res[0]
            cursor.execute(query, (list_price,date,pid,))
            mydb.commit()
    mydb.close()
result=scraper(FLIPKART_LAPTOPS)
inserting(result)
