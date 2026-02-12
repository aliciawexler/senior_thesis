# senior_thesis
Modification of Boltz-1 software for the prediction of non-canonical amino acid-containing peptidomimetics
Boltz software source (official boltz github repository): jwohlwend/boltz
## Initial Requirements
 -You must have a conda environment that has boltz installed, and you must also have a cache directory that contains the boltz-1 ccd.pkl. Visit the boltz official directory for more information.
 
 -You must have access to at least one decent GPU for initial boltz structure predictions(TitanXP was used for this workflow) many (300+) CPU resources for MD simulations, and one excellent GPU for training(TitanXP may work with smaller datasets (<2000 samples = 48h/epoch), but for larger datasets, a better GPU is necessary (L40 was used for this workflow, ~8k samples = 13h/epoch))

 -You must have AmberTools downloaded, you can do so from here: https://ambermd.org/GetAmber.php#ambertools

 -Your custom residues must have a corresponding CCD component for initial Boltz-1 processing to work as it does in this tutorial. There may be auxillary methods of obtaining this processing, and those auxillary methods may work for steps 2 and onward.
 
 -For best results, read all .md files from all directories prior to beginning. This process is incredibly error-prone and expensive, and early mistakes can be costly. It is reccomended that users execute a test workflow with their desired residues and a limited number of sequences (~50) for debugging purposes prior to creation of the final model.
## Workflow steps: 
### 1. Sequence Preparation
Use the "sequence_prep" directory to prepare your dataset of sequences. Read the "sequence_prep.md" file for detailed instructions.
### 2. MD simulations
Use the "AMBER_MD" directory to run MD simulations on your prepared sequences. This process involves the creation of your unnatural residues, incoorporation of these residues into Boltz-1 software, and simulation walkthroughs. Read the "amber_md.md" file for detailed instructions. 
### 3. Simulation Processing

## Acknowledgement and Sources
@article{passaro2025boltz2,
  author = {Passaro, Saro and Corso, Gabriele and Wohlwend, Jeremy and Reveiz, Mateo and Thaler, Stephan and Somnath, Vignesh Ram and Getz, Noah and Portnoi, Tally and Roy, Julien and Stark, Hannes and Kwabi-Addo, David and Beaini, Dominique and Jaakkola, Tommi and Barzilay, Regina},
  title = {Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction},
  year = {2025},
  doi = {10.1101/2025.06.14.659707},
  journal = {bioRxiv}
}

@article{wohlwend2024boltz1,
  author = {Wohlwend, Jeremy and Corso, Gabriele and Passaro, Saro and Getz, Noah and Reveiz, Mateo and Leidal, Ken and Swiderski, Wojtek and Atkinson, Liam and Portnoi, Tally and Chinn, Itamar and Silterra, Jacob and Jaakkola, Tommi and Barzilay, Regina},
  title = {Boltz-1: Democratizing Biomolecular Interaction Modeling},
  year = {2024},
  doi = {10.1101/2024.11.19.624167},
  journal = {bioRxiv}
}
