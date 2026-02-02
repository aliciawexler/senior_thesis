'''
This file allows a user to specify a number of backbone atoms in an alpha/beta-amino acid-containing peptidomimetic, then generates all possible combinations of the two
and writes them to a file specified by the filename parameter of the export_sequences_streamed() function. Portions that are commented out can be added in, if desired,
to add gamma amino acids to the combinations.

IMPORTANT NOTE: You MUST change "<CSV OUTPUT>" on line 52 to the name of your desired CSV file
'''
import csv
import itertools
from more_itertools import distinct_permutations
from tqdm import tqdm

# Amino acid backbone atom counts, replace with commented out version for gamma
atom_counts = {'3': 3, '4': 4} #{'3': 3, '4': 4, '5': 5}
target_atoms = 48

#remove comment for gamma
def arrangements(n):
    if n<3:
        return 0
    if n ==3:
        return 1
    if n==4:
        return 1
    #if n==5:
    #    return 1
    return arrangements(n-3)+ arrangements(n-4) #+ arrangements(n-5)

numArr = (arrangements(target_atoms))
'''
#Alpha/beta/gamma combinations
def generate_combinations():
    combos = []
    for a in range(target_atoms // atom_counts['3'] + 1):
        for b in range(target_atoms // atom_counts['4'] + 1):
            for g in range(target_atoms // atom_counts['5'] + 1):
                total = a * atom_counts['3'] + b * atom_counts['4'] + g * atom_counts['5']
                if total == target_atoms:
                    combos.append((a, b, g))
    return combos
'''
#Alpha/beta combinations
def generate_combinations():
    combos = []
    for a in range(target_atoms // atom_counts['3'] + 1):
        for b in range(target_atoms // atom_counts['4'] + 1):
            total = a * atom_counts['3'] + b * atom_counts['4']
            if total == target_atoms:
                combos.append((a, b))
    return combos
#Change "<CSV OUTPUT>" to the desired CSV output
def export_sequences_streamed(combos, filename='<CSV OUTPUT>'):
    print(f"Streaming sequences to {filename}...")
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(['Sequence'])
        #for a, b, g in tqdm(combos, desc="Processing combos"):
        for a, b in tqdm(combos, desc="Processing combos"):
            sequence = '3' * a + '4' * b #+ '5' * g
            for p in distinct_permutations(sequence):
                writer.writerow([''.join(p)])
    print("Done!", numArr, "combinations produced!")

def main():
    combos = generate_combinations()
    export_sequences_streamed(combos)

if __name__ == "__main__":
    main()

