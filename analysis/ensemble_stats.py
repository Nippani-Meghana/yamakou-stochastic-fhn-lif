import numpy as np
import simulation
from simulation.path_calling import path_calling_lif

class ensemble_stats:
    """
        A class to perform ensemble statistical analysis on the FitzHugh-Nagumo (FHN) model.
        
        This class automates multiple simulation trials to analyze the stochastic 
        behavior of neural firing, specifically calculating Inter-Spike Intervals (ISI) 
        and spike variability across independent runs.
    """
    def __init__(self):
        pass

    def trials_stats(self,ch, sigma):
        """
        Executes 100 simulation trials and calculates aggregate firing statistics.
        
        This method manages the ensemble execution loop and processes the resulting 
        spike data to compute the Inter-Spike Interval (ISI) distribution, 
        Coefficient of Variation (CV), and Fano Factor.

        Args:
            ch (int): The simulation type (1: Deterministic, 2: Additive, 3: Multiplicative).
        
        Returns:
            tuple: 
                - trial_spike_count_dict (dict): Spikes per trial ID.
                - trial_spike_timing_dict (dict): Timesteps of spikes per trial ID.
                - all_isi (list): Flattened list of all inter-spike intervals across all trials.
                - cv (float): Mean Coefficient of Variation (variability of timing).
                - fano_factor (float): Fano Factor (variability of spike counts).
        """

        trial_spike_timing_dict = {}
        trial_spike_count_dict = {}

        # 1. Ensemble Execution: Collect raw data over 100 independent trials
        for i in range(1,101):
            if i % 10 == 0:  # This will give an update every 10 trials
                print(f"Simulation in progress: {i}% complete...")
            trial_data = self.spikes(ch,sigma)
            trial_spike_timing_dict[i] = trial_data
            trial_spike_count_dict[i] = len(trial_data)

        # 2. Data Preparation for Statistical Analysis
        spike_trials = list(trial_spike_timing_dict.values())
        counts = np.array(list(trial_spike_count_dict.values()))

        all_isi = []  # Master list of all intervals across the ensemble
        cv_trial = []  # List of CV values calculated per individual trial

        # 3. ISI and CV Calculation
        # Iterate through trials to find the intervals between spikes
        for trial in spike_trials:
            if len(trial) > 1:
                isi_trial = np.diff(trial)
                cv_trial.append(np.std(isi_trial)/np.mean(isi_trial))
                all_isi.extend(isi_trial)

        if len(cv_trial) > 0:
            cv = np.mean(cv_trial)
        else:
            cv = None

        if np.mean(counts) > 0:
            fano_factor = np.var(counts) / np.mean(counts)
        else:
            fano_factor = None

        return trial_spike_count_dict, trial_spike_timing_dict, all_isi,cv,fano_factor

    def spikes(self,ch,sigma):
        """
        Runs a single FHN simulation and detects action potentials (spikes).
        
        Spike detection uses a fixed threshold to identify all-or-nothing 
        neural excursions while filtering out sub-threshold noise.
        
        Args:
            ch (int): The simulation type (1: Deterministic, 2: Additive, 3: Multiplicative).
            
        Returns:
            list: A list of indices (timesteps) where a spike was detected.
        """
        if(ch == 1):
            v,w,v_e,w_e,J_e = simulation.deterministic(-1.00125,-0.46)
        elif(ch == 2):
            v,w,v_e,w_e,J_e = simulation.additive_noise_fhn(-1.00125,-0.4, sigma)
        elif(ch == 3):
            v,w,v_e,w_e,J_e = simulation.multiplicative_noise(-1.00125,-0.4, sigma)
        elif(ch == 4):
            v = simulation.additive_noise_lif()
        else:
            print("Invalid Choice!")
        v_th = -0.55

        spike_times = []
        if ch in [1, 3]:
            for i in range(1, len(v)):
                if v[i-1] < v_th and v[i] >= v_th:
                    spike_times.append(i)

        #print("Number of spikes:", len(spike_times))
        #print("Spike Times: ",spike_times)

        if (ch == 4):
            v_peak = 20
            I_ext, R, V_r, sigma, tau = path_calling_lif()
            for i in range(1, len(v)):
                if v[i] >= v_th:
                    v[i-1] = v_peak         # Artificially draw the spike peak for your timeseries plot
                    v[i] = V_r              # Reset the voltage instantly back to resting potential
                    spike_times.append(i)

        return spike_times
    





