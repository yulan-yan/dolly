DEFAULT_INPUT_MODEL = "rinna/japanese-gpt-1b"
SUGGESTED_INPUT_MODELS = [
    "rinna/japanese-gpt-1b",
    "ai-forever/mGPT", # local_output_dir = "/dbfs/dolly_training_jp/dolly_jp__2023-05-01T16:51:59" : May 2 2023, 08:32 AM JST
    "rinna/japanese-gpt2-medium",
    "abeja/gpt2-large-japanese",
    "abeja/gpt-neox-japanese-2.7b",
    "facebook/xglm-7.5B", # Could not find response key error
    "facebook/xglm-1.7B", # Could not find response key error
    "inu-ai/dolly-japanese-gpt-1b", # load_tokenizer() error
    "Tanrei/GPTSAN-japanese", # Unrecognized configuration class error
    "hajime9652/xlnet-japanese", # Couldn't instantiate the backend tokenizer
    "NovelAI/genji-jp",
    "oshizo/qa-refine-japanese-gpt-1b",
    "yellowback/gpt-neo-japanese-1.3B", # /dbfs/dolly_training_jp/dolly_jp__2023-05-02T04:43:20 : May 2 2023, 13:43 PM JST
    "Aruno/Bloom-JP-160m", # Got unexpected arguments: {'token_type_ids': tensor([[0, 0, 0,  ..., 0, 0, 0],
    "bigscience/bloom-7b1", # /dbfs/dolly_training_jp/dolly_jp__2023-05-02T04:53:35  : May 2 2023, 14:06 PM JST
    "jweb/japanese-soseki-gpt2-1b", # Couldn't instantiate the backend tokenizer from one of: 
    "skytnt/gpt2-japanese-lyric-medium", 
    "skytnt/gpt2-japanese-lyric-small",
    "knok/japanese-distilgpt2", 
    "naclbit/gpt-j-japanese-6.8b", # apache-2.0 license : Couldn't instantiate the backend tokenizer from one of:
    "thefrigidliquidation/pythia-1b-lightnovels",
    "colorfulscoop/gpt2-small-ja", # cc license
    "KBlueLeaf/guanaco-7B-leh", # gpl-3.0 license
    "KBlueLeaf/guanaco-7b-leh-v2", # gpl-3.0 license : Tokenizer class LLaMATokenizer does not exist
    "okazaki-lab/japanese-gpt2-medium-unidic", #cc license
    "nlp-waseda/gpt2-xl-japanese",  #cc license : /dbfs/dolly_training_jp/dolly_jp__2023-05-02T05:30:17 : May 2 2023, 14:30 PM JST
    "nlp-waseda/gpt2-small-japanese-wikipedia", #cc license
    "ku-nlp/gpt2-small-japanese-char", # cc license
    "pythainlp/wangchanglm-7.5B-sft-en-sharded", # cc license : Could not find response key [2, 256010]
    "mosaicml/mpt-7b" # apache-2.0 license
]
INTRO_BLURB = (
    "以下は、タスクを説明する指示です。要求を適切に満たす応答を書きなさい。"
)
INSTRUCTION_KEY = "### 指示:"
INPUT_KEY = "入力:"
RESPONSE_KEY = "### 応答:"
END_KEY = "### 終了"
RESPONSE_KEY_NL = f"{RESPONSE_KEY}\n"
DEFAULT_SEED = 42

# This is a training prompt that does not contain an input string.  The instruction by itself has enough information
# to respond.  For example, the instruction might ask for the year a historic figure was born.
PROMPT_NO_INPUT_FORMAT = """{intro}

{instruction_key}
{instruction}

{response_key}
{response}""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    response_key=RESPONSE_KEY,
    response="{response}",
)

# This is a training prompt that contains an input string that serves as context for the instruction.  For example,
# the input might be a passage from Wikipedia and the intruction is to extract some information from it.
PROMPT_WITH_INPUT_FORMAT = """{intro}

{instruction_key}
{instruction}

{input_key}
{input}

{response_key}
{response}""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    input_key=INPUT_KEY,
    input="{input}",
    response_key=RESPONSE_KEY,
    response="{response}",
)

# This is the prompt that is used for generating responses using an already trained model.  It ends with the response
# key, where the job of the model is to provide the completion that follows it (i.e. the response itself).
PROMPT_FOR_GENERATION_FORMAT = """{intro}

{instruction_key}
{instruction}

{response_key}
""".format(
    intro=INTRO_BLURB,
    instruction_key=INSTRUCTION_KEY,
    instruction="{instruction}",
    response_key=RESPONSE_KEY,
)