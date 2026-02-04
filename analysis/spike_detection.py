from pathlib import Path
import json
from simulation.deterministic import deterministic
import numpy as np

def spikes_fhn():
    v, w, v_e, w_e, J_e = deterministic()
    v_th = -0.7

    spike_times = []

    for i in range(1, len(v)):
        if v[i-1] < v_th and v[i] >= v_th:
            spike_times.append(i)

    print("Total voltages recorded:", len(v))
    print("Number of spikes:", len(spike_times))
  

spikes_fhn()

    
    

    
