# Notes for the `kcorrect` package

## `kcorrect` installation


```bash
conda create -n kcorrect python=3.9 numpy=1.23
pip install kcorrect
```

## Cautions
- `kcorrect 5.1.8` may exhibit memory leaks when processing large numbers (~100) of galaxies in a single script (e.g., within a loop). Then the program may be killed without error. Need a script (e.g. `fit_one_galaxy.py`) for fitting one galaxy and a main script to run these subprocesses in loops.
- `kcorrect 5.1.8` may not work with `numpy` version after 1.23
- The default unit of flux is maggies. In real observations, the inverse variance numbers are often too large for matrix calculations. Recommend to normalize the flux and ivar before fitting.
- When preprocessing the templates, the minimum redshift should below 0, for deriving the fitted physical parameters later.

## AGN templates
The templates from [Pai et al. 2024](https://ui.adsabs.harvard.edu/abs/2024ApJ...977..102P/abstract), 
see https://kcorrect.readthedocs.io/en/stable/templates.html


## Basic usages
Documentation: https://kcorrect.readthedocs.io/en/stable/

See tutorial.ipynb for some tricks.




