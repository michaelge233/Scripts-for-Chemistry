# Scripts for Chemistry
A set of data processing and visualization scripts in chemistry.  Following requirements are needed to run them:
* Python3 along with Jupyter
* numpy
* pandas
* matplotlib
* scipy
* pymatgen
* ase

The scripts are divided into following categories.
## Course Assignments
Scripts relating to my course assigments.
## Molecular Modeling Examples
Examples of Molecular Modeling for computational chemistry in Python Jupyter Notebook (.ipynb) format. The main goal of these scripts is to generate the initial input structure files like the POSCAR in VASP for computation. <br>
**Interlayer_binding_energy.ipynb :** A modeling example to calculate the interlayer binding energy of a two-dimensional perovskite.
**Perovskite_ion_migration.ipynb :** A modeling example to calculate the ion migration activation energy of halogen vacancy in two-dimensional perovskite.
**Useful_functions.py :** A collection of useful functions written by myself in modeling. You can copy them into Jupyter notebook and follow the annotation to use them while modeling.
## VASP Input
Scripts for generating input files for VASP. These scprits can be directly executed via `Python3 <scriptname>.py` <br>
**Generate_KPOINTS_hybride.py :** This script offers an easy way to generate the KPOINTS file for electronic band structure calculation using hybrid functions (such as B3LYP, HSE and PBE0). The convenient line mode KPOINTS file only works for LDA or GGA, but not for hybrid functionals. To generate KPOINTS file for hybrid functions, you need to put the line mode KPOINTS file (rename as bands_KPOINTS), the IBZKPT in scf (rename as scf_IBZKPT) and this script in a same dir, and run this script. The generated KPOINTS can be used for hybrid functionals directly. <br>
**Generate_POTCAR.py :** This script is a tool to generate the POTCAR. Firstly, you should edit this script to replace the value of POTPATH with the path you store your pseudopotentials. Then, put this script and the POSCAR file in the same path and run this script. <br>
**See_force.py :** This script is to show the residual forces during the geometry optimization. The residual forces are often treated as convergence criteria, but neither stdout nor OSZICAR containing them.
This script extracts the residual forces from OUTCAR and outputs to stdout. It was designed to monitor the geometry optimization and can be directly executed on Linux. Just copy the script to the path that VASP are running, and run this script.
## VASP Post Processing
Examples of post processing of VASP output in Python Jupyter Notebook (.ipynb) format. The main goal of these scripts is to convert the raw output data to figures to be published. <br>
**Band_PDOS.ipynb :** An example to plot band structure and PDOS of a 2D perovskite from raw output.
## High-throughput calculation
Coming.
