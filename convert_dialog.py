import os
import json

SPECIAL_TOKENS = ["<PAD>", "<UNK>", "<BOS>", "<EOS>", "<User>", "<Assistant>", "<SEP>"]

def isOdd(num):
    return True if num % 2 == 1 else False

def process_txt_file(path):
    dialogs = []
    current_dialog = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                index_str, text = line.strip().split("\t", 1)
                index = int(index_str)
            except:
                continue

            role = "user" if isOdd(index) else "assistant"
            current_dialog.append({"role": role, "text": text})

            # 새로운 대화 단위 구분: index가 1로 다시 시작하면 새로운 dialog
            if index == 1 and current_dialog[:-1]:
                dialogs.append(current_dialog[:-1])
                current_dialog = [current_dialog[-1]]

    if current_dialog:
        dialogs.append(current_dialog)

    return dialogs

def process_json_file(path):
    dialogs = []
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            data = [json.loads(line) for line in f]

    grouped = {}
    for item in data:
        idx = item.get("index", 0)
        user_text = item.get("user_utterance", "").strip()
        system_text = item.get("system_utterance", "").strip()

        if idx not in grouped:
            grouped[idx] = []

        if user_text.lower() != "null" and user_text != "":
            grouped[idx].append({"role": "user", "text": user_text})
        if system_text.lower() != "null" and system_text != "":
            grouped[idx].append({"role": "assistant", "text": system_text})

    for turns in grouped.values():
        dialogs.append(turns)

    return dialogs

def convert_all(file_list, tokenizer_file, train_file):
    tokenizer_lines = []
    train_data = []

    # special token
    tokenizer_lines.extend(SPECIAL_TOKENS)
    tokenizer_lines.append("")

    for path in file_list:
        if path.endswith(".txt"):
            dialogs = process_txt_file(path)
        elif path.endswith(".json"):
            dialogs = process_json_file(path)
        else:
            continue

        for dialog in dialogs:
            # tokenizer_data.txt
            for turn in dialog:
                tokenizer_lines.append(f"<BOS> {turn['text']} <EOS>")
            tokenizer_lines.append("")  # dialog 구분

            # train_data.jsonl
            train_data.append({"turns": dialog})

    with open(tokenizer_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tokenizer_lines))
    print(f"tokenizer_data.txt saved to {tokenizer_file}")

    with open(train_file, "w", encoding="utf-8") as f:
        for dialog in train_data:
            f.write(json.dumps(dialog, ensure_ascii=False) + "\n")
    print(f"train_data.jsonl saved to {train_file}")