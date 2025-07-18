import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash
from datetime import datetime, timezone

try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
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
      `name` varchar(60) NOT NULL,
      `email` varchar(320) NOT NULL,
      `username` varchar(40) NOT NULL,
      `password` varchar(60) NOT NULL,
      `is_admin` int NOT NULL,
      `email_confirmed` int NOT NULL,
      `created_at` DATETIME NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE (`username`),
      UNIQUE (`email`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['ActiveSessions'] = ('''
CREATE TABLE `activesessions` (
      `jti` VARCHAR(36),
      `user_id` INT NOT NULL,
      `ip_address` VARCHAR(15) NOT NULL,
      `created_at` DATETIME NOT NULL,
      `expires_at` DATETIME NOT NULL,
      PRIMARY KEY (`jti`),
      FOREIGN KEY (`user_id`) REFERENCES users(`id`) ON DELETE CASCADE
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['TokenBlocklist'] = ('''
CREATE TABLE `tokenblocklist` (
      `jti` VARCHAR(36),
      `user_id` INT NOT NULL,
      `ip_address` VARCHAR(15) NOT NULL,
      `created_at` DATETIME NOT NULL,
      `expires_at` DATETIME NOT NULL,
      `revoked_at` DATETIME NOT NULL,
      PRIMARY KEY (`jti`),
      FOREIGN KEY (`user_id`) REFERENCES users(`id`) ON DELETE CASCADE
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
USERquery = 'INSERT INTO users (name, email, username, password, is_admin, created_at, email_confirmed) VALUES (%s, %s, %s, %s, %s, %s, %s)'
USERvalues = [
      (
            "Rodrigo Lopes",
            "123@gmail.com",
            "Apoc",
            generate_password_hash("admin").decode('utf-8'),
            1,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      ),
      (
            "Rafael de Pilla",
            "rrmontebello@gmail.com",
            "Rath",
            generate_password_hash("admin").decode('utf-8'),
            1,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      ),
      (
            "User 1",
            "user1@gmail.com",
            "user1",
            generate_password_hash("user1").decode('utf-8'),
            0,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      ),
      (
            "User 2",
            "user2@gmail.com",
            "user2",
            generate_password_hash("user2").decode('utf-8'),
            0,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      ),
      (
            "User 3",
            "user3@gmail.com",
            "user3",
            generate_password_hash("user3").decode('utf-8'),
            0,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      ),
      (
            "User 4",
            "user4@gmail.com",
            "user4",
            generate_password_hash("user4").decode('utf-8'),
            0,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      ),
      (
            "User 5",
            "user5@gmail.com",
            "user5",
            generate_password_hash("user5").decode('utf-8'),
            0,
            datetime.now(timezone.utc).replace(tzinfo=None),
            1
      )
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
