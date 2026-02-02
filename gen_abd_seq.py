#!/usr/bin/env python3
import csv
from itertools import product

ALPHABET = ("D", "A")
LENGTH = 10
WINDOW = 10  # subsequence length to enforce uniqueness


def windows(seq: str, k: int):
    for i in range(len(seq) - k + 1):
        yield seq[i : i + k]


def main() -> None:
    seen_xmers = set()
    kept = 0

    with open("abd_test10.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # Deterministic order: lexicographic by ALPHABET order (D, A, B)
        for tup in product(ALPHABET, repeat=LENGTH):
            seq = "".join(tup)

            seq_xmers = list(windows(seq, WINDOW))
            # Omit if ANY x-mer in this sequence was seen before
            if any(sx in seen_xmers for sx in seq_xmers):
                continue

            # Keep: write and record its x-mers as now "used"
            w.writerow([seq])
            kept += 1
            seen_xmers.update(seq_xmers)

    alphabet_str = ",".join(ALPHABET)
    print(f"Total possible {LENGTH}-mers over {{{alphabet_str}}}: {len(ALPHABET) ** LENGTH:,}")
    print(f"Sequences kept after linear {WINDOW}-mer filter: {kept:,}")


if __name__ == "__main__":
    main()

