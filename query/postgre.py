import psycopg2
from psycopg2 import sql
import pandas as pd
import csv

def Info(*args):
    print('\033[93m' + ' '.join([str(arg) for arg in args]) + '\033[0m')

if __name__ == '__main__':
    import os
    Info("Starting Postgresql service...")
    os.system("service postgresql start")
    Info("Postgres started")

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS commodities (
            commodity_code VARCHAR PRIMARY KEY,
            commodity_name VARCHAR(255),
            type_gauge TEXT,
            class_name VARCHAR(255),
            class_code VARCHAR(50),
            commodity_specific JSONB
        )
    """)

    cur.execute("""
    CREATE TEMP TABLE temp_commodities (LIKE commodities);
""")
    
    with open('data/commodity.csv', 'r') as f:
        cur.copy_expert("COPY temp_commodities FROM STDIN WITH CSV HEADER", f)

    Info("Data loaded")
    # with open('data/commodity.csv', 'r', encoding='utf-8') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # 跳过标题行
    #     for row in reader:
    #         cur.execute("""
    #             INSERT INTO commodities (commodity_code, commodity_name, type_gauge, class_name, class_code, commodity_specific)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #             ON CONFLICT (commodity_code) DO NOTHING
    #         """, row)