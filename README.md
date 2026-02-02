# senior_thesis
Modification of Boltz-1 software for the prediction of non-canonical amino acid-containing peptidomimetics
## Initial Requirements
-You must have a conda environment that has boltz installed, and you must also have a cache directory that contains the boltz-1 ccd.pkl. Visit the boltz official directory for more information.

-You must have access to at least one decent GPU and many (300+) CPU resources
## Workflow steps: 
### 1. Generation of peptide sequences (CSV)
The Boltz training requires a wide slew of peptide sequences to train on, and thus there are a few generation options to choose from, each of which produces thousands of randomized sequences for training. These options are always written to a csv file of your choosing. You may also choose to create your own generation script if none of these options work for your sequence generation. Options are as follows: 
   1. helix.py: Given a number of backbone atoms, the script generates all possible combinations of alpha/beta-amino acid sequences. By switching the parts that are commented out, users can also include gamma amino     acids.
   2. gen_sequences_no_cyc_red.py: Given a number of residues, a collection of amino acid one-letter codes(doesn't have to be the actual one-letter code, this step only processes it like a letter), and a linear redundancy filter length, the script generates all possible sequences of the amino acids but omits any cyclic repeats or linear repeats of the length you specifiy.
   3. gen_seq.py: Same as gen_sequences_no_cyc_red.py but keeps cyclic redundancies. 
For more detailed information on these scripts and their use, see their header comments.
### 2. Translation of sequences to yaml input files
Boltz predicts with .yaml files as inputs, so we need to turn our .csv file of sequences into a directory of .yaml inputs(in the same directory as your .csv file). As long as your sequences have no other canonical amino acids but alanine, use the script "generate_yaml.py" to do this. Each resulting yaml file will be uniquely named by the line number of the sequence in the .csv file, and the sequences will be capped with an acetyl group on the n-terminus and an nh2 cap on the c-terminus.
### 3. Boltz-1 initial structure predictions
Boltz-1 cannot accurately predict the structures of non-canonical amino acid-containing peptidomimetics, but does provide an ideal template for MD simulations later. Use the provided run_initial_predictions.job file to loop through your yaml file directory and create boltz_results_sequence_<sequence_number> directories in the same directory as your yaml files, or write your own, as long as the directory name is the same.

