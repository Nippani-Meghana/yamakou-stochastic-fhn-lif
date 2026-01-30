from pathlib import Path
import json
from simulation.deterministic import deterministic
import numpy as np

def spikes_fhn():
    v,w,v_e,w_e,J_e = deterministic()
    v_th = -0.7
    spike_count = 0
    spikes_volts = []
    for i in v:
        if i>=v_th:
            spike_count += 1
            spikes_volts.append(v)


    print("Number of spikes are:",spike_count)
    print("Spike Voltages are :")
    for i in spikes_volts:
        print(i)


spikes_fhn()

    
    

    
