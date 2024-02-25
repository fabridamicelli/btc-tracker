from pathlib import Path
import itertools
import json
import time

import fire


def read(filename, start_line_idx):
    with open(filename) as f:
        lines = []
        for n, line in enumerate(itertools.islice(f, start_line_idx, None), start=1):
            lines.append(json.loads(line.strip()))
    next_start_line_idx = start_line_idx + n
    return lines, next_start_line_idx


def main(
    input_file="./price.jsonl",
    state_file="./state.json",
    start_line_idx=0,
    freq=8,
):
    while True:
        lines, start_line_idx = read(input_file, start_line_idx)
        Path(state_file).write_text(
            json.dumps(
                {
                    "input_filename": input_file,
                    "start_line_idx": start_line_idx,
                    "freq_seconds": freq,
                }
            )
        )
        print(f"Next line: {start_line_idx}")
        time.sleep(freq)


if __name__ == "__main__":
    fire.Fire(main)
