DEFAULT_INPUT_MODEL = "rinna/japanese-gpt-1b"
SUGGESTED_INPUT_MODELS = [
    "rinna/japanese-gpt-1b",
    "ai-forever/mGPT", 
    "rinna/japanese-gpt2-medium",
    "abeja/gpt2-large-japanese",
    "abeja/gpt-neox-japanese-2.7b",
    "inu-ai/dolly-japanese-gpt-1b", 
    "yellowback/gpt-neo-japanese-1.3B", 
    "bigscience/bloom-7b1", # 
    "jweb/japanese-soseki-gpt2-1b", 
    "colorfulscoop/gpt2-small-ja", 
    "nlp-waseda/gpt2-xl-japanese",  
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