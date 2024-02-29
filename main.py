import os
import json

from .extraction.XVERSE import Extraction
from .query.postgre import Postgre
import torch


def recommend(inp):
    db = Postgre()  # 加载数据库
    ext = Extraction()  # 加载模型
    
    ans = ext.extract(str(inp))  # 抽取属性信息
    ans = json.loads(ans)  # str转换为字典
    # print(ans)
    records = db.query(ans)  # 在数据库中query
    ans = {**ans, "推荐商品": records}  # 添加属性信息
    # print(ans)
    return ans
    

if __name__ == "__main__":
    db = Postgre()
    ext = Extraction()
    
    try:
        while True:
            inp = input("Input: ")
            # inp = inp.strip(',')
            # inp = inp.strip('"')
            # inp = eval(inp)
            # inp = [i['user'] for i in inp]
            # inp = ' '.join(inp)
            # print(inp)
            
            ans = ext.extract(inp)
            ans = json.loads(ans)
            # print(ans)
            records = db.query(ans)
            ans = {**ans, "推荐商品": records}
            print(ans)
    # release vram while keyboard interrupt
    except KeyboardInterrupt:
        del ext
        del db
        
        torch.cuda.empty_cache()
        print("vram released")
        
        
