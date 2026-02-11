import numpy as np
from Models.FHN import FHN
from simulation import path_calling

def multiplicative_noise(v0,w0):
    """
    Simulates the FitzHugh-Nagumo (FHN) model with multiplicative stochastic noise 
    using a Second-Order Stochastic Runge-Kutta (Heun) method.
    
    In this implementation, the noise intensity scales with the state variable 'w'.
    The SRK method is used to maintain numerical stability and accuracy that 
    Euler-Maruyama might lose when dealing with state-dependent noise.
    
    Args:
        v0 (float): Initial condition for membrane potential.
        w0 (float): Initial condition for recovery variable.
        
    Returns:
        tuple: (v, w, v_e, w_e, J_e) arrays of states, equilibrium points, and Jacobian.
    """
    I_ext,a,b,tau = path_calling()
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
        sigma = 0.02
        delta_B = np.sqrt(dt) * np.random.normal(0, 1)
        v_predictor = v[i-1] + neuron.f(v[i-1], w[i-1])*dt
        w_predictor = w[i-1] + neuron.g(v[i-1], w[i-1]) * dt + (sigma*delta_B*w[i-1])
        v[i] = v[i-1] + (1/2)*((neuron.f(v[i-1], w[i-1])) + (neuron.f(v_predictor, w_predictor)))*dt
        w[i] = w[i-1] +(1/2)*((neuron.g(v[i-1], w[i-1]))+(neuron.g(v_predictor, w_predictor)))*dt + (1/2)*sigma*(w[i-1]+w_predictor)*delta_B

    print("v values:",v)
    print("w values:",w)
    v_e, w_e = neuron.get_equilibrium()  
    print("Equilibrium function:", (v_e, w_e))
    J, J_e = neuron.jacobian()
    print("Jacobian Function:", J_e)
    neuron.is_excitable()

    return v,w,v_e,w_e,J_e