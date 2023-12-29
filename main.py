from extraction.Baichuan2 import Extraction

# use hf mirror site
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

if __name__ == "__main__":
    ext = Extraction()
    while True:
        inp = input("Input: ")
        print(ext.extract(inp))