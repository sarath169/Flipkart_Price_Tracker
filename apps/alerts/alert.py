import os
import sys

import mysql.connector
import dotenv
import logging

from mailjet_rest import Client
from twilio.rest import Client as smsClient

def connection():
    dotenv.load_dotenv()
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return mydb
def update_db(mydb):
    cursor=mydb.cursor()
    query='''UPDATE `alert` SET `alert_sent`=1 WHERE `alert_sent`= 0'''
    cursor.execute(query)
    mydb.commit()

def alert_mail(mydb):
    cursor=mydb.cursor()
    query='''SELECT DISTINCT (SELECT `product_name` FROM `products` pro WHERE pro.product_id = p.product_id) AS prod_name, a.threshold, p.product_id, p.listed_price, p.date_time,a.user_email,a.phone_number,a.alert_sent
            FROM `alert` a JOIN `price` p ON a.product_id = p.product_id
            WHERE p.date_time = (SELECT MAX(p2.date_time) FROM `price` p2
            WHERE p2.product_id = p.product_id); '''
    cursor.execute(query)
    data=cursor.fetchall()
    # print(data)
    for i in data:
        prod_name=i[0]
        price=int(i[3])
        threshold=i[1]
        # print("alert_sent",i[7])
        if price > threshold or i[7]:
            # print("the price is above threshold or the alert is already sent")
        else:
            if i[5]:
                api_key = os.getenv('mailjet_api_key')
                api_secret = os.getenv('mailjet_api_secret')
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
                # print(result.status_code)
                # print(result.json())
            if i[6]:
                # and set the environment variables. See http://twil.io/secure
                account_sid = os.getenv('account_sid')
                auth_token = os.getenv('auth_token')
                client = smsClient(account_sid, auth_token)

                message = client.messages \
                                .create(
                                     body="The Product "+i[0]+" is below "+str(i[1])+" and the current price is "+str(i[3]),
                                     from_='+13126266504',
                                     to='+91 '+i[6]
                                 )

                # print(message.sid)
            if i[5] and i[6]:
                account_sid = os.getenv('account_sid')
                auth_token = os.getenv('auth_token')
                client = smsClient(account_sid, auth_token)

                message = client.messages \
                                .create(
                                     body="The Product "+i[0]+" is below "+str(i[1])+" and the current price is "+str(i[3]),
                                     from_='+13126266504',
                                     to='+91 '+i[6]
                                 )

                # print(message.sid)
                api_key = os.getenv('mailjet_api_key')
                api_secret = os.getenv('mailjet_api_secret')
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
                # print(result.status_code)
                # print(result.json())



def alert():
    mydb = connection()
    alert_mail(mydb)
    update_db(mydb)

if __name__ == '__main__':
    alert()
