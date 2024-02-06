import psycopg2
from psycopg2 import sql
import pandas as pd
import csv

if __name__ == '__main__':
    import os
    os.system("service postgresql start")
    print("Postgres started")

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS commodities (
    #         commodity_code BIGINT PRIMARY KEY,
    #         commodity_name VARCHAR(255),
    #         type_gauge VARCHAR(255),
    #         class_name VARCHAR(255),
    #         class_code VARCHAR(255),
    #         commodity_specific JSON
    #     )
    # """)

    # with open('data/commodity.csv', 'r', encoding='utf-8') as file:
    #     reader = csv.reader(file)
    #     next(reader)  # 跳过标题行
    #     for row in reader:
    #         cur.execute("""
    #             INSERT INTO commodities (commodity_code, commodity_name, type_gauge, class_name, class_code, commodity_specific)
    #             VALUES (%s, %s, %s, %s, %s, %s)
    #             ON CONFLICT (commodity_code) DO NOTHING
    #         """, row)