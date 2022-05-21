# My CESM Experiment

Objective: demonstrate minimum working example for compiling analysis and diagnostics associated with a CESM case.

## Invoking the calculation

To reproduce the calculation:

1. Build conda environment for computations:

```bash
conda env create -f environment.yml
```

1. Run all the notebooks in [\_toc.yml](notebooks/_toc.yml).

## Building the book

The JupyterBook rendition can be built with the following steps.

1. Clone this repository
1. Build environment as described in 1. above
1. (Optional) Edit the books source files located in the `notebooks` directory
1. Activate the conda environment (i.e., run: `conda activate metabolic`)
1. Run `jupyter-book clean notebooks/` to remove any existing builds
1. Run `jupyter-book build notebooks/`

A fully-rendered HTML version of the book will be built in `notebooks/_build/html/`.

## Credits

This project is created using the excellent open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).
