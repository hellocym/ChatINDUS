# 从data/test3.csv 读取input
# curl命令：curl -X POST -H "Content-Type: application/json" -d '{"input":[{"user":"你好，我想要采购一个轴承，不太确定具体型号。","agent":"您好！有很多种轴承，例如深沟球轴承、圆锥滚子轴承、推力轴承等。您能描述一下您的需求或应用场景 吗？"},{"user":"我需要一个应用于电机的轴承，要求转速较高，单列的。","agent":"了解了。那您可能需要一个深沟球轴承，它适合于高速旋转的应用场 景。关于轴承的具体尺寸，您能提供一下内径、外径和宽度的要求吗？"},{"user":"内径12mm，外径37mm，宽度12mm。","agent":"好的，我已经记录了您的 要求。我们有符合您描述的深沟球轴承，我会尽快为您提供采购详情。"}]}' http://127.0.0.1:7890/demo
# 将返回结果写回data/test3.csv 的RESULT列

import os
import json
import pandas as pd
import requests

url = 'http://127.0.0.1:7890/demo' 

f = pd.read_csv('data/test3.csv')
for i in range(len(f)):
    inp = f.iloc[i, 0]
    data = {'input': inp}
    response = requests.post(url, json=data)
    result = response.text
    # result中有\uxxxx的字符，需要转换
    result = result.encode('utf-8').decode('unicode_escape')
    f.iloc[i, 1] = result
    print(result)

f.to_csv('data/3_test.csv', index=False)
    