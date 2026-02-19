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

from analysis.ensemble_stats import ensemble_stats
import simulation
from visualization.timeseries import timeseries as plot_timeseries
import Models
import analysis
import sys
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Initialize the statistical analysis engine.
stats = analysis.ensemble_stats()

while(True):
    print("\n====DASHBOARD====")
    print("1. Deterministic FHN")
    print("2. Stochastive Additive FHN")
    print("3. Stochastive Multiplicative FHN")
    print("4. LIF")
    print("5. Exit")

    # Capture primary model choice. 
    try:
        ch = int(input('Please make your choice: '))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        continue

    # FIX 1: Exit logic updated to option 5
    if(ch == 5):
        print("Program Terminated!")
        sys.exit()
        
    if ch not in [1, 2, 3, 4]:
        print("Invalid input. Please enter a number between 1 and 5.")
        continue

    # REGIME PARAMETERS: 
    s = 0.0
    if ch in [2, 3, 4]:
        s = float(input("Please enter sigma value: "))

    print('\n===DATA OUTPUT PERSPECTIVE===')
    print("1. Phase Portrait (Not available for LIF)")
    print("2. Ensemble Stats")
    print("3. Timeseries")
    print("4. ISI Histogram")
    print("5. Comparison with Biological Ground Truth")   

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
        if(ch == 1):
            from visualization.phase_portrait import det_phase_portrait
            det_phase_portrait()
        elif(ch == 2):
            from visualization.phase_portrait import add_noise_phase_portrait
            add_noise_phase_portrait(s)
        elif(ch == 3):
            from visualization.phase_portrait import mult_noise_phase_portrait
            mult_noise_phase_portrait(s)
        elif(ch == 4):
            print("Phase Portrait is not available for 1D LIF Model.")

    elif (ch_data == 2):
        """
        ENSEMBLE STATS PERSPECTIVE
        Executes a batch of trials to analyze long-term behavior.
        """
        print('Printing Ensemble Stats...')
        count, timing, isi, cv, fano_factor = stats.trials_stats(ch, s)
        print("Trials and Spike Count: ", count)
        print("CV:", cv)
        print("Fano Factor: ", fano_factor)

    elif(ch_data == 3):
        """
        TIMESERIES PERSPECTIVE
        Standard temporal trace of membrane potential. 
        """
        plot_timeseries(ch, s)

    elif(ch_data == 4):
        """
        ISI HISTOGRAM PERSPECTIVE
        Visualizes the distribution of inter-spike intervals across trials.
        """
        from visualization.isi_histogram import plot_isi_histogram
        print("Generating ISI Histogram...")
        _, _, all_isi, _, _ = stats.trials_stats(ch, s)
        plot_isi_histogram(all_isi, ch, s)

    elif (ch_data == 5):
        import scipy.stats as sc_stats  

        print("Loading biological ground truth...")
        try:
            bio_isi_ms = np.load('allen_data/biological_isi.npy')
            # Filter out sleep/pause outliers so we measure the active firing regime
            bio_isi_ms = bio_isi_ms[bio_isi_ms < 200] 
        except FileNotFoundError:
            print("Error: Could not find 'allen_data/biological_isi.npy'.")
            continue

        # Safeguard 's' so FHN doesn't crash on 0 spikes
        fhn_sigma = 0.05 if s == 0.0 else s
        
        # --- THE FIX: Dynamically select Additive vs Multiplicative FHN ---
        # If the user chose 3, run Multiplicative. Otherwise, default to 2 (Additive).
        fhn_ch = ch if ch in [2, 3] else 2  
        fhn_label = "Multiplicative FHN" if fhn_ch == 3 else "Additive FHN"

        print(f"Simulating {fhn_label} Model (100 trials, sigma={fhn_sigma})...")
        _, _, fhn_isi_timesteps, fhn_cv, _ = stats.trials_stats(fhn_ch, fhn_sigma)

        print("Simulating LIF Model (100 trials)...")
        _, _, lif_isi_timesteps, lif_cv, _ = stats.trials_stats(4, fhn_sigma)
        # SAFEGUARD: Replace 'None' CVs with 0.0 so formatting doesn't crash
        fhn_cv_display = fhn_cv if fhn_cv is not None else 0.0
        lif_cv_display = lif_cv if lif_cv is not None else 0.0

        # Convert to ms
        dt = 0.01
        fhn_ms = np.array(fhn_isi_timesteps) * dt if fhn_isi_timesteps else np.array([])
        lif_ms = np.array(lif_isi_timesteps) * dt if lif_isi_timesteps else np.array([])

        print("\n" + "="*40)
        print("FINAL STATISTICAL BENCHMARKS")
        print("="*40)

        # --- 1. Calculate and Compare CV ---
        bio_cv = np.std(bio_isi_ms) / np.mean(bio_isi_ms)
        print(f"Biological Mouse CV : {bio_cv:.3f}")
        print(f"Math Model ({fhn_label}) CV : {fhn_cv_display:.3f}")
        print(f"Engineering (LIF) CV: {lif_cv_display:.3f}\n")

        # --- 2. Calculate KS Test ---
        if len(fhn_ms) > 0 and len(lif_ms) > 0:
            ks_fhn_stat, _ = sc_stats.ks_2samp(fhn_ms, bio_isi_ms)
            ks_lif_stat, _ = sc_stats.ks_2samp(lif_ms, bio_isi_ms)

            print("Kolmogorov-Smirnov Distance (Lower is closer to Biology):")
            print(f"{fhn_label} vs Biology KS Statistic: {ks_fhn_stat:.3f}")
            print(f"LIF vs Biology KS Statistic: {ks_lif_stat:.3f}")
        else:
            print("Not enough spikes generated to calculate KS Statistic.")
            
        print("="*40 + "\n")

        print("Generating the plot...")

        # --- PLOTTING ---
        fig, ax = plt.subplots(figsize=(10, 6))

        my_bins = np.arange(0, 160, 4)

        ax.hist(bio_isi_ms, bins=my_bins, density=True, alpha=0.5, color='#2ca02c', label=f'Biological (CV: {bio_cv:.2f})', edgecolor='black')
        ax.hist(fhn_ms, bins=my_bins, density=True, alpha=0.5, color='#9467bd', label=f'{fhn_label} (CV: {fhn_cv_display:.2f})', edgecolor='black')
        ax.hist(lif_ms, bins=my_bins, density=True, alpha=0.5, color='#ff7f0e', label=f'LIF (CV: {lif_cv_display:.2f})', edgecolor='black')

        ax.set_title(f'Inter-Spike Interval Distribution: Models vs. Reality', fontsize=14, fontweight='bold')
        ax.set_xlabel('Inter-Spike Interval (ms)', fontsize=12)
        ax.set_ylabel('Probability Density', fontsize=12)

        ax.set_xlim(0, 160)

        ax.legend(fontsize=11, loc='upper right')
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        plt.tight_layout()
        plt.show()