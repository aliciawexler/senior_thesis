#!/usr/bin/env python3
import csv
from itertools import product

ALPHABET = ("D", "A", "B")
LENGTH = 10
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
    seen_7mers = set()    # globally used linear 7-mers among sequences written
    kept = 0
    cyclic_unique = 0

    with open("hmm.csv", "w", newline="", encoding="utf-8") as f:
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

            # 2) Linear 7-mer filter (NO wraparound)
            seq_7mers = list(linear_windows(seq, WINDOW))
            if any(s7 in seen_7mers for s7 in seq_7mers):
                continue

            w.writerow([seq])
            kept += 1
            seen_7mers.update(seq_7mers)

    print(f"Total possible 12-mers over {{D,A,B}}: {total:,}")
    print(f"Unique after cyclic (rotation) dedup: {cyclic_unique:,}")
    print(f"Kept after linear 7-mer filter: {kept:,}")

if __name__ == "__main__":
    main()

