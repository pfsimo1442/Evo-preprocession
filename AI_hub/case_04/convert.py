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

    tokenizer_lines = SPECIAL_TOKENS + [""]  # special token 명시 + 공백
    train_lines = []

    cnt = 0
    pbar = tqdm(sorted(os.listdir(INPUT_DIR)))
    # input 디렉토리 순회
    for filename in pbar:
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # numberOfParticipants가 2가 아니면 skip
        if data.get("participantsInfo", {}).get("numberOfParticipants") != "2":
            continue

        # sessionInfo 안에 여러 session이 있을 수 있음
        sessions = data.get("sessionInfo", [])
        for session in sessions:
            dialog_list = session.get("dialog", [])
            turns = []
            session_tokenizer_lines = []

            for dialog in dialog_list:
                speaker = dialog.get("speaker")
                utter = dialog.get("utterance", "").strip()

                if not utter:
                    continue

                # tokenizer_data.txt용
                session_tokenizer_lines.append(f"<BOS> {utter} <EOS>")

                # train_data.jsonl용
                # role = "user" if speaker == "speaker1" else "assistant"
                if speaker == "speaker1":
                    role = "user"
                elif speaker == "speaker2":
                    role = "assistant"
                else:
                    continue

                turns.append({
                    "role": role,
                    "text": utter
                })

            # session 기반 결과 반영
            if turns:
                train_lines.append({"turns": turns})

            # tokenizer_data.txt는 세션은 \n\n으로 구분
            if session_tokenizer_lines:
                tokenizer_lines.append("\n".join(session_tokenizer_lines))
                tokenizer_lines.append("")  # 세션 사이 공백 줄 → \n\n 효과
        
        cnt += 1
        pbar.set_description("Processing %s now..." % filename)

    print(f"finish convert {cnt} json files")

    # tokenizer_data.txt 저장
    with open(TOKENIZER_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tokenizer_lines).strip() + "\n")

    # train_data.jsonl 저장
    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for item in train_lines:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"완료! tokenizer_data.txt: {TOKENIZER_FILE}, train_data.jsonl: {TRAIN_FILE}")

if __name__ == "__main__":
    main()