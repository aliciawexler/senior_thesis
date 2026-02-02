# senior_thesis
Modification of Boltz-1 software for the prediction of non-canonical amino acid-containing peptidomimetics

## Workflow steps: 
### 1. Generation of Peptide Sequences
The Boltz training requires a wide slew of peptide sequences to train on, and thus there are two generation options to choose from, each of which produces thousands of randomized sequences for training. These options are always written to a csv file. Options are as follows: 
1. helix.py: Given a number of backbone atoms, the script generates all possible combinations of alpha/beta-amino acid sequences. By switching the parts that are commented out, users can also include gamma amino acids.
2. 
