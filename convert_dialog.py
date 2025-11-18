import os
import json

SPECIAL_TOKENS = ["<PAD>", "<UNK>", "<BOS>", "<EOS>", "<User>", "<Assistant>", "<SEP>"]

def process_txt_file(path):
    """
    txt 파일 처리: index 기반 연속 대화 추출
    """
    dialogs = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    current_dialog = []
    prev_index = None
    for line in lines:
        if not line.strip():
            continue
        try:
            index, text = line.strip().split("\t", 1)
        except:
            text = line.strip()
            index = prev_index
        if prev_index is None:
            prev_index = index

        if index != prev_index:
            if current_dialog:
                dialogs.append(current_dialog)
            current_dialog = []
            prev_index = index

        current_dialog.append(text)
    if current_dialog:
        dialogs.append(current_dialog)

    return dialogs

def process_json_file(path):
    """
    JSON / JSONL 파일 처리: index 기반 연속 대화 추출
    """
    dialogs = []
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            # JSONL 형식일 경우
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

    # 맨 앞 special token 삽입
    tokenizer_lines.extend(SPECIAL_TOKENS)
    tokenizer_lines.append("")  # 구분용 빈 줄

    for path in file_list:
        if path.endswith(".txt"):
            dialogs = process_txt_file(path)
            for dialog in dialogs:
                # tokenizer_data.txt
                for turn in dialog:
                    tokenizer_lines.append(f"<BOS> {turn} <EOS>")
                tokenizer_lines.append("")  # dialog 구분
                # train_data.jsonl
                train_data.append({"turns": [{"role": "user" if i % 2 == 0 else "assistant", "text": t} 
                                             for i, t in enumerate(dialog)]})
        elif path.endswith(".json"):
            dialogs = process_json_file(path)
            for dialog in dialogs:
                # tokenizer_data.txt
                for turn in dialog:
                    tokenizer_lines.append(f"<BOS> {turn['text']} <EOS>")
                tokenizer_lines.append("")  # dialog 구분
                # train_data.jsonl
                train_data.append({"turns": dialog})

    # 파일 저장
    with open(tokenizer_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tokenizer_lines))
    print(f"tokenizer_data.txt saved to {tokenizer_file}")

    with open(train_file, "w", encoding="utf-8") as f:
        for dialog in train_data:
            f.write(json.dumps(dialog, ensure_ascii=False) + "\n")
    print(f"train_data.jsonl saved to {train_file}")