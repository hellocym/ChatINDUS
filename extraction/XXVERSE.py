import torch
from modelscope import AutoTokenizer, AutoModelForCausalLM,snapshot_download
from modelscope import GenerationConfig