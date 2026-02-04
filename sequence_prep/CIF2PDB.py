'''
This file turns the .cif files output by boltz-1 into .pdb files, and corrects any NH2 atom namings to NHE for compatibility with downstream tools. It also contains some
atom renamings for custom residues 0W6(gamma-alanine) and B3A(beta-alanine) to match downstream custom atom namings, but this may not be necessary for your use case, as
the DAL(D-alanine) custom residue did not need to have any atom renamings.
EDITS:
Line ~91: Set <path_to_your_yaml_and_boltz_directory> to the path containing your boltz-1 output directories(base_boltz_dir).
FOR CUSTOM RESIDUES:
Line ~20: Add any necessary atom renamings in the same style as rename_0W6 and rename_B3A for your custom residues. For guidance in this process, see the "custom residue" 
folder in the MD directory. Make sure all atom names are 3 characters long, with spaces added to the right as necessary.
Line ~48: Add any necessary renaming dictionaries to the fix_nh2_atom_in_pdb function in the same style as the other renamings. A commented out template is provided 
in the method, just change the <3-letter_code> to the code of your residue (MAKE SURE TO KEEP THE SPACE BEFORE!! For example, if your residue code is "XYZ", atom_res
should be " XYZ"), and <custom_rename_dict> to the name of your renaming dictionary.
'''

import os
from Bio.PDB import MMCIFParser, PDBIO

rename_0W6= {"CA ":"C  ", "C16":"C1 ", "C17":"C2 ", "C18":"C3 ", "C  ":"C4 "}
rename_B3A= {"CG ":"C  ", "CA ":"C1 ", "CB ":"C2 ", "C  ":"C3 "}

def convert_cif_to_pdb(cif_file, pdb_file):
    parser = MMCIFParser(QUIET=True)
    structure_id = os.path.splitext(os.path.basename(cif_file))[0]
    structure = parser.get_structure(structure_id, cif_file)
    
    io = PDBIO()
    io.set_structure(structure)
    io.save(pdb_file)

def fix_nh2_atom_in_pdb(pdb_path):
    with open(pdb_path, 'r') as f:
        lines = f.readlines()

    modified_lines = []
    changed = False

    for line in lines:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            atom_code = line[13:16]
            atom_res = line[16:20]
            print(atom_code)
            if atom_res == " 0W6" and atom_code in rename_0W6:
                line = line[:13] + rename_0W6[atom_code] + line[16:]
                print(rename_0W6[atom_code])
            elif atom_res == " B3A" and atom_code in rename_B3A:
                line = line[:13] + rename_B3A[atom_code] + line[16:]
                print(rename_B3A[atom_code])
            '''
            elif atom_res == " <3-letter_code>" and atom_code in <custom_rename_dict>:
                line = line[:13] + <custom_rename_dict>[atom_code] + line[16:]
                print(<custom_rename_dict>[atom_code])
            '''
            atom_name = line[16:20]
            if atom_name == " NH2":
                line = line[:16] + " NHE" + line[20:]
                changed = True
        modified_lines.append(line)

    if changed:
        print(f"→ Replaced NH2 with NHE in: {pdb_path}")
    else:
        print(f"→ No NH2 atoms found in: {pdb_path}")

    with open(pdb_path, 'w') as f:
        f.writelines(modified_lines)

def batch_process_boltz_predictions(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            pred_path = os.path.join(root, d, "predictions")
            if os.path.isdir(pred_path):
                nested_dirs = [os.path.join(pred_path, ndir) for ndir in os.listdir(pred_path)
                               if os.path.isdir(os.path.join(pred_path, ndir))]
                for nested_dir in nested_dirs:
                    cif_files = [f for f in os.listdir(nested_dir) if f.endswith(".cif")]
                    for cif in cif_files:
                        cif_path = os.path.join(nested_dir, cif)
                        pdb_name = cif.replace("_model_0.cif", ".pdb")
                        pdb_path = os.path.join(nested_dir, pdb_name)

                        # Delete old PDB if it exists
                        if os.path.exists(pdb_path):
                            os.remove(pdb_path)

                        # Step 1: Convert CIF to PDB
                        convert_cif_to_pdb(cif_path, pdb_path)

                        # Step 2: Fix NH2 atom in PDB
                        fix_nh2_atom_in_pdb(pdb_path)

base_boltz_dir = "<path_to_your_yaml_and_boltz_directory>"
batch_process_boltz_predictions(base_boltz_dir)
