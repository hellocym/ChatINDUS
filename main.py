import os
import json

from extraction.XVERSE import Extraction
from query.postgre import Postgre

# use hf mirror site
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

def recommend(inp):
    ext = Extraction()
    db = Postgre()
    
    ans = ext.extract(inp)
    ans = json.loads(ans)
    # print(ans)
    records = db.query(ans)
    ans = {**ans, "records": records}
    print(ans)
    return ans
    

if __name__ == "__main__":
    ext = Extraction()
    db = Postgre()
    
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
        ans = {**ans, "records": records}
        # print(records)
        
