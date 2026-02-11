# General Overview
In this folder, you will find resources for running MD on a single sequence and running MD on a batch (your batch of boltz predictions). It is reccomended that you run MD individually before running a large batch for troubleshooting.
Before working in your terminal, make sure to run these two commands to activate any ambertools you may require: 

module --ignore-cache load share_modules/AMBER/2024_mpicuda

source /share/software/scisoft/AMBER/2024/amber24/amber.sh

## Workflow 1: Custom Residue Generation and Processing
It is possible to skip steps 4 and 5 (const.py editing and custom ccd generation) before MD, but completing them in parallel will save a lot of time and editing in the future. The provided examples are not from completing these steps in parallel, which is why some of the atom names from the first section(before these steps) differ from their corresponding atom names in those steps.
### 1. Create your residue in Avogadro
Avogadro software: https://avogadro.cc/
This is a 3D molecular editing software. Use it to build your residue, and make sure to cap the C-terminus with NH2(also reffered to as NHE in some documents) and the N-terminus with an acetyl group(ACE). Save it as a .mol2 file and make sure the name is exactly 3 characters long. This is your residue name. For best practice, it should NOT be included in the "components.cif" file already(or have the same 3-letter code as any cannonical residue), see the "unused_3letter_acronyms" spreadsheet for a list of 953 unused candidates.
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

After completing these steps, when you run tleap for the first time during workflow 2, you will most likely find errors/warnings stating that there are missing bonds, angles, or torsions. These must be added to the .frcmod 

### 4. Const.py editing

### 5. Custom CCD generation
Each custom residue will need its own respective ccd.pkl entry, created by adding entries to the "components.cif" for each residue and processing that file with ccd.py. You will most likely be able to find your residue on the wwPDB Chemical Component Dictionary or even the default components.cif file, and it is best to copy values for the _chem_comp_atom.model_Cartn_* (coordinate) columns from these standard entries. You may have to change the atom names, it is easiest to look at the bonds at the bottom of the entry, draw out the molecule, compare with your own atom names, and fix atom names accordingly. You can also use the "modify_pdbs.py" script to fix your atom names to fit the CCD data. If you made any mistakes in your atom naming for MD, this is an ideal opportunity to fix that. Examples are provided in the "Custom_Residue_Examples" folder(DAL-->DJA and B3A-->BBD).
If your residue does not have 

## Workflow 2: Individual MD processing
### 1. Make a directory for MD
### 2. Load AMBER and AMBER profiles
Run the following commands in your terminal

## Workflow 3: Batch MD processing
### 1. Make a directory for MD
This directory should be in the same directory as your yaml/boltz output directory
