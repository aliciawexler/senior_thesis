# senior_thesis
Modification of Boltz-1 software for the prediction of non-canonical amino acid-containing peptidomimetics

## Workflow steps: 
### 1. Generation of peptide sequences (CSV)
The Boltz training requires a wide slew of peptide sequences to train on, and thus there are a few generation options to choose from, each of which produces thousands of randomized sequences for training. These options are always written to a csv file of your choosing. You may also choose to create your own generation script if none of these options work for your sequence generation. Options are as follows: 
   1. helix.py: Given a number of backbone atoms, the script generates all possible combinations of alpha/beta-amino acid sequences. By switching the parts that are commented out, users can also include gamma amino     acids.
   2. gen_sequences_no_cyc_red.py: Given a number of residues, a collection of amino acid one-letter codes, and a linear redundancy filter length, the script generates all possible sequences of the amino acids but omits any cyclic repeats or linear repeats of the length you specifiy.
   3. gen_seq.py: Same as gen_sequences_no_cyc_red.py but keeps cyclic redundancies. 
For more detailed information on these scripts and their use, see their header comments.
### 2. Translation of sequences to yaml input files


