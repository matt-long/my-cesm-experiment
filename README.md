# My CESM Experiment

Objective: demonstrate minimum working example for compiling analysis and diagnostics associated with a CESM case.

## Run the package

1. Build conda environment for computations:

```bash
conda env create -f environment.yml
```
or

```bash
mamba env create -f environment.yml
```

1. Specify the case information in [\_config-calc.yml](notebooks/_config-calc.yml).
1. Open and run the [\_run.ipynb](notebooks/_run.ipynb) notebook.
1. Edit and run the [build-and-publish.sh](./build-and-publish.sh) script.

## To extend the package

1. Add your notebook to the list in [\_config-calc.yml](notebooks/_config-calc.yml).
1. Add your notebook to [\_toc.yml](notebooks/_toc.yml).


## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
