import psycopg2
import psycopg2.extras
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

        with open('data/commodity.csv', 'r') as f:
            cur.copy_expert("COPY commodities FROM STDIN WITH CSV HEADER", f)
        
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

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("DROP TABLE IF EXISTS commodities;")

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
    "技术属性要求": {"内径": input('内径: '), "外径": input('外径: '), "宽度": input('宽度: ')}
    }


    # 筛选
    Info("Querying...")

    sql = """
    SELECT * FROM commodities
    WHERE CLASS_NAME LIKE %s
    AND EXISTS (
        SELECT 1
        FROM jsonb_array_elements(commodity_specific) AS cs(item)
        WHERE (item->>'paramName' = '内径' AND item->>'paramValue' = %s)
    AND EXISTS (
        SELECT 1
        FROM jsonb_array_elements(commodity_specific) AS cs(item)
        WHERE (item->>'paramName' = '外径' AND item->>'paramValue' = %s)
    )
    AND EXISTS (
        SELECT 1
        FROM jsonb_array_elements(commodity_specific) AS cs(item)
        WHERE (item->>'paramName' = '宽度' AND item->>'paramValue' = %s)
    );
    """
    cur.execute(sql, (query["品类要求"], query["技术属性要求"]["内径"], query["技术属性要求"]["外径"], query["技术属性要求"]["宽度"]))
    # cur.execute(sql, ('%' + query["品类要求"] + '%', query["技术属性要求"]["内径"], query["技术属性要求"]["外径"]))

    # 获取满足品类要求的所有记录中前3条记录
    results = cur.fetchall()
    results = results[:3]
    print(results)





    cur.close()
    conn.close()