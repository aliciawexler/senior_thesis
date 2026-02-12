# General Overview
In this folder, you will find resources for running MD on a single sequence and running MD on a batch (your batch of boltz predictions). It is reccomended that you run MD individually before running a large batch for troubleshooting. Each simulation takes 6-8 hours with the provided min.in and production.in simulation files, which first minimize the molecule over 1000 steps (half steepest descent, half conjugate gradient) in a vaccum (min.in) before simulating the equilibriation of the molecule at 37C for 200 ns, taking a frame every nanosecond.

Before working in your terminal, make sure to run these two commands to activate any ambertools you may require: 

module --ignore-cache load <wherever you downloaded amber>/AMBER/2024_mpicuda

source /<wherever you downloaded amber>/AMBER/2024/amber24/amber.sh

## Workflow 1: Custom Residue Generation and Processing
Steps 4 and 5 (const.py editing and custom ccd generation) should be done after MD, as MD processing relies on your custom residue's name in the .mol2 file you create of it aligning with the typical ccd component you're analyzing that appears in Boltz-1 from the yaml files. However, it is beneficial to consult atom naming conventions, as it will save a lot of time pre-training if your custom residue's atoms don't have to be renamed later. The provided examples are not from completing these steps in parallel at all, which is why some of the atom names from the first section(before these steps) differ from their corresponding atom names in those steps.
### 1. Create your residue in Avogadro
Avogadro software: https://avogadro.cc/
This is a 3D molecular editing software. Use it to build your residue, and make sure to cap the C-terminus with NH2(also reffered to as NHE in some documents) and the N-terminus with an acetyl group(ACE). Save it as a .mol2 file and make sure the name is exactly 3 characters long. This should be the same name as the CCD component you predicted Boltz with during the "sequence_prep" steps(found in your .yaml files). 
### 2. Labeling atoms
Open the .mol2 file in a text editor. On line 2, replace the string of asteriks with the 3-letter name you've given your residue. Keep your 3D molecule up on Avogadro and label each atom by number (on Avogadro, click "Display Settings..." in the upper toolbar --> check "Label" under "Display Types" --> click the wrench icon next to "label" to open label settings --> In the box labeled "Atom Labels", change the "Text" field to "Atom Number"). Then, add unique atom names no longer than 3 characters to the mol2 file and ensure they correlate with your atom numbers in Avogadro. It may be helpful to make sure these atom names align with the default ccd names of your residue, if those exist(see step 5: Custom CCD generation for more information). Make sure all atom types and connections are correct in the .mol2 file.
In the "AMBER_MD/Custom_Residue_Examples" directory, there is an example of this editing for the DAL residue. The original .mol2 file is called "DAL.mol2.original" and the labeled file is called "DAL.mol2".
For future processing purposes(alignment with provided prepgen.in file), some specific atoms must be given the following standardized names:

| Portion of .mol2 file | Atom | Mandatory Name |
| ------------- | ------------- | ------------- |
| Residue | Nitrogen | N |
| Residue | Carbonyl Carbon | C |
| Residue | Alpha Carbon | CA |
| NH2(aka NHE) | Nitrogen | NHE |
| NH2(aka NHE) | Hydrogen 1 | HN1 |
| NH2(aka NHE) | Hydrogen 2 | HN2 |
| ACE | Hydrogen 1 | HC1 |
| ACE | Hydrogen 2 | HC2 |
| ACE | Hydrogen 3 | HC3 |
| ACE | Sp3 Carbon | CAC |
| ACE | Oxygen | OAC |
| ACE | Carbonyl Carbon | C1 |

### 3. Processing your .mol2 file with ambertools
Run the commands at the top of the page in your terminal before starting. 
1. Run this command, replacing the "residue name" portions with the 3-letter name you've given your residue: 
  antechamber -i <residue name>.mol2 -fi mol2 -o <residue name>.ac -fo ac -c bcc -nc 0
    After running this, ensure the .ac file is correct(example for DAL is in the examples directory).
2. Then, run this command similarly: 
  parmchk2 -i <residue name>.ac -f ac -o <residue name>.frcmod
3. Edit the "residue_name.prepgen.in" file by changing "residue_name" to your residue 3-letter name, ensuring all of the prepgen.in atom names align with your residue's atom names (if your residue was not given the standardized names specified in step 2: labeling atoms), and adding any other main_chain atoms to the file as such (if your residue is not an alpha-amino acid): 
...
MAIN_CHAIN CA # Alpha Carbon
MAIN_CHAIN CB # Beta Carbon
MAIN_CHAIN CG # Gamma Carbon
OMIT_NAME HN1 # Omit NHE hydrogen 1
...
4. Run this command:
  prepgen -i <residue name>.ac -o <residue name>.prepin -f prepin -m <residue name>.prepgen.in
    Check the name on the .prepin file, which  should be the first 3 letters of the line above the line starting with “CORRECT”. Make sure this is your residue name.

After completing these steps, when you run tleap for the first time during workflow 2, you will most likely find errors/warnings stating that there are missing bonds, angles, or torsions. This is mostly just because the names of your custom residue atoms are lowercase gaff letters, and the names of the cannonical residue atoms are uppercase ff14SB letters, so you need to parameterize the interactions between the two. These must be added to the .frcmod, in this case, they originate from the gaff2.dat file found in the Sources directory as well as the "AMBER/2024/amber24/dat/leap/parm" directory located wherever you installed AMBER.

It is reccomended that you pause here and complete workflows 2 and/or 3 and simulation processing up through centriod PDB collection before returning to steps 4 and 5. 

### 4. Const.py editing
At this point, you must choose a different 3-letter code for your residue. It should NOT be included in the "components.cif" file already(or have the same 3-letter code as any cannonical residue), see the "unused_3letter_acronyms" spreadsheet for a list of 953 unused candidates. You must also pick a token to represent it as a unique one-letter code(not used for any other amino acid). This workflow has only been tested with letters as one-letter codes, ***
### 5. Custom CCD generation
Each custom residue will need its own respective ccd.pkl entry, created by adding entries to the "components.cif" for each residue and processing that file with ccd.py. You will most likely be able to find your residue on the wwPDB Chemical Component Dictionary or even the default components.cif file, and it is best to copy values from these standard entries. You may have to change the atom names, it is easiest to look at the bonds at the bottom of the entry, draw out the molecule, compare with your own atom names, and fix atom names accordingly. You can also use the "modify_pdbs.py" script to fix your atom names to fit the CCD data(after MD processing). If you made any mistakes in your atom naming for MD, this is an ideal opportunity to fix that. Examples are provided in the "Custom_Residue_Examples" folder(DAL-->DJA and B3A-->BBD).

## Workflow 2: Individual MD processing
### 1. Make directories for MD
Make a directory called "MD", cd into that directory, and then make a directory for your specific MD job and cd into the job directory you just made.
### 2. Load AMBER and AMBER profiles
Before moving forward, make sure you've run both of these commands on your terminal: 
module --ignore-cache load <wherever you downloaded amber>/AMBER/2024_mpicuda

source /<wherever you downloaded amber>/AMBER/2024/amber24/amber.sh
### 3. Upload Files
Add the following files to your job directory:
1. pdb of the sequence you'd like to perform AMBER on(from initial Boltz-1 prediction)
2. .frcmod and .prepin files for your unnatural residues
3. .in files for MD simulation (examples provided in MD_unchanged directory, should have at least 1 minimization file(min.in) and 1 production file(production.in))
4. tleap.in (see tleap_single.in for instructions and example, do NOT use tleap.in in the MD_change directory for guidance).
5. run.sh (see run.sh in the MD_change folder for an example using only min.in and production.in simulation input files)
6. MD_submit.job (see MD_submit.job for example)
  -For this, you will need to set up your own CPU configuration and include the module and source commands for amber loading. 
### 4. Simple Commands
Run these commands in order:
1. pdb4amber -i <sequence_name>.pdb -o <sequence-name>_amber.pdb
2. tleap -f tleap.in
3. sbatch MD_submit.job

## Workflow 3: Batch MD processing
### 1. Make directories for MD
Make a directory called "MD" and cd into that directory. Then, make two directories called "MD_change" and MD_unchanged" as well as a directory for your MD simulation outputs. Put these 3 directories into the "MD" directory.
### 2. File organization
To the MD_change directory, add your tleap.in, run.sh, and MD_submit.job files (found in the MD_change folder in this repo). To the MD_unchanged directory, add the .frcmod and .prepin files from your unnatural residues and your .in files for MD simulation. Make sure the "tleap.in" file has all of the lines necessary to load your unnatural amino acid .frcmod and .prepin files. You do not need to add any sequence or amber lines for this file, as the batch script does that for you. There should be a minimum of 1 empty line between the end of your amino acid loading and "quit".
### 3. Load AMBER and AMBER profiles
Before moving forward, make sure you've run both of these commands on your terminal: 
module --ignore-cache load <wherever you downloaded amber>/AMBER/2024_mpicuda

source /<wherever you downloaded amber>/AMBER/2024/amber24/amber.sh
### 4. MD_batch script modification and run
This script runs MD on your batch of boltz outputs. Note that this script is written to process a directory of predictions with the following title structure: "boltz_results_sequence_<number>/predictions/sequence_<number>/sequence_<number>.pdb". It also assumes your "MD_change" and "MD_unchanged" directories, as well as the "tleap.in", "MD_submit.job" and "run.sh" files are named as such. It will create an "MD_<sequence_number>" directory for each sequence it processes in the directory you made in step 1 for your simulation outputs. It does NOT allow for repeated submissions; if you need to re-run MD on a specific sequence, you must delete the original MD folder for that specific sequence or move it out of the output directory. See the file itself for necessary edits. Place the script in whatever directory contains your "MD" directory and run with "python MD_batch.py". It is reccomended that you run this script in a tmux session and on a virtual CPU, especially if you will be submitting 100+ structures.

## After MD: Verification
Look at a few of your MD outputs in PyMOL with the commands "load sequence_<sequence_number>_amber.parm7" and "load_traj md_<sequence_number>.nc". Make sure you're in a directory where those files are visible to PyMOL. Show as sticks, play the simulation as a video, and ensure all of the geometries are correct.
