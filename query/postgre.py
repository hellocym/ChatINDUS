import psycopg2
from psycopg2 import sql
import pandas as pd
import csv

def Info(*args):
    print('\033[93m' + ' '.join([str(arg) for arg in args]) + '\033[0m')

def load_data():
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
        CREATE TEMP TABLE IF NOT EXISTS temp_commodities (LIKE commodities);
    """)
        
        with open('data/commodity.csv', 'r') as f:
            cur.copy_expert("COPY temp_commodities FROM STDIN WITH CSV HEADER", f)

        conn.commit()  # 提交更改


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

    # 如果没有表则创建表
    table_name = 'commodities'
    cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = %s);", (table_name,))
    table_exists = cur.fetchone()[0]
    if not table_exists:
        Info("Start loading data...")
        load_data()

    Info("Data loaded")

    query = {
    "品类要求": "滚动轴承",
    "技术属性要求": {"内径": "35", "外径": "80", "宽度": "21"}
    }

    Info("Querying class...")
    sql = """
    SELECT * FROM commodities
    WHERE CLASS_NAME LIKE %s
    """
    cur.execute(sql, ('%' + query["品类要求"] + '%',))

    # 获取满足品类要求的所有记录
    results = cur.fetchall()
    print(results)
    
    cur.close()
    conn.close()