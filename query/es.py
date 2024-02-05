from elasticsearch_dsl import connections, Index, Document, Integer, Keyword, Text, Nested
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd


# example data
# COMMODITY_CODE,COMMODITY_NAME,TYPE_GAUGE,CLASS_NAME,CLASS_CODE,COMMODITY_SPECIFIC
# 200623463928171,瓦轴 ZWZ 深沟球轴承 61040X1M,61040X1M,轴承-滚动轴承-单列深沟球轴承,L130101,"[{""unit"": ""10"", ""modelCode"": ""SX0750"", ""paramName"": ""内径"", ""ifSaleMode"": 1, ""paramValue"": ""200"", ""commodityCode"": ""200623463928171""}, {""unit"": ""10"", ""modelCode"": ""SX0764"", ""paramName"": ""外径"", ""ifSaleMode"": 1, ""paramValue"": ""269.5"", ""commodityCode"": ""200623463928171""}, {""unit"": ""10"", ""modelCode"": ""SX0008"", ""paramName"": ""宽度"", ""ifSaleMode"": 1, ""paramValue"": ""51"", ""commodityCode"": ""200623463928171""}, {""unit"": ""10"", ""modelCode"": ""SX0723"", ""paramName"": ""列数"", ""ifSaleMode"": 1, ""paramValue"": ""1"", ""commodityCode"": ""200623463928171""}, {""unit"": ""10"", ""modelCode"": ""SX1634"", ""paramName"": ""基本额定动载"", ""ifSaleMode"": 1, ""paramValue"": ""91"", ""commodityCode"": ""200623463928171""}, {""unit"": ""10"", ""modelCode"": ""SX1635"", ""paramName"": ""基本额定静载"", ""ifSaleMode"": 1, ""paramValue"": ""109"", ""commodityCode"": ""200623463928171""}, {""modelCode"": ""SX0002"", ""paramName"": ""材质"", ""ifSaleMode"": 1, ""paramValue"": ""10"", ""commodityCode"": ""200623463928171""}, {""modelCode"": ""SX0733"", ""paramName"": ""保持架材质"", ""ifSaleMode"": 1, ""paramValue"": ""20"", ""commodityCode"": ""200623463928171""}, {""modelCode"": ""SX1085"", ""paramName"": ""精度等级"", ""ifSaleMode"": 1, ""paramValue"": ""20"", ""commodityCode"": ""200623463928171""}]"

# while querying, we need to search in the following columns:
# COMMODITY_NAME, CLASS_NAME, COMMODITY_SPECIFIC

# example query
# {
#     "品类要求": "深沟球轴承",
#     "技术属性要求": {
#         "内径": "25 mm",
#         "外径": "62 mm",
#         "宽度": "17 mm",
#         "列数": "1 列"
#     }
# }

# example result
# {
#     "COMMODITY_CODE": "200623463928171",
# }

# class Commodity(Document):
#     COMMODITY_CODE = Keyword()
#     COMMODITY_NAME = Text()
#     TYPE_GAUGE = Keyword()
#     CLASS_NAME = Text()
#     CLASS_CODE = Keyword()
#     # COMMODITY_SPECIFIC = Nested(
#     #     properties={
#     #         'paramName': Keyword(),
#     #         'paramValue': Keyword(),
#     #     }
#     # )

#     class Index:
#         name = 'commodities'

connections.create_connection(hosts=['http://localhost:9200'], timeout=60)
print('\033[93m' + 'Connected to ES' + '\033[0m')


if Index('commodities').exists():
    Index('commodities').delete()

Commodity.init()
print('\033[93m' + 'DB Initialized' + '\033[0m')

print('\033[93m' + 'Loading Data...' + '\033[0m')
df = pd.read_csv('data/commodity.csv', encoding='utf-8', low_memory=False)
df = df.fillna('')
print('\033[93m' + 'Data Loaded' + '\033[0m')

# def bulk_indexing(df):
#     for index, row in df.iterrows():
#         COMMODITY_SPECIFIC_str = row['COMMODITY_SPECIFIC']
#         COMMODITY_SPECIFIC_nested = []
#         if COMMODITY_SPECIFIC_str != '':
#             COMMODITY_SPECIFIC_list = 0(COMMODITY_SPECIFIC_str)
#             for COMMODITY_SPECIFIC in COMMODITY_SPECIFIC_list:
#                 if COMMODITY_SPECIFIC['paramName'] != '' and COMMODITY_SPECIFIC['paramValue'] != '':
#                     COMMODITY_SPECIFIC_nested.append(
#                         {
#                             'paramName': COMMODITY_SPECIFIC['paramName'],
#                             'paramValue': COMMODITY_SPECIFIC['paramValue'],
#                         }
#                 )
#         print(COMMODITY_SPECIFIC_nested)
#         yield {
#             '_index': 'commodities',
#             '_id': row['COMMODITY_CODE'],
#             '_source': {
#                 'COMMODITY_CODE': row['COMMODITY_CODE'],
#                 'COMMODITY_NAME': row['COMMODITY_NAME'],
#                 'TYPE_GAUGE': row['TYPE_GAUGE'],
#                 'CLASS_NAME': row['CLASS_NAME'],
#                 'CLASS_CODE': row['CLASS_CODE'],
#                 # 'COMMODITY_SPECIFIC': COMMODITY_SPECIFIC_nested,
#             }
            
#         }
    
# bulk(connections.get_connection(), bulk_indexing(df[:10]), request_timeout=100)
# bulk_indexing(df[:10])
# s = Search().filter('term', CLASS_NAME='深沟球轴承') # 品类要求

# response = s.execute()

# for hit in response:
#     print(hit.COMMODITY_NAME)

