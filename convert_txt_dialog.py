import json

def convert_txt(file_path, tokenizer_output, train_output):
    dialogs = []
    current_dialog = []
    last_idx = None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            idx, text = line.split("\t", 1)
            idx = int(idx)

            if last_idx is not None and idx < last_idx:
                dialogs.append(current_dialog)
                current_dialog = []

            current_dialog.append(text)
            last_idx = idx

    if current_dialog:
        dialogs.append(current_dialog)

    # tokenizer data
    with open(tokenizer_output, "w", encoding="utf-8") as f:
        for dialog in dialogs:
            for utt in dialog:
                f.write(utt + "\n")

    # jsonl data
    with open(train_output, "w", encoding="utf-8") as f:
        for dialog in dialogs:
            turns = []
            for i, t in enumerate(dialog):
                role = "user" if i % 2 == 0 else "assistant"
                turns.append({"role": role, "text": t})

            json.dump({"turns": turns}, f, ensure_ascii=False)
            f.write("\n")

    print("TXT 변환 완료!")