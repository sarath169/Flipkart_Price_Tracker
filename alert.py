import os
import sys

import mysql.connector
import smtplib, ssl
import dotenv
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def connection():
    dotenv.load_dotenv()
    sql = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return sql
def send_email (admin, pwd, user, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(admin, pwd)
        server.sendmail(admin, user, message)
        server.close()
        return True

def alert_mail(sql):
    cursor=sql.cursor()
    query='''select distinct (SELECT product_name from products pro where pro.product_id=p.product_id) as prod_name, a.threshold, p.product_id, p.listed_price, p.date_time,a.user_email
from alert a join price p on a.product_id=p.product_id
where p.date_time = (select max(p2.date_time) from price p2
where p2.product_id = p.product_id); '''
    cursor.execute(query)
    data=cursor.fetchall()
    print(data)
    for i in data:
        print(i)
        price=int(i[3])
        threshold=i[1]
        if price>threshold:
            print("the price is above threshold")
        else:
            sender_email =  os.getenv('sender_email')
            print("sender",sender_email)
            receiver_email = i[5]
            print("receiver",i[5])
            pwd = os.getenv('email_pwd')
            msg = """\
            Subject: "Price Drop Alert"

            The price of the product
             """+ i[0]+'is priced at '+i[3]+' please have a look if interested.'

            print(send_email(sender_email, pwd, receiver_email, msg))
def main():

    sql=connection()
    alert_mail(sql)

if __name__ == '__main__':
    main()
