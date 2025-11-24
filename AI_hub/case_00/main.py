import os
from convert_dialog import convert_all

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TXT = os.path.join(BASE_DIR, "input_txt")
INPUT_JSON = os.path.join(BASE_DIR, "input_json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TOKENIZER_FILE = os.path.join(OUTPUT_DIR, "tokenizer_data.txt")
TRAIN_DATA_FILE = os.path.join(OUTPUT_DIR, "train_data.jsonl")

# 모든 입력 파일 목록 생성
all_input_files = []
for folder in [INPUT_TXT, INPUT_JSON]:
    for fname in os.listdir(folder):
        if fname.endswith(".txt") or fname.endswith(".json"):
            all_input_files.append(os.path.join(folder, fname))

# 변환 실행
convert_all(all_input_files, TOKENIZER_FILE, TRAIN_DATA_FILE)

print("All preprocessing done.")