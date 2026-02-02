'''
This file generates all possible sequences of a specified length of the amino acids represented by their one-letter codes in "ALPHABET" after omitting cyclic redundancies. Cyclic redundancies are sequences that 
are the same when the ends are ignored, such that if sequence "ABD" has already been generated, "BDA" will be omitted as a cyclic redundancy. Optionally, by setting "WINDOW" to an integer less than "LENGTH", 
you may also omit sequences containing repeated motifs as long as that window, such that for LENGTH=3 and WINDOW=2, if "ABD" has already been generated, "DAB" will be ommitted due to its repeated "AB" motif.
All sequences are saved to a csv file of your specification.
EDITS:
Line 17: Edit the one-letter codes in ALPHABET to include all of the amino acids and only the amino acids you'd like to generate sequences of.
Line 19: Set LINEAR to your desired sequence length
Line 21: Set WINDOW to your desired linear motif length (or set to the same integer as LENGTH if you'd rather not use the WINDOW feature)
Line 39: Set <CSV> to the name of your desired csv output file
'''

#!/usr/bin/env python3
import csv
from itertools import product

ALPHABET = ("D", "A", "B")
#LENGTH = length of peptide
LENGTH = 10
#Sequences containing motifs of length WINDOW that have already been produces are omitted
WINDOW = 10

def min_rotation(s: str) -> str:
    """Lexicographically smallest rotation (rotation-only cyclic equivalence)."""
    return min(s[i:] + s[:i] for i in range(len(s)))

def linear_windows(s: str, k: int):
    """All contiguous k-mers without wraparound."""
    for i in range(len(s) - k + 1):
        yield s[i:i+k]

def main() -> None:
    total = len(ALPHABET) ** LENGTH
    seen_cyclic = set()   # canonical cyclic reps we've already kept/considered
    seen_xmers = set()    # globally used linear WINDOW-mers among sequences written
    kept = 0
    cyclic_unique = 0

    with open("<CSV>.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sequence"])  # keep it simple

        for tup in product(ALPHABET, repeat=LENGTH):
            seq = "".join(tup)

            # 1) Remove cyclic redundancies (rotation classes)
            canon = min_rotation(seq)
            if canon in seen_cyclic:
                continue
            seen_cyclic.add(canon)
            cyclic_unique += 1

            # 2) Linear WINDOW-mer filter (NO wraparound)
            seq_xmers = list(linear_windows(seq, WINDOW))
            if any(sx in seen_xmers for sx in seq_xmers):
                continue

            w.writerow([seq])
            kept += 1
            seen_xmers.update(seq_xmers)

    print(f"Total possible {LENGTH}-mers over {{D,A,B}}: {total:,}")
    print(f"Unique after cyclic (rotation) dedup: {cyclic_unique:,}")
    print(f"Kept after linear {WINDOW}-mer filter: {kept:,}")


if __name__ == "__main__":
    main()

