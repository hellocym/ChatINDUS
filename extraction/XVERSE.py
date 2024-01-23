import torch
from modelscope import AutoTokenizer, AutoModelForCausalLM,snapshot_download
from modelscope import GenerationConfig

class Extraction:
    def __init__(self):
        model_dir = snapshot_download('xverse/XVERSE-7B-Chat',revision = 'v1.0.0')
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
        model.generation_config = GenerationConfig.from_pretrained(model_dir)
        self.model = model.eval()

        self.prompt = '请根据示例提取文本中的工业品信息\n示例：\n'
        egs = [
            '输入：你好，我想要采购一个O型圈但不太确定具体型号 我需要一个应用于橡塑成形密封圈 内径:64.4, 材质:10, 横截面直径:3.1',
            '输出：{"品类要求": "橡塑成形密封","技术属性要求": {"内径": "64.4","材质": "10","横截面直径": "3.1"}}',
        ]
        for eg in egs:
            self.prompt += eg + '\n'

    def extract(self, inp):
        p = self.prompt + '输入：' + inp + '\n输出：'
        history = [{"role": "user", "content": p}]
        response = self.model.chat(self.tokenizer, history)
        return response