import psycopg2,os
from dotenv import load_dotenv

load_dotenv()

dbname= os.getenv("DB_NAME")
user= os.getenv("DB_USER")
password= os.getenv("DB_PASSWORD")
host= os.getenv("DB_HOST")
port= os.getenv("DB_PORT")

def get_connection():
    return psycopg2.connect(
        dbname = dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

conn = get_connection()
cursor = conn.cursor()
print("Conectado com sucesso!")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidosclientes (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    produto VARCHAR(100) NOT NULL,
    data TIMESTAMP NOT NULL,
    entregue BOOLEAN NOT NULL DEFAULT FALSE
);
""")

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS pagamentos (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    montante NUMERIC(15,2) NOT NULL,
    pago BOOLEAN NOT NULL DEFAULT FALSE
    )
""")

conn.commit()
