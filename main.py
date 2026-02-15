"""
Main Execution Hub: Neural Dynamics Simulation Dashboard
-------------------------------------------------------
This script serves as the primary controller for the simulation framework. 
It implements a decoupled architecture where the mathematical model selection 
is independent of the visualization and analysis methods.

Author: NM
Date: February 2026
Project: Stochastic Dynamics in FitzHugh-Nagumo and LIF Models
"""

import simulation
from visualization.timeseries import timeseries as plot_timeseries
import Models
import analysis
import sys

# Initialize the statistical analysis engine.
# This object handles multi-trial simulations to calculate metrics like 
# Coefficient of Variation (CV) and Fano Factor.
stats = analysis.ensemble_stats()

while(True):
    print("====DASHBOARD====")
    print("1. Deterministic FHN")
    print("2. Stochastive Additive FHN")
    print("3. Stochastive Multiplicative FHN")
    print("4. LIF")
    print("5. Radical OU")
    print("6. Exit")

    # Capture primary model choice. 
    # int() cast is necessary for numerical comparison in logic blocks.
    try:
        ch = int(input('Please make your choice: '))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 6.")
        continue

    # REGIME PARAMETERS: 
    # Stochastic models (2 and 3) require a noise intensity parameter (sigma).
    # Defaulting to 0.0 for deterministic models prevents NameErrors later.
    s = 0.0
    if ch in [2, 3]:
        s = float(input("Please enter sigma value: "))

    if(ch == 6):
        print("Program Terminated!")
        sys.exit()

    print('===DATA OUTPUT PERSPECTIVE===')
    print("1. Phase Portrait")
    print("2. Ensemble Stats")
    print("3. Timeseries")

    try:
        ch_data = int(input('Please make your choice: '))
    except ValueError:
        print("Invalid input. Returning to main menu.")
        continue

    if(ch_data == 1):
            """
        PHASE PORTRAIT PERSPECTIVE
        Visualizes the system's trajectory relative to its nullclines. 
        Crucial for identifying the 'separatrix' or threshold boundary.
        """
            print("Generating Phase Portrait...")
            # Local imports prevent unnecessary memory usage and circular dependencies
            if(ch == 1):
                from visualization.phase_portrait import det_phase_portrait
                det_phase_portrait()
            elif(ch == 2):
                from visualization.phase_portrait import add_noise_phase_portrait
                add_noise_phase_portrait(s)
            elif(ch == 3):
                from visualization.phase_portrait import mult_noise_phase_portrait
                mult_noise_phase_portrait(s)

    elif (ch_data == 2):
            """
        ENSEMBLE STATS PERSPECTIVE
        Executes a batch of trials to analyze long-term behavior.
        Calculates:
          - Inter-Spike Interval (ISI): Time between consecutive spikes.
          - CV: Measure of firing regularity (CV ~ 1 is Poisson-like).
          - Fano Factor: Measure of spike count variability.
        """
            print('Printing Ensemble Stats...')
            count, timing,isi,cv,fano_factor = stats.trials_stats(ch, s)
            print("Trials and Spike Count: ",count)
            print("ISI: ",isi)
            print("CV:",cv)
            print("Fano Factor: ",fano_factor)

    elif(ch_data == 3):
        """
        TIMESERIES PERSPECTIVE
        Standard temporal trace of membrane potential. 
        Used to visualize the waveforms of action potentials.
        """
        plot_timeseries(ch,s)

