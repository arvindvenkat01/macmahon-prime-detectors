# Explicit MacMahonesque Prime Detectors
This repository contains Python implementations and verification scripts for two novel explicit prime-detecting formulas based on MacMahonesque partition statistics $M_k(n)$.

**Author**: Arvind N. Venkat

This work has been archived and assigned a permanent identifier on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXX.svg)](https://doi.org/10.5281/zenodo.XXXX)


- DOI: `10.5281/zenodo.XXXX`
- URL: `[https://zenodo.org/records/XXXX](https://zenodo.org/records/XXXX)`

## Abstract

These results extend the theoretical framework established by **Craig, van Ittersum, and Ono (2024)** by providing computationally optimized formulas at depth 4 and in the binomial basis.


## Repository Contents

`verify_quartic_detector.py` - [Cubic-Degree Quartic Detector (Depth 4)] : A prime detector involving partitions with exactly 4 distinct sizes ($M_4$), featuring polynomial coefficients of degree 3 (cubic) in $n$. This represents a degree reduction compared to the quartic-degree examples in the literature.

`verify_binomial_detector.py` - [Binomial-Basis Cubic Detector] : A compact reformulation of the cubic detector using binomial coefficients, revealing a structural symmetry where $M_1$ and $M_2$ are weighted identically.


## 🚀 Usage

Both scripts use an optimized dynamic programming approach with memoization (`functools.lru_cache`) to compute partition statistics efficiently.
All the scripts were run in Google Colaboratory. The code can be copy-pasted into a cell and executed to produce the mentioned output.



## Prerequisites

* Python 3.8+
* `sympy`


## Citation

If you use this work, please cite the paper using the Zenodo archive.

@misc{naladiga_venkat_2025_17066282,
  author       = {Naladiga Venkat, Arvind},
  title        = {To be uploaded
                  },
  month        = sep,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v2},
  doi          = {10.5281/zenodo.XXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXX},
}


## 🙏 Acknowledgments
Based on the foundational work of Craig, van Ittersum, and Ono: *"Integer partitions detect the primes"* (PNAS, 2024).


## License

The content of this repository is dual-licensed:

- **MIT License** for `prime-cube-taxicab-verifier.py`  
- **CC BY 4.0** (Creative Commons Attribution 4.0 International) for all other content (paper, results, README, etc.)
