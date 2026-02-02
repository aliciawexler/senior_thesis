'''
This file takes a csv file of sequences and turns each into a yaml file in a new directory that's in the same directory as the csv file. This file turns your sequence into an all-alanine sequence that is 2 residues
longer than the actual sequence. This is for the addition of terminal NHE and ACE caps. Each yaml file is named "sequence_<csv_line_number>.yaml".

Setup of yaml file:

Version: <csv line #>

sequences:
  - protien:
      id: A
      sequence: <Each number is represented as an A>
      msa: empty 
      modifications: 
        - position: <position number>
          ccd: <'B3A' for 4 and '0W6' for 5>
        -<other mods>
EDITS:
Line 28: Add the non-canonical amino acid's CCD code to the mod_map if not already there. Make sure the character matches what's in your sequences.
Line 33: Change <OUTPUT> to the desired output directory name
Line 70: Change <CSV> to the input csv name
'''

import csv
import yaml
import os

mod_map = {
    'B': 'B3A',
    'D': 'DAL'
}

def convert_line_to_yaml(line, index, output_dir="<OUTPUT>"):
    sequence_alone = ''.join(['A' for _ in line.strip()])  # Replace each number with 'A', add 2 additional As to the sequence
    numResidues = len(line)
    sequence = sequence_alone +"AA"
    modifications = []
    modifications.append(f"        - position: 1\n          ccd: 'ACE'")
    for pos, val in enumerate(line.strip()):
        if val in mod_map:
            modifications.append(f"        - position: {pos+2}\n          ccd: '{mod_map[val]}'")
    modifications.append(f"        - position: {numResidues+2}\n          ccd: 'NH2'")
    # Build YAML string manually, remove first line when done with first run through
    yaml_string = f"""Original Sequence: {line}
Version: {index+1}

sequences:
  - protein:
      id: A
      sequence: {sequence}
      msa: empty
      modifications:
"""
    if modifications:
        yaml_string += '\n'.join(modifications)
    else:
        yaml_string += "        []"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"sequence_{index+1}.yaml")
    with open(output_file, 'w') as f:
        f.write(yaml_string)

def process_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader):
            line = ''.join(row)  # Flatten row into a string
            convert_line_to_yaml(line, index)

process_csv("<CSV>.csv")
print("Done!")

