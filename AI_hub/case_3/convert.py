import os
import json
from tqdm import tqdm

INPUT_DIR = "input"
OUTPUT_DIR = "output"
TOKENIZER_FILE = os.path.join(OUTPUT_DIR, "tokenizer_data.txt")
TRAIN_FILE = os.path.join(OUTPUT_DIR, "train_data.jsonl")

# special tokens
SPECIAL_TOKENS = ["<BOS>", "<EOS>"]

def process_text(text):
    # '\n' -> ' '로 변환
    return text.replace("\n", " ").strip()

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tokenizer_lines = SPECIAL_TOKENS + [""]  # 첫 줄에 <BOS> <EOS> 명시 후 공백
    train_lines = []

    cnt = 0
    pbar = tqdm(sorted(os.listdir(INPUT_DIR)))
    for filename in pbar:
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # speakerC가 존재하면 skip
        speakerC = data.get("info", {}).get("speaker", {}).get("speakerCId")
        if speakerC is not None:
            continue

        utterances = data.get("utterances", [])
        dialogue = []
        for utt in utterances:
            speaker = utt["speaker"]
            text = process_text(utt["text"])
            if not text:
                continue

            # tokenizer_data.txt용
            tokenizer_lines.append(f"<BOS> {text} <EOS>")

            # train_data.jsonl용
            role = "user" if speaker == "speakerA" else "assistant"
            dialogue.append({"role": role, "text": text})

        # tokenizer_data.txt는 dialogue마다 \n 추가
        if tokenizer_lines:
            tokenizer_lines.append("")
        # train_data.jsonl에는 1개의 dialogue 단위로 기록
        if dialogue:
            train_lines.append({"turns": dialogue})
        
        cnt += 1
        pbar.set_description("Processing %s now..." % filename)
    
    print(f"finish convert {cnt} json files")

    # write tokenizer_data.txt
    with open(TOKENIZER_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tokenizer_lines))

    # write train_data.jsonl
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for line in train_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    print(f"완료! tokenizer_data.txt: {TOKENIZER_FILE}, train_data.jsonl: {TRAIN_FILE}")

if __name__ == "__main__":
    main()