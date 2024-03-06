#!/bin/bash

echo "=============================="

source /etc/profile 

module load py-mpi4py/3.1.4/gcc-12.3.0-openmpi intel-oneapi-compilers/2023.1.0/gcc-11.4.0

python3 /usr/users/st76i/st76i_14/Python-Launcher-Examples/launcher_sub_wolf.py 4096 --strategy core
