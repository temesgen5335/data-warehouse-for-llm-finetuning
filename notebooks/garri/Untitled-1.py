# %%
# !pip install -q transformers
# !pip install -q peft
# !pip install -q bitsandbytes
# !pip install -q torch

# %%
import torch
import os

# %%
# from google.colab import drive
# drive.mount('/content/drive')

# cache_dir = "/content/drive/MyDrive/Colab Notebooks/hf_models" # adding a cache dir is optional

# %%
cache_dir = "/home/hillary_kipkemoi/cache_dir" # adding a cache dir is optional

# %%
from transformers import LlamaTokenizer

checkpoint = "iocuydi/llama-2-amharic-3784m"
commit_hash = "04fcac974701f1dab0b8e39af9d3ecfce07b3773"
# The commit hash is needed, because the model repo was rearranged after this commit (files -> finetuned/files),
# and I couldn't load the model from the new structure

tokenizer = LlamaTokenizer.from_pretrained(checkpoint, revision=commit_hash, cache_dir= cache_dir)

# %%
embedding_size = tokenizer.get_input_embeddings().weight.shape[0]


# %%
print(tokenizer.encode("በ በአለማቀፍ ደረጃ የተፈፀመው የሞት ቅጣት"))

print(tokenizer.tokenize("በ በአለማቀፍ ደረጃ የተፈፀመው የሞት ቅጣት"))

# %%
tokenizer.vocab_size

# %%
import torch

torch.cuda.is_available() # Need GPU to use load_in_8bit

# %% [markdown]
# [source llama hf docs](https://huggingface.co/docs/transformers/main/en/model_doc/llama#transformers.LlamaForCausalLM)

# %%
from peft import PeftModel
from transformers import LlamaForCausalLM, GenerationConfig, AutoModelForSequenceClassification

llama_model = LlamaForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    load_in_8bit=True,
    device_map="auto",
    cache_dir= cache_dir, # optional
)

# %%
llama_model.resize_token_embeddings(len(tokenizer)) # needed because the fine-tuned model extended the tokenizer

# %%
# this is the model we want:
model = PeftModel.from_pretrained(llama_model, "iocuydi/llama-2-amharic-3784m",revision =commit_hash, cache_dir= cache_dir)

# %%
model.is_quantized

# %%



