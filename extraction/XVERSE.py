import torch
from modelscope import AutoTokenizer, AutoModelForCausalLM,snapshot_download
from modelscope import GenerationConfig
from jsonformer import Jsonformer

class Extraction:
    def __init__(self):
        model_dir = snapshot_download('xverse/XVERSE-7B-Chat',revision = 'v1.0.0')
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
        model.generation_config = GenerationConfig.from_pretrained(model_dir)
        self.model = model.eval()

        self.prompt = '请根据示例提取文本中的工业品信息\n示例：\n'
        egs = [
            # '输入：你好，我想要采购一个O型圈但不太确定具体型号 我需要一个应用于橡塑成形密封圈 内径:64.4, 材质:10, 横截面直径:3.1',
            # '输出：{"品类要求": "橡塑成形密封","技术属性要求": {"内径": "64.4","材质": "10","横截面直径": "3.1"}}',
            '输入：[{"user": "你好，我想要采购一个轴承，不太确定具体型号。","agent": "您好！有很多种轴承，例如深沟球轴承、圆锥滚子轴承、推力轴承等。您能描述一下您的需求或应用场景吗？"},{"user": "我需要一个应用于电机的轴承，要求转速较高，单列的。","agent": "了解了。那您可能需要一个深沟球轴承，它适合于高速旋转的应用场景。关于轴承的具体尺寸，您能提供一下内径、外径和宽度的要求吗？"},{"user": "内径12mm，外径37mm，宽度12mm。","agent": "好的，我已经记录了您的要求。我们有符合您描述的深沟球轴承，我会尽快为您提供采购详情。"}]',
            '输出：{"品类要求": "深沟球轴承","技术属性要求": {"内径": "12 mm","外径": "37 mm","宽度": "12 mm","列数": "1 列"}}',

        ]
        for eg in egs:
            self.prompt += eg + '\n'
        
        # 技术属性要求的键值对数量不定

        self.json_schema = {
            "type": "object",
            "properties": {
                "品类要求": {"type": "string"},
                "技术属性要求": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "string"
                    }
                }
            }
        }

    def extract(self, inp):
        p = self.prompt + '输入：' + inp + '\n输出：'
        history = [{"role": "user", "content": p}]
        response = self.model.chat(self.tokenizer, history)
        return response