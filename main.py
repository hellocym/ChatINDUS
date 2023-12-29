from extraction.Baichuan2 import Extraction

# use hf mirror site
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

if __name__ == "__main__":
    ext = Extraction()
    while True:
        inp = input("Input: ")
        inp = inp.strip('"')
        inp = eval(inp)
        inp = [i['user'] for i in inp]
        inp = ' '.join(inp)
        # print(' '.join(inp))
        ans = ext.extract(inp)
        ans = ans.split('->')[-1]
        print(ans)