import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class Extraction:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("baichuan-inc/Baichuan2-7B-Base", trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained("baichuan-inc/Baichuan2-7B-Base", torch_dtype=torch.float16, trust_remote_code=True)
        self.model = self.model.quantize(4).cuda()
        #self.example_input = "{'user': '你好，我想要采购一个O型圈但不太确定具体型号', 'agent': '您好！请问您的产品规格和尺寸是什么？这样我才能为您推荐合适的O型圈。'}, {'user': '我需要一个应用于橡塑成形密封圈', 'agent': '好的，请告诉我产品的材料、工作温度范围以及是否具有耐磨性等要求，以便我为您提供更准确的建议。'}, {'user': '内径:64.4, 材质:10, 横截面直径:3.1', 'agent': '根据您提供的参数，以下是一些可能适合的产品：\n\n1. Viton O型圈(Viton是一种氟聚合物，适用于高温、高压和化学环境)\n2. NBR O型圈(NBR是一种丁腈橡胶，适用于中等压力和温度环境)\n3. Silicone O型圈(硅橡胶适用于低温、高湿度和食品级应用)\n\n由于没有具体的品牌或供应商信息，以上仅为参考建议。如果您能提供更多详细信息，例如所需的工作条件、寿命要求等，我们将能够更好地帮助您选择合适的产品。'}"
        self.example_input = "你好，我想要采购一个O型圈但不太确定具体型号 我需要一个应用于橡塑成形密封圈 内径:64.4, 材质:10, 横截面直径:3.1"
        self.example_output = '''{
"品类要求": "橡塑成形密封",
"技术属性要求": {
"内径": "64.4",
"材质": "10",
"横截面直径": "3.1"
}
}'''
        self.prompt = f"{self.example_input}->{self.example_output}"

    def extract(self, inp):
        msg = self.prompt + "\n" + inp + "->"
        inputs = self.tokenizer(msg, return_tensors='pt')
        inputs = inputs.to('cuda:0')
        pred = self.model.generate(**inputs, max_new_tokens=64, repetition_penalty=1.1)
        return self.tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)
    
# inp = "{'user': '你好，我想要采购一个调心滚子轴承但不太确定具体型号', 'agent': '您好！请问您的应用场景是什么？例如：汽车、机械设备等。这样我可以给您推荐更合适的调心滚子轴承型号。'}, {'user': '我需要一个调心滚子轴承', 'agent': '根据您的需求，我们建议使用以下几种常见的调心滚子轴承类型：\n1. NACHI的NJ2308E-TVP2(内径40mm，外径72mm，厚度25mm)\n2. SKF的NU2308ECM(内径40mm，外径72mm，厚度26mm)\n3. FAG的NAO92308-HCSNAP(内径40mm，外径72mm，厚度2cm)\n以上三种都是常用的调心滚子轴承，适用于各种不同的场合和行业。如果您有其他特殊要求或问题，请随时告诉我们，我们会尽力为您提供帮助。'}, {'user': '内径:190, 外径:340, 宽度:120'}"
# msg = f"{example_input}->{example_output}\n{inp}->"

# inputs = tokenizer(msg, return_tensors='pt')
# inputs = inputs.to('cuda:0')
# pred = model.generate(**inputs, max_new_tokens=64, repetition_penalty=1.1)
# print(tokenizer.decode(pred.cpu()[0], skip_special_tokens=True))