import mysql.connector as mysql
from .. import config
from .. import logger
from mysql.connector.pooling import MySQLConnection
from mysql.connector.cursor import MySQLCursor
logger = logger.getLogger(__name__)

def connect() -> MySQLCursor:
    mysql_connection: MySQLConnection = mysql.connect(user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST, port=config.DB_PORT, database='prueba')
    logger.debug("MySQL connected successfully!")
    return mysql_connection

