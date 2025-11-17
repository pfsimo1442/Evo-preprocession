import json
from collections import defaultdict

def convert_json_dialog(json_file, tokenizer_output, train_output):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    dialogs = defaultdict(list)

    for item in data:
        idx = item["index"]
        u = item["user_utterance"]
        s = item["system_utterance"]

        if s and s.lower() != "null":
            dialogs[idx].append(("assistant", s))

        if u and u.lower() != "null":
            dialogs[idx].append(("user", u))

    # tokenizer text
    with open(tokenizer_output, "w", encoding="utf-8") as f:
        for idx in sorted(dialogs.keys()):
            for role, text in dialogs[idx]:
                f.write(text + "\n")

    # jsonl data
    with open(train_output, "w", encoding="utf-8") as f:
        for idx in sorted(dialogs.keys()):
            turns = []
            for role, text in dialogs[idx]:
                turns.append({"role": role, "text": text})

            json.dump({"turns": turns}, f, ensure_ascii=False)
            f.write("\n")

    print("JSON 대화 변환 완료!")