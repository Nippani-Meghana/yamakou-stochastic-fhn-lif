# FHN_LIF: Stochastic FitzHugh-Nagumo Model and Embedded LIF Analysis

A Python implementation replicating the computational work from Yamakou et al. (2019), "The stochastic FitzHugh-Nagumo neuron model in the excitable regime embeds a leaky integrate-and-fire model."

## Overview

This project explores how stochastic noise influences neural firing in the excitable regime of the FitzHugh-Nagumo (FHN) model and demonstrates how this complex biophysical model can be reduced to a simpler Leaky Integrate-and-Fire (LIF) model while preserving key statistical properties of spike timing.

### Key Concepts

**Excitable Regime**: The FHN model is parameterized such that it rests at a stable fixed point unless perturbed. In this regime, the neuron does not fire spontaneously but can be driven to spike by noise or external input.

**Stochastic Resonance**: Background noise, rather than disrupting neural function, can actually induce regular firing patterns through a phenomenon known as coherence resonance.

**Model Embedding**: The paper demonstrates that a properly parameterized LIF model can reproduce the inter-spike interval (ISI) statistics of the stochastic FHN model, providing a computationally cheaper alternative.

## Project Structure

```
FHN_LIF/
├── Models/
│   ├── __init__.py
│   └── FHN.py                  # Core FitzHugh-Nagumo dynamics
├── simulation/
│   ├── __init__.py
│   ├── deterministic.py        # Euler method integration
│   ├── additive_noise.py       # Euler-Maruyama method
│   ├── multiplicative_noise.py # Stochastic Runge-Kutta (Heun)
│   └── path_calling.py         # Configuration loader
├── visualization/
│   ├── phase_portrait.py       # Phase plane analysis
│   └── timeseries.py           # Temporal dynamics
├── analysis/
│   ├── __init__.py
│   └── ensemble_stats.py       # ISI, CV, Fano factor computation
├── config/
│   └── fhn_params.json         # Model parameters
└── main.py                      # Interactive dashboard
```

## Mathematical Background

### FitzHugh-Nagumo Equations

The deterministic FHN model consists of two coupled ordinary differential equations:

```
dv/dt = v - (v³/3) - w + I_ext
dw/dt = (1/τ)(v + a - bw)
```

Where:
- `v`: Fast variable (membrane potential)
- `w`: Slow variable (recovery/adaptation)
- `τ`: Time scale separation parameter
- `I_ext`: External current
- `a, b`: Shape parameters

### Stochastic Extensions

**Additive Noise** (constant background fluctuations):
```
dw = (1/τ)(v + a - bw)dt + σ dW
```

**Multiplicative Noise** (state-dependent fluctuations):
```
dw = (1/τ)(v + a - bw)dt + σw dW
```

Where `dW` represents a Wiener process (Brownian motion).

## Implementation Details

### Numerical Methods

**Deterministic Integration**: Standard Euler method with timestep `dt = 0.01`

**Additive Noise**: Euler-Maruyama method
- Noise term: `σ * N(0,1) * √dt`
- The `√dt` scaling ensures proper Brownian motion variance

**Multiplicative Noise**: Second-order Stochastic Runge-Kutta (Heun's method)
- Uses predictor-corrector approach
- Necessary for numerical stability when noise scales with state variable
- More accurate than Euler-Maruyama for state-dependent noise

### Spike Detection

Spikes are detected using an upward threshold crossing at `v_th = -0.55`. When the membrane potential crosses this threshold from below, a spike is registered.

### Statistical Analysis

**Inter-Spike Interval (ISI)**: Time between consecutive spikes
- Computed from spike timing arrays
- Distribution characterizes firing regularity

**Coefficient of Variation (CV)**: `σ_ISI / μ_ISI`
- CV ≈ 0: Regular firing (clock-like)
- CV ≈ 1: Poisson-like (random)
- CV > 1: Bursty or irregular

**Fano Factor**: `Var(spike_count) / Mean(spike_count)`
- Measures trial-to-trial variability
- FF = 1 for Poisson process
- FF > 1 indicates overdispersion

## Current Implementation Status

### Completed
- Core FHN model with equilibrium and stability analysis
- Deterministic simulation (Euler method)
- Stochastic simulations (Euler-Maruyama and SRK methods)
- Phase plane visualization with nullclines
- Time series plotting
- Ensemble statistics framework (100 trials)
- ISI, CV, and Fano factor computation
- Interactive command-line dashboard

### In Progress
1. ISI distribution histograms
2. Embedded LIF model implementation
3. Quantitative comparison (FHN vs LIF)
4. Power spectral density analysis
5. Firing probability vs. noise intensity curves

## Installation

### Prerequisites
```bash
Python 3.8+
numpy
scipy
matplotlib
sympy
```

### Setup
```bash
git clone 
cd FHN_LIF
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the main dashboard:
```bash
python main.py
```

You will be presented with options to:
1. Choose simulation type (deterministic, additive noise, multiplicative noise)
2. Set noise intensity (sigma) for stochastic models
3. Select visualization (phase portrait, ensemble stats, time series)

### Example: Running Ensemble Analysis

```python
from analysis.ensemble_stats import ensemble_stats

stats = ensemble_stats()

# Choice 2 = additive noise simulation
count, timing, isi, cv, fano = stats.trials_stats(ch=2)

print(f"Mean CV: {cv}")
print(f"Fano Factor: {fano}")
```

### Configuration

Model parameters are stored in `config/fhn_params.json`:
```json
{
  "fhn_parameters": {
    "I_ext": 0.265,
    "a": 0.7,
    "b": 0.75,
    "tau": 12.5
  }
}
```

These values place the system in the excitable regime as specified in Yamakou et al.

## Key Results to Replicate

From the original paper, the project aims to reproduce:

1. **Phase portraits showing excitability**: Small perturbations return to equilibrium; larger ones trigger full action potentials

2. **Noise-induced firing**: Stochastic fluctuations can drive regular spiking even when the deterministic system is stable

3. **ISI statistics**: Both FHN and embedded LIF should produce similar ISI distributions

4. **Coherence resonance**: Optimal noise level where firing becomes most regular (minimum CV)

## Scientific Context

The FHN model is a simplified version of the Hodgkin-Huxley equations, retaining essential excitable dynamics while being analytically tractable. Understanding how stochastic FHN maps to LIF is important because:

- **Computational efficiency**: LIF is much faster to simulate in large networks
- **Theoretical insight**: Shows which features of complex models are essential for spike statistics
- **Biological relevance**: Real neurons operate in noisy environments

## References

**Primary Source**:
Yamakou, M.E., Tran, T.D., Duc, L.H., Jost, J. (2019). The stochastic Fitzhugh–Nagumo neuron model in the excitable regime embeds a leaky integrate-and-fire model. *Journal of Mathematical Biology*, 79, 509–532. [https://doi.org/10.1007/s00285-019-01366-z](https://doi.org/10.1007/s00285-019-01366-z)

**Additional Reading**:
- FitzHugh, R. (1961). Impulses and Physiological States in Theoretical Models of Nerve Membrane. *Biophysical Journal*, 1(6), 445–466.
- Nagumo, J., Arimoto, S., Yoshizawa, S. (1962). An Active Pulse Transmission Line Simulating Nerve Axon. *Proceedings of the IRE*, 50(10), 2061–2070.

## Learning Resources

For those new to computational neuroscience:

**Stochastic Differential Equations**:
- Understanding the difference between Itô and Stratonovich interpretation
- Why `√dt` scaling is necessary for Brownian motion
- When to use Euler-Maruyama vs. higher-order methods

**Phase Plane Analysis**:
- Nullclines represent curves where dv/dt = 0 or dw/dt = 0
- Fixed points occur at nullcline intersections
- Stability determined by Jacobian eigenvalues at fixed points

**Excitability**:
- Threshold behavior: small perturbations decay, large ones trigger spikes
- All-or-nothing response characteristic of neurons
- Refractory period: temporary inability to spike again

## Project Status

This is an active learning project documenting the implementation process. The code is functional but under development. Feedback and contributions are welcome.

## Author

Second-year undergraduate student in Computer Science and Engineering (IoT), self-teaching computational neuroscience.

## License

This project is for educational purposes. The original research is credited to Yamakou et al. (2019).

## Acknowledgments

This implementation was developed as part of independent study in computational neuroscience, following the methodology described in the original paper. Special thanks to the authors for providing clear mathematical formulations that enable reproducibility.