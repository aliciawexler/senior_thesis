'''
This script sets up and submits MD simulations for a directory of predicted PDB structures(yaml_output_dir). It can be run on the whole directory,
or on specific target sequences, given that your predictions are in the format 
"boltz_results_sequence_<number>/predictions/sequence_<number>/sequence_<number>.pdb"). 
If you would like to run on specific sequences, set USE_FILTER_LIST to True and populate TARGET_SEQUENCES with the sequence numbers you want to 
process (as strings).

Edits:
Line 38: Set <your_yaml_output_dir> to the directory where your prediction PDBs are located.
Line 44: Set <your_desired_MD_output_dir> to the name of the directory where you want the MD setup directories to be created. Each sequence will have its own 
subdirectory named "MD_sequence_<number>".
Line 123: Ensure that '<number>' is set to an integer value(do NOT keep as a string) that matches an empty line in your tleap.in file below your lines
loading your residues and before "quit". Keep in mind that lines are 0-indexed, so if you want to insert at line 18, you should set this to 17.
Lines 146 and 147: Ensure the *run.sh* lines match the names of your minimization and production input files. If you have more steps, adjust accordingly.
'''
import os
import shutil
import subprocess
import re

# ==========================================
# CONFIGURATION: FILTER SPECIFIC SEQUENCES
# ==========================================
# Set this to True to run only the sequences in the list below.
# Set this to False to run on ALL sequences found in the directory.
USE_FILTER_LIST = False

# List of sequence numbers to process (as strings)
TARGET_SEQUENCES = [
    "403", "537" #example sequence numbers; replace with your actual target sequence numbers
]
# ==========================================

# Save starting directory
starting_dir = os.getcwd()

# Set base directories
yaml_output_dir = "<your_yaml_output_dir>" 
md_base_dir = "MD"
md_template_dir = os.path.join(md_base_dir, "MD_unchanged")
md_change_dir = os.path.join(md_base_dir, "MD_change")

# Parent directory for output files:
md_output_parent_dir = os.path.join(md_base_dir, "<your_desired_MD_output_dir>")
os.makedirs(md_output_parent_dir, exist_ok=True)

for dir_name in os.listdir(yaml_output_dir):
    if not re.fullmatch(r"boltz_results_sequence_(\d+)", dir_name):
        continue
    
    pred_dir = os.path.join(yaml_output_dir, dir_name, "predictions")
    if not os.path.isdir(pred_dir):
        continue
    else:
        print(f"Processing predictions in: {pred_dir}")
        
    for seq_folder in os.listdir(pred_dir):
        if not seq_folder.startswith("sequence_"):
            continue
            
        sequence_num = seq_folder.split("_")[1]

        # ---------------------------------------------------------
        # FILTER LOGIC: Check if we should skip this sequence
        # ---------------------------------------------------------
        if USE_FILTER_LIST and sequence_num not in TARGET_SEQUENCES:
            # print(f"Skipping sequence {sequence_num} (not in target list)")
            continue
        # ---------------------------------------------------------

        title = seq_folder
        
        # Create MD_sequence_<sequence number> directory
        md_target_dir = os.path.join(md_output_parent_dir, f"MD_sequence_{sequence_num}")
        if os.path.exists(md_target_dir):
            print(f"Directory {md_target_dir} already exists. Skipping sequence {sequence_num}.")
            continue
        
        print(f"{title} is being worked on")
        seq_path = os.path.join(pred_dir, seq_folder)
        pdb_name = f"sequence_{sequence_num}.pdb"
        seq_pdb_path_1 = os.path.join(seq_path, pdb_name)
        seq_pdb_path = os.path.abspath(seq_pdb_path_1)
        
        os.makedirs(md_target_dir, exist_ok=True)
        
        # Copy files from MD_unchanged and MD_change into the new directory
        for src_dir in [md_template_dir, md_change_dir]:
            for file in os.listdir(src_dir):
                full_src_path = os.path.join(src_dir, file)
                # Check if it is a file before copying
                if os.path.isfile(full_src_path):
                    shutil.copy(full_src_path, md_target_dir)
                    
        # Copy and rename PDB file
        amber_pdb_name = f"sequence_{sequence_num}_amber.pdb"
        print(amber_pdb_name)
        # amber_pdb_path is defined but not strictly used for copy here, just reference
        amber_pdb_path = os.path.join(md_target_dir, amber_pdb_name)
        shutil.copy(seq_pdb_path, os.path.join(md_target_dir, pdb_name))

        os.chdir(md_target_dir)

        # Parse PDB to build residue sequence
        sequence = []
        last_resid = None
        with open(seq_pdb_path) as pdbf:
            for line in pdbf:
                if not line.startswith(("ATOM", "HETATM")):
                    continue
                parts = line.split()
                resname = parts[3]
                resid = parts[5]
                if resid != last_resid:
                    sequence.append(resname)
                    last_resid = resid

        # Update tleap.in
        tleap_path = "tleap.in"
        with open(tleap_path, "r") as f:
            lines = f.readlines()
            
        lines['<number>'] = f"full = sequence {{ {' '.join(sequence)} }}\n"
        idx = 18
        lines.insert(idx, f"saveAmberParm full sequence_{sequence_num}_amber.parm7 sequence_{sequence_num}_amber.rst7\n")
        idx += 1

        with open(tleap_path, "w") as f:
            f.writelines(lines)

        # Update submit.job
        submit_path = "MD_submit.job"
        with open(submit_path, "r") as f:
            lines = f.readlines()
        print(lines[4])
        lines[4] = f"#SBATCH --job-name=MD_sequence_{sequence_num}\n"
        print(lines[4])
        with open(submit_path, "w") as f:
            f.writelines(lines)

        # Update run.sh
        run_sh_path = "run.sh"
        with open(run_sh_path, "r") as f:
            lines = f.readlines()
        print(lines[1])
        lines[1] = f"sander -O -i min.in -o min.out -p sequence_{sequence_num}_amber.parm7 -c sequence_{sequence_num}_amber.rst7 -r min.rst7\n"
        lines[2] = f"sander -O -i production2.in -o md.out -p sequence_{sequence_num}_amber.parm7 -c min.rst7 -r md.rst7 -x md_{sequence_num}.nc\n"
        print(lines[2])
        with open(run_sh_path, "w") as f:
            f.writelines(lines)

        # Run pdb4amber, tleap, and submit job
        subprocess.run(f"""
        pdb4amber -i {pdb_name} -o {amber_pdb_name}
        """, shell=True, executable='/bin/bash')
        print("ran pdb4amber")
        
        with open(amber_pdb_name) as fin:
            pdb_lines = fin.readlines()
            
        ter_idxs = [i for i, L in enumerate(pdb_lines) if L.startswith("TER")]
        if ter_idxs:
            last_ter = ter_idxs[-1]
            cleaned = []
            for i, L in enumerate(pdb_lines):
                if L.startswith("TER") and i != last_ter:
                    continue
                cleaned.append(L)
        else:
            cleaned = pdb_lines
            
        with open(amber_pdb_name, "w") as fout:
            fout.writelines(cleaned)
            
        print("stripped internal TER lines, kept final TER")
        
        subprocess.run(f"""
        tleap -f tleap.in && \
        sbatch MD_submit.job
        """, shell=True, executable='/bin/bash')
        print("ran tleap and job submission")
        
        os.chdir(starting_dir)

print("All MD setup and submission complete.")
