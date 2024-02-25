from typing import Optional
from dataclasses import dataclass
import time
import json

import fire
from rich.align import Align
from rich.live import Live
from rich.table import Table
from file_read_backwards import FileReadBackwards


@dataclass
class Row:
    timestamp: Optional[str] = None
    diff: Optional[float] = None
    value: Optional[float] = None

    @classmethod
    def from_json(cls, s: str) -> "Row":
        record = json.loads(s.strip())
        return cls(timestamp=record["timestamp"], value=float(record["value"]))

    @property
    def value_fmt(self):
        if self.value is None:
            return "[khaki3]None"
        return "[khaki3]{:10.2f}".format(self.value)

    @property
    def diff_fmt(self):
        if self.diff is None:
            return "[yellow]None"

        if self.diff == 0:
            arrow = "-"
            color = "yellow"
        elif self.diff < 0:
            arrow = "↑"
            color = "green"
        else:
            arrow = "↓"
            color = "red"
        return f"[{color}]{arrow} {'{:10.5f}'.format(self.diff)}"


def read_n_lines_from_bottom_to_top(filename, n):
    with FileReadBackwards(filename, encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            yield line
            if i == n:
                return


def update_diffs(rows: list[Row]):
    """Update diffs in place"""
    # Iterate from new to old (top to bottom of the table)
    for row, last_row in zip(rows, rows[1:]):
        row.diff = 100 * (last_row.value - row.value) / last_row.value


def make_table(filename, n_rows) -> Table:
    table = Table(title="Live Bitcoin Price")
    table.add_column("[light_cyan1]Timestamp", no_wrap=True, vertical="middle")
    table.add_column("[khaki3]Value (USD)", vertical="middle")
    table.add_column("Δ%", vertical="middle")

    # Read one more line than we need to display for last row to have a valid value
    lines = read_n_lines_from_bottom_to_top(filename, n=n_rows + 1)
    rows = [Row.from_json(line) for line in lines]
    update_diffs(rows)

    for row in rows[:-1]:  # Don't render the last one
        table.add_row(f"[light_cyan1]{row.timestamp}", row.value_fmt, row.diff_fmt)
    return table


def render(filename, n_rows):
    return Align.center(make_table(filename, n_rows))


def main(filename: str, rows: int = 10):
    with Live(render(filename, rows), refresh_per_second=1, screen=True) as live:
        while True:
            live.update(render(filename, rows))
            time.sleep(0.5)


if __name__ == "__main__":
    fire.Fire(main)
