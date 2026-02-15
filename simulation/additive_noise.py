import numpy as np
from Models.FHN import FHN
from Models.LIF import LIF
from simulation.path_calling import path_calling_fhn
from simulation.path_calling import path_calling_lif

def additive_noise_fhn(v0,w0, sigma):
    """
    Simulates the FitzHugh-Nagumo (FHN) model with additive stochastic noise 
    using the Euler-Maruyama numerical method.
    
    The Euler-Maruyama method is an extension of the Euler method for SDEs:
    v(t+dt) = v(t) + f(v, w)*dt
    w(t+dt) = w(t) + g(v, w)*dt + sigma * dW
    
    where dW is a Wiener process increment (Brownian motion) sampled from 
    a Normal distribution N(0, sqrt(dt)).
    Brownian motion (the dW term in an SDE) has a variance that grows linearly with time. 
    To keep the noise consistent across different step sizes, the random displacement must 
    be scaled by the square root of the time interval.
    """

    # Load model parameters from centralized config
    I_ext,a,b,tau = path_calling_fhn()
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
        # Noise intensity parameter (sigma)
        noise = sigma * np.random.normal(0, 1) * np.sqrt(dt)
        # Calculate the Wiener increment dW. 
        # For Brownian motion, variance scales with dt, so std_dev scales with sqrt(dt).
        v[i] = v[i-1] + neuron.f(v[i-1], w[i-1])*dt
        w[i] = w[i-1] + neuron.g(v[i-1], w[i-1]) * dt + noise

    #print("v values:",v)
    #print("w values:",w)
    v_e, w_e = neuron.get_equilibrium()  
    #print("Equilibrium function:", (v_e, w_e))
    J, J_e = neuron.jacobian()
    #print("Jacobian Function:", J_e)
    #neuron.is_excitable()

    return v,w,v_e,w_e,J_e


def additive_noise_lif():
    dt = 0.01        # timestep
    T = 1000           # total time
    steps = int(T/dt)

    I_ext, R, V_r, sigma, tau = path_calling_lif()

    neuron_2 = LIF(I_ext,R, V_r, sigma, tau)
    v = np.zeros(steps)

    v[0] = V_r

    for i in range(1, steps):
        noise = sigma * np.random.normal(0, 1) * np.sqrt(dt)
        v[i] = v[i-1] + neuron_2.leaky_integrate_and_fire_model(v[i-1])*dt + noise

    return v
