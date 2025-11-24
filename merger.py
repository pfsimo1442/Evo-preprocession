import os
import json

TOKENIZER_DIR = "merged/tokenizer"
TRAIN_DIR = "merged/train"
OUTPUT_DIR = "output"

MERGED_TOKENIZER = os.path.join(OUTPUT_DIR, "tokenizer_data.txt")
MERGED_TRAIN = os.path.join(OUTPUT_DIR, "train_data.jsonl")

SPECIAL_TOKENS = ["<BOS>", "<EOS>"]


def merge_tokenizer_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    merged_lines = []
    merged_lines.extend(SPECIAL_TOKENS)
    merged_lines.append("")  # special token 뒤 한 줄 공백

    for fname in sorted(os.listdir(TOKENIZER_DIR)):
        if not fname.endswith(".txt"):
            continue

        path = os.path.join(TOKENIZER_DIR, fname)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        # 각 파일의 special token(<BOS>, <EOS>) 헤더 제거
        cleaned = []
        for line in lines:
            striped = line.strip()
            if striped in SPECIAL_TOKENS:
                continue
            cleaned.append(line)

        # 파일별로 그대로 이어붙임
        merged_lines.extend(cleaned)
        merged_lines.append("")  # 파일 구분용 빈 줄

    # 최종 저장
    with open(MERGED_TOKENIZER, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_lines).strip() + "\n")


def merge_train_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(MERGED_TRAIN, "w", encoding="utf-8") as outfile:
        for fname in sorted(os.listdir(TRAIN_DIR)):
            if not fname.endswith(".jsonl"):
                continue

            path = os.path.join(TRAIN_DIR, fname)
            with open(path, "r", encoding="utf-8") as infile:
                for line in infile:
                    line = line.strip()
                    if line:
                        outfile.write(line + "\n")


def main():
    merge_tokenizer_files()
    merge_train_files()
    print("모든 tokenizer_data.txt / train_data.jsonl 병합 완료!")


if __name__ == "__main__":
    main()