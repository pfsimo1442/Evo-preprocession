import os
import json
from tqdm import tqdm

INPUT_DIR = "input"
OUTPUT_DIR = "output"
TOKENIZER_FILE = os.path.join(OUTPUT_DIR, "tokenizer_data.txt")
TRAIN_FILE = os.path.join(OUTPUT_DIR, "train_data.jsonl")

SPECIAL_TOKENS = ["<BOS>", "<EOS>"]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tokenizer_lines = SPECIAL_TOKENS + [""]  # special token 명시 후 한 줄 공백
    train_lines = []

    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)

        session_turns = []
        session_tokenizer_lines = []
        prev_turn = None

        cnt = 0
        pbar = tqdm(records)
        for entry in pbar:
            turn = entry.get("Turn")
            q = entry.get("Question", "").strip()
            a = entry.get("Answer", "").strip()

            # Turn이 "1"이면 새 세션 시작
            if turn == "1":
                # 이전 세션 저장
                if session_turns:
                    train_lines.append({"turns": session_turns})
                    tokenizer_lines.append("\n".join(session_tokenizer_lines))
                    tokenizer_lines.append("")  # 세션 구분 빈줄

                # 새 세션 초기화
                session_turns = []
                session_tokenizer_lines = []

            # Question → user
            if q:
                session_turns.append({"role": "user", "text": q})
                session_tokenizer_lines.append(f"<BOS> {q} <EOS>")

            # Answer → assistant
            if a:
                session_turns.append({"role": "assistant", "text": a})
                session_tokenizer_lines.append(f"<BOS> {a} <EOS>")

            cnt += 1
            pbar.set_description("Processing %s now..." % filename)

        # 마지막 세션 저장
        if session_turns:
            train_lines.append({"turns": session_turns})
            tokenizer_lines.append("\n".join(session_tokenizer_lines))
            tokenizer_lines.append("")

        print(f"finish convert {cnt} sessions")

    # tokenizer_data.txt 저장
    with open(TOKENIZER_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tokenizer_lines).strip() + "\n")

    # train_data.jsonl 저장
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for line in train_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    print(f"완료! tokenizer_data.txt: {TOKENIZER_FILE}, train_data.jsonl: {TRAIN_FILE}")


if __name__ == "__main__":
    main()