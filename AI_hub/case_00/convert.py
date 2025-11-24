import os
import json
from collections import defaultdict


# ==============================
#  JSON 처리 (case17)
# ==============================
def process_case17_json(path):
    import json
    from collections import defaultdict

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    groups = defaultdict(list)
    for row in data:
        groups[row["index"]].append(row)

    sessions = []

    for idx, rows in groups.items():
        # ignore session if assistant starts first
        if rows[0]["user_utterance"] == "null":
            continue

        turns = []
        current_user = None
        assistant_buffer = []

        for r in rows:
            user = r["user_utterance"]
            sys = r["system_utterance"]

            # user 발화 처리
            if user and user != "null":
                # 이전 user가 있고 assistant도 있으면 저장
                if current_user is not None and assistant_buffer:
                    turns.append({"role": "user", "text": current_user})
                    turns.append({
                        "role": "assistant",
                        "text": " ".join(assistant_buffer)
                    })
                    assistant_buffer = []

                current_user = user.strip()

            # assistant 발화 처리
            if sys and sys != "null":
                assistant_buffer.append(sys.strip())

        # 마지막 user → assistant 저장
        if current_user is not None:
            turns.append({"role": "user", "text": current_user})
        if assistant_buffer:
            turns.append({
                "role": "assistant",
                "text": " ".join(assistant_buffer)
            })

        # assistant로 시작하는 세션 제거
        if turns[0]["role"] == "assistant":
            continue

        sessions.append({"turns": turns})

    return sessions


# ==============================
#  TXT 처리 (case17)
# ==============================
def process_case17_txt(path):
    sessions = []
    current_turns = []

    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or "\t" not in line:
            continue

        idx_str, text = line.split("\t", 1)
        idx_str = idx_str.replace("\ufeff", "")

        try:
            idx = int(idx_str)
        except:
            continue

        text = text.replace("\n", " ").strip()

        # index == 1이면 새로운 session 시작
        if idx == 1:
            if current_turns:
                sessions.append({"turns": current_turns})
            current_turns = []  # reset

        # 홀수 = user, 짝수 = assistant
        role = "user" if idx % 2 == 1 else "assistant"
        current_turns.append({"role": role, "text": text})

    # 마지막 session 추가
    if current_turns:
        sessions.append({"turns": current_turns})

    return sessions


# ==============================
#  tokenizer_data.txt 생성
# ==============================
def build_tokenizer_lines(all_sessions):
    lines = ["<BOS>", "<EOS>", ""]
    for session in all_sessions:
        turns = session["turns"]
        for t in turns:
            lines.append(f"<BOS> {t['text']} <EOS>")
        lines.append("")  # 발화 간 공백
    return "\n".join(lines)


# ==============================
#  JSONL 생성
# ==============================
def build_jsonl(all_sessions):
    jsonl_lines = []
    for session in all_sessions:
        jsonl_lines.append(json.dumps(session, ensure_ascii=False))
    return "\n".join(jsonl_lines)


# ==============================
#  메인 함수
# ==============================
def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    all_sessions = []

    for fname in os.listdir(input_dir):
        path = os.path.join(input_dir, fname)

        if fname.endswith(".json"):
            sessions = process_case17_json(path)
            all_sessions.extend(sessions)

        elif fname.endswith(".txt"):
            sessions = process_case17_txt(path)
            all_sessions.extend(sessions)

    # tokenizer_data.txt
    tokenizer_text = build_tokenizer_lines(all_sessions)
    with open(os.path.join(output_dir, "tokenizer_data.txt"), "w", encoding="utf-8") as f:
        f.write(tokenizer_text)

    # train_data.jsonl
    jsonl_text = build_jsonl(all_sessions)
    with open(os.path.join(output_dir, "train_data.jsonl"), "w", encoding="utf-8") as f:
        f.write(jsonl_text)

    print(f"완료! 총 세션 수: {len(all_sessions)}")


if __name__ == "__main__":
    main()