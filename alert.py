import os
import sys

import mysql.connector
import smtplib, ssl
import dotenv
import logging



def connection():
    dotenv.load_dotenv()
    sql = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return sql

def alert_mail(sql):
    cursor=sql.cursor()
    query="select user_email from alert"
    cursor.execute(query)
    emails=cursor.fetchall()
    for i in emails:
        print(i)
        query="select product_id,threshold from alert where user_email=%s"
        cursor.execute(query,i)
        info=cursor.fetchall()
        for j in info:
            pid=(j[0])
            threshold=(j[1])
            q='''select listed_price from price where product_id=1 '''
            cursor.execute(q)
            result=cursor.fetchone()
            print(result[0])
            req_price=int(result[0])
            if req_price>threshold:
                continue
            else:
                sender_email =  os.getenv('sender_email')
                receiver_email = i[0]
                pwd = os.getenv('email_pwd')
                port=465
                smtp_server = "smtp.gmail.com"
                sender_email = sender_email  # Enter your address
                receiver_email = receiver_email # Enter receiver address
                password = pwd
                message = """\
                Subject: "Price Drop alert"

                there is a price drop in the product your are intrested in."""
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)

def main():

    sql=connection()
    alert_mail(sql)

if __name__ == '__main__':
    main()
