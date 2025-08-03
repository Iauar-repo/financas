import mysql.connector
from mysql.connector import errorcode

try:
    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="admin")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User or password is wrong!")
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `financas`;")
cursor.execute("CREATE DATABASE `financas`;")
cursor.execute("USE `financas`;")

cursor.execute("DROP USER IF EXISTS `financas`@`localhost`;")
cursor.execute("FLUSH PRIVILEGES;")
cursor.execute("CREATE USER `financas`@`localhost` IDENTIFIED BY 'fin123';")
cursor.execute(
    "GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, INDEX, REFERENCES on financas.* TO `financas`@`localhost`;"
)
cursor.execute("FLUSH PRIVILEGES;")

cursor.close()
conn.close()