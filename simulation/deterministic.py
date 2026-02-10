import numpy as np
from Models.FHN import FHN
from simulation import path_calling


def deterministic(v0,w0):
    I_ext,a,b,tau =path_calling()

    dt = 0.01        # timestep
    T = 1000           # total time
    steps = int(T/dt)

    v = np.zeros(steps)
    w = np.zeros(steps)
    t = np.linspace(0, T, steps)

    neuron = FHN(a, b, tau, I_ext)

    # Initial conditions
    v[0] = v0
    w[0] = w0

    # Time evolution loop
    for i in range(1, steps):
        v[i] = v[i-1] + neuron.f(v[i-1], w[i-1])*dt
        w[i] = w[i-1] + neuron.g(v[i-1], w[i-1])*dt

    print("v values:",v)
    print("w values:",w)
    v_e, w_e = neuron.get_equilibrium()  
    print("Equilibrium function:", (v_e, w_e))
    J, J_e = neuron.jacobian()
    print("Jacobian Function:", J_e)
    neuron.is_excitable()

    return v,w,v_e,w_e,J_e
