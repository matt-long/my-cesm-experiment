#!/bin/bash

set -e

remote_mach=thorodin.cgd.ucar.edu
remote_dir=/web/web-data/staff/mclong/my-cesm-experiment

source activate cesm-exp

conda info --envs

jupyter-book clean _computed-notebooks
jupyter-book build _computed-notebooks --all

scp -r _computed-notebooks/_build/html/* ${remote_mach}:${remote_dir}