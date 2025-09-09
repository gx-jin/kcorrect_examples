# Notes for the `kcorrect` package

## `kcorrect` installation


```bash
conda create -n kcorrect python=3.9 numpy=1.23
pip install kcorrect
```

## `kcorrect` warnings
- `kcorrect 5.1.8` may exhibit memory leaks when processing large numbers (~100) of galaxies in a single script (e.g., within a loop). Then the program may be killed without error. Need a script for fitting one galaxy and a main script to run these subprocesses in loops.

## AGN templates
The templates from [Pai et al. 2024](https://ui.adsabs.harvard.edu/abs/2024ApJ...977..102P/abstract), 
see https://kcorrect.readthedocs.io/en/stable/templates.html


## Code usages
### Check filter names
```python
import kcorrect
import os

kcorrect_path = os.path.dirname(kcorrect.__file__)
data_path = os.path.join(kcorrect_path, 'data')
responses_path = os.path.join(data_path, 'responses')

# Check files in the responses directory
if os.path.exists(responses_path):
    response_files = os.listdir(responses_path)
    print(f"Number of files in responses directory: {len(response_files)}")
    print("\nAll filter response files:")
    
    # Sort alphabetically and display
    for i, f in enumerate(sorted(response_files), 1):
        # Remove file extension to get filter name
        filter_name = os.path.splitext(f)[0]
        print(f"{i:3d}. {filter_name}")
    
    print(f"\nTotal filters found: {len(response_files)}")
else:
    print(f"Responses directory does not exist: {responses_path}")
```
