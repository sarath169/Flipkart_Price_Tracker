import datetime

import requests
import logging
import mysql.connector

from bs4 import BeautifulSoup
from openpyxl import Workbook
from mysql.connector import Error
from mysql.connector import errorcode

from Constants import *


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
    sql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mindfire#12",
    database="flipkart_laptops"
    )
    cursor=sql.cursor()
    n=len(laptops)
    for i in range(n):
        logging.info('executed times',i)
        name=str(laptops[i][0])
        list_price=str(laptops[i][2])
        date=str(laptops[i][4])
        cursor.execute("SELECT product_id FROM products WHERE product_name = %s",(name,))
        res=cursor.fetchone()
        pid=None
        if res:
            pid=res[0]
        query='''insert into price (listed_price,date_time, product_id) values (%s,%s,%s)'''
        logging.info("person id is",pid)
        if pid:
            logging.info("in the if statement",pid)
            cursor.execute(query,(list_price,date,pid,))
            sql.commit()
        else:
            logging.info("else block",i)
            q1="insert into products (product_name) values (%s)"
            cursor.execute(q1,(name,))
            sql.commit()
            cursor.execute("SELECT product_id FROM products WHERE product_name = %s",(name,))
            res=cursor.fetchone()
            pid=res[0]
            cursor.execute(query, (list_price,date,pid,))
            sql.commit()
    sql.close()
    # except mysql.connector.Error as error:
    #     print("Failed to insert record into Laptop table, Error is: {}".format(error))

        # query='''IF EXISTS (cursor.execute("SELECT * FROM products WHERE product_name = %s",(name,)))
        #         BEGIN
        #         cursor.execute("insert into price (listed_price, date_time, product_id) values (%s, %s, %s)",
        #         (list_price,date,pid,)    #         );
        #         END
        #         ELSE
        #         BEGIN
        #             cursor.execute("insert into products (product_name) values (%s)",
        #             (name,)
        #             );
        #             cursor.execute("insert into price (listed_price, date_time, product_id) values (%d, %s, %d)",
        #             (laptops[i][2],"laptops[i][4]",(select product_id from products where product_name=laptops[i][0]),)
        #             )
        #         END'''
# def log_to_xlsx(laptops):
#     #
#     log_records=[]
#     for i in laptops:
#         log_records.append(i)
#         logging.info(i)
#     wb_log=Workbook()
#     ws_log=wb_log.active
#     ws_log['A1']='Log_Info'
#     for logs in log_records:
#         ws_log.append(logs)
#     wb_log.save("Logging Report.xlsx")
#     return 0

# def data_to_xlsx(laptops):
#     wb=Workbook()
#     # grab the active worksheet
#     ws = wb.active
#     # Data can be assigned directly to cells
#     ws['A1'] = 'Name'
#     ws['B1'] = 'Ratings'
#     ws['C1'] = 'Listing Price'
#     ws['D1'] = 'Actual Price'
#     ws['E1'] = 'Date and Time'
#     # Rows can also be appended
#     for i in laptops:
#         ws.append(i)
#     # Python types will automatically be converted
#     # Save the file
#     d=datetime.datetime.now()
#     wb.save("laptops_list_"+str(d)+".xlsx")
#     return 0
result=scraper(FLIPKART_LAPTOPS)
inserting(result)

# data_to_xlsx(result)
