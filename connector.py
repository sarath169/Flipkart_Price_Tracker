import mysql.connector

mysql = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mindfire#12",
  database="flipkart_laptops"
)
cursor=mysql.cursor()
# cursor.execute('create database flipkart_laptops')
# cursor.execute('''CREATE TABLE products (product_id INT AUTO_INCREMENT PRIMARY KEY
#                                           ,product_name VARCHAR(255) UNIQUE)''')
# cursor.execute('''CREATE TABLE price (listed_price VARCHAR(255) NOT NULL
#                                        ,date_time VARCHAR(255)
#                                        ,product_id INT
#                                        ,FOREIGN KEY (product_id) REFERENCES products(product_id));''')
cursor.execute("SHOW TABLES")
for x in cursor:
    print(x)
#
cursor.execute("select * from price where product_id is not NULL order by product_id")
k=cursor.fetchall()
for i in k:
    print(i)
# query='INSERT INTO products (product_name) VALUES (%s)'
# val=[("Avita Pura Ryzen 5 Quad Core 3500U  (8 GB/512 GB SSD/Windows 10 Home in S Mode) NS14A6INV561-SHGYB Th...",)
#     ,('HP 14 Core i5 10th Gen - (8 GB/512 GB SSD/Windows 10 Home) 14-ck2018TU Thin and Light Laptop',)
#     ,("HP 15s Celeron Dual Core - (4 GB/1 TB HDD/Windows 10 Home) 15s-du1044tu Thin and Light Laptop",)
#     ]
# name='HP 14 Core i5 10th Gen - (8 GB/512 GB SSD/Windows 10 Home) 14-ck2018TU Thin and Light Laptop'
# cursor.executemany(query,val)

# q='''drop table products'''
# cursor.execute(q)


# res=cursor.fetchall()
# for x in res:
#     print(x)
mysql.commit()
mysql.close()
