import uvicorn
from fastapi import FastAPI
from .routes import example
import src.config
from src import repository as mysql
from mysql.connector.pooling import MySQLConnection
from mysql.connector.cursor import MySQLCursor

connection: MySQLConnection = mysql.connect()
cursor: MySQLCursor = connection.cursor()
cursor.execute("Select * from users")
result = cursor.fetchall()
for x in result:
    print(x)

app = FastAPI()
app.include_router(example.router, prefix="/example")
