# Stochastic Neuron Models: Comparison with Biological Spike Trains

## Overview

This project implements and analyzes stochastic versions of the FitzHugh-Nagumo (FHN) neuron model in the excitable regime, alongside a Leaky Integrate-and-Fire (LIF) model, with a primary focus on comparing their spiking statistics to real biological neuron data. The FHN model is simulated under deterministic conditions and with additive or multiplicative noise, using numerical methods such as Euler and Heun schemes. The LIF model incorporates additive noise. Ensemble simulations are performed to compute inter-spike interval (ISI) distributions, coefficient of variation (CV), and Fano factor, enabling quantitative benchmarks against empirical data from mouse cortical neurons (sourced from the Allen Brain Observatory).

Originally inspired by Yamakou et al. (2019), the project has evolved beyond replication to emphasize biological fidelity. The radial Ornstein-Uhlenbeck reduction from the paper is omitted, as it prioritizes mathematical abstraction over physiological realism. Instead, emphasis is placed on ISI histogram comparisons and statistical tests (e.g., Kolmogorov-Smirnov distance) with biological ground truth.

Key findings from simulations:
- Biological CV: 0.64
- Stochastic Additive FHN CV: 0.28
- Stochastic Multiplicative FHN CV: 0.34
- LIF CV: 0.02

These results highlight that stochastic FHN models capture more irregularity than standard LIF, though neither fully matches biological variability. Future extensions may incorporate Generalized LIF (GLIF) models to improve CV alignment.

## Features

- Modular architecture separating models, simulations, visualizations, and analyses.
- Deterministic and stochastic (additive/multiplicative noise) simulations of FHN using Euler-Maruyama and Heun methods.
- Additive noise simulation of LIF with threshold/reset dynamics.
- Phase portraits for FHN to visualize nullclines, equilibria, and trajectories.
- Time series plots of membrane potential and recovery variables.
- Ensemble statistics: ISI histograms, CV, Fano factor over 100 trials.
- Direct comparison with biological ISI data via histograms, CV, and KS tests.
- Configurable parameters via JSON files for reproducibility.
- Interactive dashboard in `main.py` for selecting models and output perspectives.

## Requirements

- Python 3.8+
- Libraries: NumPy, SciPy, SymPy, Matplotlib

Install dependencies:
```
pip install numpy scipy sympy matplotlib
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd stochastic-neuron-models-comparison
   ```

2. Ensure biological data is available: Place `biological_isi.npy` (preprocessed ISI from Allen Brain Observatory) in the `allen_data/` directory. This file contains ISI values in milliseconds from mouse cortical neuron spike trains.

3. Run the main script:
   ```
   python main.py
   ```

## Usage

The project is controlled via `main.py`, which provides an interactive menu:

1. **Model Selection**:
   - 1: Deterministic FHN
   - 2: Stochastic Additive FHN (prompt for sigma)
   - 3: Stochastic Multiplicative FHN (prompt for sigma)
   - 4: LIF (prompt for sigma)
   - 5: Exit

2. **Output Perspective**:
   - 1: Phase Portrait (FHN only; visualizes trajectories and nullclines)
   - 2: Ensemble Stats (spike counts, timings, CV, Fano factor over 100 trials)
   - 3: Time Series (plots v(t) and w(t) for FHN; v(t) for LIF)
   - 4: ISI Histogram (probability density of ISIs)
   - 5: Comparison with Biological Ground Truth (overlaid ISI histograms, CVs, KS distances)

Example workflow:
- Select model 2 (Additive FHN), enter sigma=0.05.
- Select output 5: Generates comparative plot and stats against biological data.

Parameters are loaded from `config/fhn_params.json` and `config/lif_params.json`. Modify these for custom experiments (e.g., adjust I_ext, tau).

## Directory Structure

```
stochastic-neuron-models-comparison
├── Models
│   ├── __init__.py
│   ├── FHN.py          # FHN model class with equilibrium and Jacobian
│   └── LIF.py          # LIF model class
├── simulation
│   ├── __init__.py
│   ├── deterministic.py    # Deterministic FHN solver
│   ├── additive_noise.py   # Additive noise for FHN and LIF (Euler-Maruyama)
│   ├── multiplicative_noise.py  # Multiplicative noise for FHN (Heun method)
│   └── path_calling.py     # Parameter loading from JSON
├── visualization
│   ├── phase_portrait.py   # Phase plane plots with nullclines
│   ├── timeseries.py       # Time series plots
│   └── isi_histogram.py    # ISI distribution histograms
├── analysis
│   ├── __init__.py
│   └── ensemble_stats.py   # Ensemble trials, spike detection, stats (CV, Fano)
├── config
│   ├── fhn_params.json     # FHN parameters (I_ext, a, b, tau)
│   └── lif_params.json     # LIF parameters (I_ext, R, V_r, sigma, tau)
├── allen_data
│   └── biological_isi.npy  # Preprocessed biological ISI data
└── main.py                 # Interactive dashboard
```

## Models

- **FitzHugh-Nagumo (FHN)**: A 2D reduced model of neuron excitability. Equations:
  - dv/dt = v - v³/3 - w + I_ext
  - dw/dt = (1/τ)(v + a - b w)
  Simulated deterministically (Euler) or stochastically (additive: dw += σ dW; multiplicative: dw += σ w dW using Heun).

- **Leaky Integrate-and-Fire (LIF)**: A 1D engineering model. Equation:
  - dv/dt = (1/τ)(- (v - V_r) + R I_ext) + σ dW
  With threshold/reset: If v >= V_th, spike and reset to V_r.

Spike detection uses fixed thresholds (FHN: v_th = -0.55; LIF: v_th = -55.0).

## Biological Data Comparison

Biological ISI data is loaded from `allen_data/biological_isi.npy` (filtered to <200 ms for active firing). Models are benchmarked via:
- CV: std(ISI)/mean(ISI) – Measures irregularity.
- KS Statistic: Distributional distance (lower = better fit).
- Overlaid histograms for visual inspection.

Current limitations: LIF exhibits low CV (regular firing), suggesting a need for GLIF variants (e.g., with adaptive thresholds or refractory periods) to better capture biological irregularity (CV ~0.64).

## Results and Discussion

Simulations reveal that multiplicative noise in FHN introduces more variability (CV=0.34) than additive (CV=0.28), closer to biology but still underestimating. LIF's low CV (0.02) indicates overly regular dynamics, unsuitable without extensions. These discrepancies underscore the value of noise type and model dimensionality in replicating empirical spike trains.

## Future Work

- Implement Generalized LIF (GLIF) to address low CV in LIF.
- Parameter optimization (e.g., via SciPy minimize) to minimize KS distance to biology.
- Expand biological datasets (e.g., from CRCNS or EBRAINS).

## References

- Yamakou, M. E., Tran, T. D., Duc, L. H., & Jost, J. (2019). The stochastic FitzHugh-Nagumo neuron model in the excitable regime embeds a leaky integrate-and-fire model. *Journal of Mathematical Biology*, 79(2), 509–532. https://doi.org/10.1007/s00285-019-01366-z
- Allen Brain Observatory: Electrophysiology data for mouse cortical neurons.

## License

This project is licensed under the MIT License.