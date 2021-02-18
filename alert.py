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
                password = os.getenv('email_pwd')
                port=465
                message = MIMEMultipart("alternative")
                message["Subject"] = "Price Drop Alert"
                message["From"] = sender_email
                message["To"] = receiver_email

                # Create the plain-text and HTML version of your message
                text = """\
                Hi,
                How are you?
                Real Python has many great tutorials:
                www.realpython.com"""
                html = """\
                <html>
                  <body>
                    <p>Hi,<br>
                       Hope you are doing well<br>
                       The product which you are intrested is below the threshold.
                    </p>
                  </body>
                </html>
                """

                # Turn these into plain/html MIMEText objects
                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                message.attach(part1)
                message.attach(part2)

                # Create secure connection with server and send email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, message.as_string()
                    )

def main():

    sql=connection()
    alert_mail(sql)

if __name__ == '__main__':
    main()
