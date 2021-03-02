import os
import sys

import mysql.connector
import dotenv
import logging

from mailjet_rest import Client

def connection():
    dotenv.load_dotenv()
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return mydb

def alert_mail(mydb):
    cursor=mydb.cursor()
    query='''select distinct (SELECT product_name from products pro where pro.product_id=p.product_id) as prod_name, a.threshold, p.product_id, p.listed_price, p.date_time,a.user_email
from alert a join price p on a.product_id=p.product_id
where p.date_time = (select max(p2.date_time) from price p2
where p2.product_id = p.product_id); '''
    cursor.execute(query)
    data=cursor.fetchall()
    print(data)
    for i in data:
        print(i)
        prod_name=i[0]
        price=int(i[3])
        threshold=i[1]
        if price>threshold:
            print("the price is above threshold")
        else:
            api_key = os.getenv('api_key')
            api_secret = os.getenv('api_secret')
            sender_mail=os.getenv('sender_email')
            reciever_mail=i[5]
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data = {
              'Messages': [
            				{
            						"From": {
            								"Email": sender_mail,
            								"Name": "Alert"
            						},
            						"To": [
            								{
            										"Email": reciever_mail,
            										"Name": "Subscriber"
            								}
            						],
                                    "Variables":{
                                    "product_name":prod_name,
                                    "threshold":threshold,
                                    },
            						"TemplateID":2454076,
            						"TemplateLanguage": True,
            						"Subject": "Price Drop Alert"
            				}
            		]
            }
            result = mailjet.send.create(data=data)
            print(result.status_code)
            print(result.json())

def main():
    mydb=connection()
    alert_mail(mydb)

if __name__ == '__main__':
    main()
