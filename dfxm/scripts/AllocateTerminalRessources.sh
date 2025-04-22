#!/bin/bash
echo Remember to run the following commands after the ressources are allocated
echo module load darfix/2.4
echo darfix
salloc --x11 --ntasks=1 --mem=400G --time=12:00:00 --cpus-per-task=20  srun --pty bash