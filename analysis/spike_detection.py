import simulation
import numpy as np

def spikes_fhn():
    print("====DASHBOARD====")
    print("1. Deterministic FHN")
    print("2. Stochastive Additive FHN")
    print("3. Stochastive Multiplicative FHN")
    ch = int(input('Please make your choice: '))
    if(ch == 1):
        v,w,v_e,w_e,J_e = simulation.deterministic(-1.00125,-0.46)
    elif(ch == 2):
        v,w,v_e,w_e,J_e = simulation.additive_noise(-1.00125,-0.4)
    elif(ch == 3):
        v,w,v_e,w_e,J_e = simulation.multiplicative_noise(-1.00125,-0.4)
    else:
        print("Invalid Choice!")
    v_th = -0.7

    spike_times = []

    for i in range(1, len(v)):
        if v[i-1] < v_th and v[i] >= v_th:
            spike_times.append(i)

    print("Total voltages recorded:", len(v))
    print("Number of spikes:", len(spike_times))
  
spikes_fhn()

    
    

    
