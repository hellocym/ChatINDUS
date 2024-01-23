# given query json, search for the query in data/commodity.csv
# return the result in json format
# use gradio for demo

import pandas as pd
import numpy as np
import json
import re
import os
import gradio as gr

os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

query = '{"品类要求": "深沟球轴承","技术属性要求": {"内径": "25 mm","外径": "62 mm","宽度": "17 mm","列数": "1 列"}}'
query = json.loads(query)

def search(query):
    # load data
    df = pd.read_csv('../data/commodity.csv', encoding='utf-8')
    df = df.fillna('')
    # df = df.astype(str)
    return df
    # search
    CLASS_NAME = query['品类要求']
    # if CLASS_NAME in df 'CLASS_NAME' column
    result = df[df['CLASS_NAME'].str.contains(CLASS_NAME)]
    return result


df = pd.read_csv('../data/commodity.csv', encoding='utf-8', low_memory=False)
df = df.fillna('')


def filter_records(name):
    print(name)
    return df[df["COMMODITY_NAME"].str.contains(name)]



demo = gr.Interface(
    filter_records,
    [
        # gr.Dataframe(
        #     value=df[:10]
        # ),
        gr.Textbox()
    ],
    "dataframe",
)

if __name__ == "__main__":
    demo.launch()
