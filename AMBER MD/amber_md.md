# General Overview
In this folder, you will find resources for running MD on a single sequence and running MD on a batch (your batch of boltz predictions). It is reccomended that you run MD individually before running a large batch for troubleshooting.
## Workflow 1: Custom Residue Generation and Processing
### 1. Create your residue in Avogadro
Avogadro software: https://avogadro.cc/
This is a 3D molecular editing software. Use it to build your residue, and make sure to cap the C-terminus with NH2 and the N-terminus with an acetyl group. Save it as a .mol2 file and make sure the name is exactly 3 characters long. This is your residue name. For best practice, it should NOT be included in the "components.cif" file already, see the "unused_3letter_acronyms" spreadsheet for a list of candidates.
### 2. Labeling atoms
Open the .mol2 file in a text editor. Keep your 3D molecule up on Avogadro and label each atom by number (on avogadro). Then, add labels to the residue and ensure they correlate with your atom numbers. Give each atom a unique an appropriate name no longer than 3 characters. Make sure all atom types and connections are correct.
*more stuff*
### 3. Const.py editing

### 4. Custom CCD generation
Each custom residue will need its own respective ccd.pkl entry, created by adding entries to the "components.cif" for each residue and processing that file with ccd.py. You will most likely be able to find your residue on the wwPDB Chemical Component Dictionary or even the default components.cif file, and it is best to copy values for the _chem_comp_atom.model_Cartn_* (coordinate) columns from these standard entries. You may have to change the atom names, it is easiest to look at the bonds at the bottom of the entry, draw out the molecule, compare with your own atom names, and fix atom names accordingly. You can also use the "modify_pdbs.py" script to fix your atom names to fit the CCD data. If you made any mistakes in your atom naming for MD, this is an ideal opportunity to fix that. Examples are provided in the "Custom_Residue_Examples" folder(DAL-->DJA and B3A-->BBD).


## Workflow 2: Individual MD processing
### 1. Make a directory for MD
### 2. Load AMBER and AMBER profiles
Run the following commands in your terminal

## Workflow 3: Batch MD processing
### 1. Make a directory for MD
This directory should be in the same directory as your yaml/boltz output directory