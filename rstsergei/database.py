from flask_mysqldb import MySQL
import MySQLdb.cursors

MYSQL_HOST = 'mysql'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'begemot'
MYSQL_CURSORCLASS = 'DictCursor'

mysql = MySQL()
