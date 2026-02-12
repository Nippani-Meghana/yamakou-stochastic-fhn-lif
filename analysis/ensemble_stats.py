import numpy as np
import simulation

class ensemble_stats:
    """
    A class to perform ensemble statistical analysis on the FitzHugh-Nagumo (FHN) model.
    
    This class automates multiple simulation trials to analyze the stochastic 
    behavior of neural firing, specifically calculating Inter-Spike Intervals (ISI) 
    and spike variability across independent runs.
    """
    def __init__(self):
        pass

    def trials(self):
        """
        Executes a batch of 100 simulation trials based on user selection.
        
        This method manages the ensemble execution loop, collecting data from 
        either deterministic, additive stochastic, or multiplicative stochastic 
        simulations. 
        
        Returns:
            tuple: (trial_spike_count_dict, trial_spike_timing_dict)
                - trial_spike_count_dict: Mapping of trial IDs to total spikes detected.
                - trial_spike_timing_dict: Mapping of trial IDs to lists of spike indices.
        """
        print("====DASHBOARD====")
        print("1. Deterministic FHN")
        print("2. Stochastive Additive FHN")
        print("3. Stochastive Multiplicative FHN")
        ch = int(input('Please make your choice: '))

        trial_spike_timing_dict = {}
        trial_spike_count_dict = {}

        for i in range(1,101):
            if i % 10 == 0:  # This will give an update every 10 trials
                print(f"Simulation in progress: {i}% complete...")
            trial_data = self.spikes_fhn(ch)
            trial_spike_timing_dict[i] = trial_data
            trial_spike_count_dict[i] = len(trial_data)


        return trial_spike_count_dict, trial_spike_timing_dict

    def spikes_fhn(self,ch):
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
            v,w,v_e,w_e,J_e = simulation.additive_noise(-1.00125,-0.4)
        elif(ch == 3):
            v,w,v_e,w_e,J_e = simulation.multiplicative_noise(-1.00125,-0.4)
        else:
            print("Invalid Choice!")
        v_th = -0.55

        spike_times = []

        for i in range(1, len(v)):
            if v[i-1] < v_th and v[i] >= v_th:
                spike_times.append(i)

        #print("Number of spikes:", len(spike_times))
        #print("Spike Times: ",spike_times)

        return spike_times

