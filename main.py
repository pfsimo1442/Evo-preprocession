import os
from convert_txt_dialog import convert_txt_to_tokenizer
from convert_json_dialog import convert_json_to_train_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TXT = os.path.join(BASE_DIR, "input_txt")
INPUT_JSON = os.path.join(BASE_DIR, "input_json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

TOKENIZER_FILE = os.path.join(OUTPUT_DIR, "tokenizer_data.txt")
TRAIN_DATA_FILE = os.path.join(OUTPUT_DIR, "train_data.jsonl")

# 변환 실행
convert_txt_to_tokenizer(INPUT_TXT, TOKENIZER_FILE)
convert_json_to_train_data(INPUT_JSON, TRAIN_DATA_FILE)

print("All preprocessing done.")