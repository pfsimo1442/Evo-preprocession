import os

def convert_txt_to_tokenizer(input_dir, output_file):
    """
    숫자 기반 연속 대화 txt 파일들을 tokenizer_data.txt 형식으로 변환
    """
    all_lines = []
    for fname in os.listdir(input_dir):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(input_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        current_dialog = []
        prev_index = None
        for line in lines:
            if not line.strip():
                continue
            # 숫자\t텍스트 형태
            try:
                index, text = line.strip().split("\t", 1)
            except:
                text = line.strip()
                index = prev_index
            if prev_index is None:
                prev_index = index

            if index != prev_index:
                # 이전 dialog flush
                for turn in current_dialog:
                    all_lines.append(f"<BOS> {turn} <EOS>")
                all_lines.append("")  # 대화 구분
                current_dialog = []
                prev_index = index

            current_dialog.append(text)

        # 마지막 대화 flush
        for turn in current_dialog:
            all_lines.append(f"<BOS> {turn} <EOS>")
        all_lines.append("")

    # 파일 저장
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))
    print(f"tokenizer_data.txt saved to {output_file}")