import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='iauar'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User or password is wrong!')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `financas`;")
cursor.execute("CREATE DATABASE `financas`;")
cursor.execute("USE `financas`;")

cursor.execute("DROP USER IF EXISTS `financas`@`localhost`;")
cursor.execute("FLUSH PRIVILEGES;")
cursor.execute("CREATE USER `financas`@`localhost` IDENTIFIED BY 'fin123';")
cursor.execute("GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT on financas.* TO `financas`@`localhost` WITH GRANT OPTION;")
cursor.execute("FLUSH PRIVILEGES;")


# tables
TABLES = {}

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(20) NOT NULL,
      `nickname` varchar(10) NOT NULL,
      `password` varchar(100) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['ActiveSessions'] = ('''
CREATE TABLE `activesessions` (
      `jti` VARCHAR(36),
      `user_id` INT NOT NULL,
      `ip_address` VARCHAR(45) NOT NULL,
      `created_at` DATETIME NOT NULL,
      `expires_at` DATETIME NOT NULL,
      PRIMARY KEY (`jti`),
      FOREIGN KEY (`user_id`) REFERENCES users(`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['TokenBlocklist'] = ('''
CREATE TABLE `tokenblocklist` (
      `jti` VARCHAR(36),
      `user_id` INT NOT NULL,
      `ip_address` VARCHAR(45) NOT NULL,
      `created_at` DATETIME NOT NULL,
      `expires_at` DATETIME NOT NULL,
      `revoked_at` DATETIME NOT NULL,
      PRIMARY KEY (`jti`),
      FOREIGN KEY (`user_id`) REFERENCES users(`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for TBname in TABLES:
      TBquery = TABLES[TBname]
      try:
            print(f'Creating table {TBname}')
            cursor.execute(TBquery)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Table already exists.')
            else:
                  print(err.msg)
      else:
            print('OK\n')


# inserting users
USERquery = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
USERvalues = [
      ("Rodrigo Lopes", "Apoc", generate_password_hash("admin").decode('utf-8')),
      ("Rafael de Pilla", "Rath", generate_password_hash("admin").decode('utf-8'))
]
cursor.executemany(USERquery, USERvalues)

cursor.execute('select * from financas.users')
print(' -------------  Users List:  -------------')
for user in cursor.fetchall():
    print(user[1])

# commit
conn.commit()

cursor.close()
conn.close()
