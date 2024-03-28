#!/bin/bash

echo "==============Load Modules==============="

source /etc/profile 

module load py-mpi4py/3.1.4/gcc-12.3.0-openmpi 
echo "\t- mpi module loaded"
module load intel-oneapi-compilers/2023.1.0/gcc-11.4.0 
echo "\t- intel module loaded"
module load valgrind/3.20.0/gcc-12.3.0-openmpi
echo "\t- valgrind module loaded"

echo "========================================="

