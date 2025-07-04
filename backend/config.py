SECRET_KEY='devadmin'

SGBD='mysql+mysqlconnector'
DBUSER='financas'
DBPASS='fin123'
DBNAME='financas'

SQLALCHEMY_DATABASE_URI=f'{SGBD}://{DBUSER}:{DBPASS}@localhost/{DBNAME}'