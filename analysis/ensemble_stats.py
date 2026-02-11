import numpy as np
import simulation

class ensemble_stats:
    def __init__(self):
        pass

    def trials(self):
        print("====DASHBOARD====")
        print("1. Deterministic FHN")
        print("2. Stochastive Additive FHN")
        print("3. Stochastive Multiplicative FHN")
        ch = int(input('Please make your choice: '))

        trial_spike_timing_dict = {}
        trial_spike_count_dict = {}

        for i in range(1,101):
            trial_data = self.spikes_fhn(ch)
            trial_spike_timing_dict[i] = trial_data
            trial_spike_count_dict[i] = len(trial_data)

        print("Trials and Spike Count: ",trial_spike_count_dict)
        print("Trials and Spike Timings: ",trial_spike_timing_dict)

    def spikes_fhn(ch):
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

