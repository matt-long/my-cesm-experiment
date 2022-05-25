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

1. **Edit the configuration file**: Specify the case information in [\_config-calc.yml](notebooks/_config-calc.yml).
1. **Run the notebooks**: Open and run the [\_run.ipynb](notebooks/_run.ipynb) notebook. The notebooks will be run and the computed notebooks save in the `output_dir`, which is specified in [\_config-calc.yml](notebooks/_config-calc.yml). This is the directory from which the Jupyter Book is built.
1. **Build the book**: Edit and run the [build-and-publish.sh](notebooks/build-and-publish.sh) script.

## To extend the package

1. Add your notebook to the `compute_notebooks` and `book_toc` lists in [\_config-calc.yml](notebooks/_config-calc.yml). Markdown and ipynb files that are in the `book_toc`, but not the `compute_notebooks` list are automatically copied into the `output_dir`.


## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
