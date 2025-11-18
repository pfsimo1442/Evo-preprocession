import os
import json

def convert_json_to_train_data(input_dir, output_file):
    """
    JSON 대화 데이터를 train_data.jsonl 형식으로 변환
    """
    output_data = []
    for fname in os.listdir(input_dir):
        if not fname.endswith(".txt") and not fname.endswith(".json"):
            continue
        path = os.path.join(input_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                # JSONL 파일일 경우
                data = [json.loads(line) for line in f]

        # index별로 묶기
        dialogs = {}
        for item in data:
            idx = item.get("index", 0)
            if idx not in dialogs:
                dialogs[idx] = []
            user_text = item.get("user_utterance", "").strip()
            system_text = item.get("system_utterance", "").strip()

            if user_text.lower() != "null" and user_text != "":
                dialogs[idx].append({"role": "user", "text": user_text})
            if system_text.lower() != "null" and system_text != "":
                dialogs[idx].append({"role": "assistant", "text": system_text})

        # dialogs flatten
        for turns in dialogs.values():
            if not turns:
                continue
            output_data.append({"turns": turns})

    # 파일 저장 (JSONL)
    with open(output_file, "w", encoding="utf-8") as f:
        for dialog in output_data:
            f.write(json.dumps(dialog, ensure_ascii=False) + "\n")

    print(f"train_data.jsonl saved to {output_file}")