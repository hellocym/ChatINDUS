import psycopg2
import psycopg2.extras
from psycopg2 import sql
import pandas as pd
import csv
import os
import json

current_script_path = os.path.abspath(__file__)

# 获取当前脚本所在目录的路径
current_dir = os.path.dirname(current_script_path)

# 构建commodity.csv文件的绝对路径
commodity_csv_path = os.path.join(current_dir, 'data', 'commodity.csv')


class Postgre:
    def __init__(self):
        os.system("service postgresql start")
        print("Postgres started")
        # delay 5s
        os.system("sleep 3")
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.cur.execute("DROP TABLE IF EXISTS commodities;")

        # 如果没有表则创建表
        table_name = 'commodities'
        self.cur.execute("SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = %s);", (table_name,))
        table_exists = self.cur.fetchone()[0]
        if not table_exists:
            self.load_data()

    def load_data(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS commodities (
                commodity_code VARCHAR PRIMARY KEY,
                commodity_name VARCHAR(255),
                type_gauge TEXT,
                class_name VARCHAR(255),
                class_code VARCHAR(50),
                commodity_specific JSONB
            )
        """)

        with open(commodity_csv_path, 'r') as f:
            self.cur.copy_expert("COPY commodities FROM STDIN WITH CSV HEADER", f)
        
        self.conn.commit()  # 提交更改

    def query(self, query: dict):
        # query = {"品类要求": xxx, "技术属性要求": {xxx: xxx, xxx: xxx, xxx: xxx, xxx: xxx}}
        # 有时候技术属性要求会出现未知，所以要判断是否存在
        # 筛选
        # convert query to dict
        class_name = query["品类要求"]
        param_dict = query["技术属性要求"]
        param_dict = {k: v for k, v in param_dict.items() if v!="未知"}
        sql_query = f"""
            SELECT * FROM commodities
            WHERE CLASS_NAME LIKE '%{class_name}%'
        """
        for k, v in param_dict.items():
            # 去除单位
            v = v.split(' ')[0]
            sql_query += f"""
                AND EXISTS (
                    SELECT 1
                    FROM jsonb_array_elements(commodity_specific) AS cs(item)
                    WHERE item->>'paramName' = '{k}' AND item->>'paramValue' = '{v}'
                )
        """
        sql_query += ";"
        
        self.cur.execute(sql_query)
        # self.cur.execute("""
        #     SELECT * FROM commodities
        #     WHERE CLASS_NAME LIKE %s
        #     AND EXISTS (
        #         SELECT 1
        #         FROM jsonb_array_elements(commodity_specific) AS cs(item)
        #         WHERE item->>'paramName' = '内径' AND item->>'paramValue' = %s
        #     )
        #     AND EXISTS (
        #         SELECT 1
        #         FROM jsonb_array_elements(commodity_specific) AS cs(item)
        #         WHERE item->>'paramName' = '外径' AND item->>'paramValue' = %s
        #     )
        #     AND EXISTS (
        #         SELECT 1
        #         FROM jsonb_array_elements(commodity_specific) AS cs(item)
        #         WHERE item->>'paramName' = '宽度' AND item->>'paramValue' = %s
        #     );
        # """, ('%' + query["品类要求"] + '%', query["技术属性要求"]["内径"], query["技术属性要求"]["外径"], query["技术属性要求"]["宽度"]))
        # cur.execute(sql, ('%' + query["品类要求"] + '%', query["技术属性要求"]["内径"], query["技术属性要求"]["外径"]))
        # for result in self.cur.fetchall():
        #     print(result)
        skus = self.cur.fetchall()
        # 返回所有COMMODITY_CODE
        return [sku['commodity_code'] for sku in skus]




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
        

        with open(commodity_csv_path, 'r') as f:
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
    "品类要求": input('品类要求: '),
    "技术属性要求": {"内径": input('内径: '), "外径": input('外径: '), "宽度": input('宽度: ')}
    }


    # 筛选
    Info("Querying...")

    cur.execute("""
        SELECT * FROM commodities
        WHERE CLASS_NAME LIKE %s
        AND EXISTS (
            SELECT 1
            FROM jsonb_array_elements(commodity_specific) AS cs(item)
            WHERE item->>'paramName' = '内径' AND item->>'paramValue' = %s
        )
        AND EXISTS (
            SELECT 1
            FROM jsonb_array_elements(commodity_specific) AS cs(item)
            WHERE item->>'paramName' = '外径' AND item->>'paramValue' = %s
        )
        AND EXISTS (
            SELECT 1
            FROM jsonb_array_elements(commodity_specific) AS cs(item)
            WHERE item->>'paramName' = '宽度' AND item->>'paramValue' = %s
        );
    """, ('%' + query["品类要求"] + '%', query["技术属性要求"]["内径"], query["技术属性要求"]["外径"], query["技术属性要求"]["宽度"]))
    # cur.execute(sql, ('%' + query["品类要求"] + '%', query["技术属性要求"]["内径"], query["技术属性要求"]["外径"]))

    # cur.execute("""
    #     SELECT * FROM commodities
    #     WHERE CLASS_NAME LIKE %s;
    # """, ('%' + query["品类要求"] + '%',))  



    # 获取满足品类要求的所有记录中前3条记录
    results = cur.fetchall()
    results = results[:3]
    for result in results:
        print(result)





    cur.close()
    conn.close()