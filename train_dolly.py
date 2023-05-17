# Databricks notebook source
# DBTITLE 1,gbrckkvrbilckiuudfluekii
# MAGIC %md
# MAGIC ## Train Dolly
# MAGIC
# MAGIC rinna/japanese-gpt-1bなどモデルをファインチューニングする日本語モデル構築の例です。
# MAGIC (e.g. [pythia-2.8b](https://huggingface.co/EleutherAI/pythia-2.8b),
# MAGIC [pythia-6.9b](https://huggingface.co/EleutherAI/pythia-6.9b), or
# MAGIC [pythia-12b](https://huggingface.co/EleutherAI/pythia-12b)) on
# MAGIC the [databricks-dolly-15k](https://github.com/databrickslabs/dolly/tree/master/data) dataset.
# MAGIC
# MAGIC ```
# MAGIC   Licensed under the Apache License, Version 2.0 (the "License");
# MAGIC   you may not use this file except in compliance with the License.
# MAGIC   You may obtain a copy of the License at
# MAGIC
# MAGIC       http://www.apache.org/licenses/LICENSE-2.0
# MAGIC
# MAGIC   Unless required by applicable law or agreed to in writing, software
# MAGIC   distributed under the License is distributed on an "AS IS" BASIS,
# MAGIC   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# MAGIC   See the License for the specific language governing permissions and
# MAGIC   limitations under the License.
# MAGIC ```
# MAGIC
# MAGIC The EleutherAI Pythia models are [Apache 2.0 licensed](https://huggingface.co/EleutherAI/gpt-j-6B) and
# MAGIC the [databricks-dolly-15k](https://github.com/databrickslabs/dolly/tree/master/data) is licensed under the terms
# MAGIC of [Creative Commons Attribution-ShareAlike 3.0 Unported License](https://creativecommons.org/licenses/by-sa/3.0/legalcode),
# MAGIC which means it can be used for either academic or commercial purposes.

# COMMAND ----------

# MAGIC %md
# MAGIC Install these additional NVIDIA libraries for Databricks Runtime 12.2 ML:

# COMMAND ----------

!wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusparse-dev-11-3_11.5.0.58-1_amd64.deb -O /tmp/libcusparse-dev-11-3_11.5.0.58-1_amd64.deb && \
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcublas-dev-11-3_11.5.1.109-1_amd64.deb -O /tmp/libcublas-dev-11-3_11.5.1.109-1_amd64.deb && \
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusolver-dev-11-3_11.1.2.109-1_amd64.deb -O /tmp/libcusolver-dev-11-3_11.1.2.109-1_amd64.deb && \
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcurand-dev-11-3_10.2.4.109-1_amd64.deb -O /tmp/libcurand-dev-11-3_10.2.4.109-1_amd64.deb && \
  dpkg -i /tmp/libcusparse-dev-11-3_11.5.0.58-1_amd64.deb && \
  dpkg -i /tmp/libcublas-dev-11-3_11.5.1.109-1_amd64.deb && \
  dpkg -i /tmp/libcusolver-dev-11-3_11.1.2.109-1_amd64.deb && \
  dpkg -i /tmp/libcurand-dev-11-3_10.2.4.109-1_amd64.deb

# COMMAND ----------

# MAGIC %md
# MAGIC Install these additional NVIDIA libraries for Databricks Runtime 13.0 ML (uncomment first):

# COMMAND ----------

#!wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusparse-dev-11-7_11.7.3.50-1_amd64.deb -O /tmp/libcusparse-dev-11-7_11.7.3.50-1_amd64.deb && \
#  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcublas-dev-11-7_11.10.1.25-1_amd64.deb -O /tmp/libcublas-dev-11-7_11.10.1.25-1_amd64.deb && \
#  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcusolver-dev-11-7_11.4.0.1-1_amd64.deb -O /tmp/libcusolver-dev-11-7_11.4.0.1-1_amd64.deb && \
#  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/libcurand-dev-11-7_10.2.10.91-1_amd64.deb -O /tmp/libcurand-dev-11-7_10.2.10.91-1_amd64.deb && \
#  dpkg -i /tmp/libcusparse-dev-11-7_11.7.3.50-1_amd64.deb && \
#  dpkg -i /tmp/libcublas-dev-11-7_11.10.1.25-1_amd64.deb && \
#  dpkg -i /tmp/libcusolver-dev-11-7_11.4.0.1-1_amd64.deb && \
#  dpkg -i /tmp/libcurand-dev-11-7_10.2.10.91-1_amd64.deb

# COMMAND ----------

# MAGIC %pip install -r requirements.txt

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger("py4j").setLevel(logging.WARNING)
logging.getLogger("sh.command").setLevel(logging.ERROR)

# COMMAND ----------

import os
import re
from datetime import datetime
from training.consts import DEFAULT_INPUT_MODEL, SUGGESTED_INPUT_MODELS
from training.trainer import load_training_dataset, load_tokenizer

dbutils.widgets.combobox("input_model", DEFAULT_INPUT_MODEL, "SUGGESTED_INPUT_MODELS", "input_model")
dbutils.widgets.text("num_gpus", "", "num_gpus")
dbutils.widgets.text("local_training_root", "", "local_training_root")
dbutils.widgets.text("dbfs_output_root", "", "dbfs_output_root")
dbutils.widgets.text("experiment_id", "", "experiment_id")

# COMMAND ----------

# Cache data and tokenizer locally before creating a bunch of deepspeed processes and make sure they succeeds.
load_training_dataset()
load_tokenizer()

# COMMAND ----------


timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
model_name = "rinna-gpt-1b_dolly15k_dbqa"

experiment_id = dbutils.widgets.get("experiment_id")
input_model = dbutils.widgets.get("input_model")

if experiment_id:
    experiment_id = re.sub(r"\s+", "_", experiment_id.strip())
    model_name = f"{model_name}__{experiment_id}"

checkpoint_dir_name = f"{model_name}__{timestamp}"

root_path = os.getcwd()
deepspeed_config = os.path.join(root_path, "config/ds_z3_bf16_config.json")

dolly_training_dir_name = "rinna-gpt-1b_dolly15k_dbqa_training"

# Use the local training root path if it was provided.  Otherwise try to find a sensible default.
local_training_root = dbutils.widgets.get("local_training_root")
if not local_training_root:
    # Use preferred path when working in a Databricks cluster if it exists.
    if os.path.exists("/local_disk0"):
        local_training_root = os.path.join("/local_disk0", dolly_training_dir_name)
    # Otherwise use the home directory.
    else:
        local_training_root = os.path.join(os.path.expanduser('~'), dolly_training_dir_name)

dbfs_output_root = dbutils.widgets.get("dbfs_output_root")
if not dbfs_output_root:
    dbfs_output_root = f"/dbfs/Users/yulan.yan@databricks.com/{dolly_training_dir_name}"

os.makedirs(local_training_root, exist_ok=True)
os.makedirs(dbfs_output_root, exist_ok=True)

local_output_dir = os.path.join(local_training_root, checkpoint_dir_name)
dbfs_output_dir = os.path.join(dbfs_output_root, checkpoint_dir_name)

num_gpus_flag = ""
num_gpus = dbutils.widgets.get("num_gpus")
if num_gpus:
    num_gpus = int(num_gpus)
    num_gpus_flag = f"--num_gpus={num_gpus}"

tensorboard_display_dir = f"{local_output_dir}/runs"

print(f"Local Output Dir: {local_output_dir}")
print(f"DBFS Output Dir: {dbfs_output_dir}")
print(f"Tensorboard Display Dir: {tensorboard_display_dir}")

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# COMMAND ----------

# MAGIC %load_ext tensorboard
# MAGIC %tensorboard --logdir '{tensorboard_display_dir}'

# COMMAND ----------

!deepspeed {num_gpus_flag} \
    --module training.trainer \
    --input-model {input_model} \
    --deepspeed {deepspeed_config} \
    --epochs 10 \
    --local-output-dir {local_output_dir} \
    --dbfs-output-dir {dbfs_output_dir} \
    --per-device-train-batch-size 6 \
    --per-device-eval-batch-size 6 \
    --logging-steps 10 \
    --save-steps 200 \
    --save-total-limit 20 \
    --eval-steps 50 \
    --warmup-steps 50 \
    --test-size 200 \
    --lr 1e-07

# COMMAND ----------

from transformers import T5Tokenizer, AutoModelForCausalLM

tokenizer = T5Tokenizer.from_pretrained(local_output_dir)
model = AutoModelForCausalLM.from_pretrained(local_output_dir)

# COMMAND ----------

import torch

MAX_ASSISTANT_LENGTH = 100
MAX_INPUT_LENGTH = 1024

INPUT_PROMPT = r'以下は、タスクを説明する指示です。要求を適切に満たす応答を書きなさい。\n\n### 指示:\n{instruction}\n\n### 入力:\n{input}\n\n### 応答:\n'
NO_INPUT_PROMPT = r'以下は、タスクを説明する指示です。要求を適切に満たす応答を書きなさい。\n\n### 指示:\n{instruction}\n\n### 応答:\n'

def prepare_input(instruction, input_text):
    if input_text != "":
        prompt = INPUT_PROMPT.format(instruction=instruction, input=input_text)
    else:
        prompt = NO_INPUT_PROMPT.format(instruction=instruction)
    return prompt

def format_output(output):
    output = output.lstrip("<s>").rstrip("</s>").replace("[SEP]", "").replace("\\n", "\n")
    return output

def generate_response(instruction, input_text):
    prompt = prepare_input(instruction, input_text)
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    n = len(token_ids[0])

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            min_length=n,
            max_length=min(MAX_INPUT_LENGTH, n + MAX_ASSISTANT_LENGTH),
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_words_ids=[[tokenizer.unk_token_id]]
        )

    output = tokenizer.decode(output_ids.tolist()[0])
    formatted_output_all = format_output(output)
    response = f"Assistant:{formatted_output_all.split('応答:')[-1].strip()}"

    return formatted_output_all, response 

# instruction = "あなたは何でも正確に答えられるAIです。"
questions = [
    "日本で一番高い山は？",
    "日本で一番広い湖は？",
    "世界で一番高い山は？",
    "世界で一番広い湖は？",
    "機械学習とは？",
    "AutoMLでモデルを解釈できますか？",
    "データレイクハウスとは何ですか?",
    "AutoMLで回帰モデルを作れますか？",
    "AutoMLではFeature Storeのテーブルをサポートしていますか？",
    "分散機械学習をどのように行うか?",
    "データレイクハウスとデータウェアハウスの違いは?",
    "MLOpsのベストプラクティスについて教えてください。",
]

# 各質問に対して応答を生成して表示
for question in questions:
    formatted_output_all, response = generate_response(question, "")
    print(f"Question: {question}\n\n{response}\n\n-----------\n")


# COMMAND ----------


