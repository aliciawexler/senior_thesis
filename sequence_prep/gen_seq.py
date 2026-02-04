'''
This file generates all possible sequences of a specified length of the amino acids represented by their one-letter codes in "ALPHABET". Optionally, by setting "WINDOW" to an integer less than "LENGTH", 
you may also omit sequences containing repeated motifs as long as that window, such that for LENGTH=3 and WINDOW=2, if "ABD" has already been generated, "DAB" will be ommitted due to its repeated "AB" motif.
All sequences are saved to a csv file of your specification.
EDITS:
Line 15: Edit the one-letter codes in ALPHABET to include all of the amino acids and only the amino acids you'd like to generate sequences of.
Line 16: Set LINEAR to your desired sequence length
Line 17: Set WINDOW to your desired linear motif length (or set to the same integer as LENGTH if you'd rather not use the WINDOW feature)
Line 29: Set <CSV> to the name of your desired csv output file
'''
#!/usr/bin/env python3
import csv
from itertools import product

ALPHABET = ("D", "A")
LENGTH = 10  #length of sequences
WINDOW = 10  # subsequence length to enforce uniqueness


def windows(seq: str, k: int):
    for i in range(len(seq) - k + 1):
        yield seq[i : i + k]


def main() -> None:
    seen_xmers = set()
    kept = 0

    with open("<CSV>.csv", "w", newline="", encoding="utf-8") as f:
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

