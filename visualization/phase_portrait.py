import matplotlib.pyplot as plt
import numpy as np
from Models.FHN import FHN
import simulation

I_ext,a,b,tau = simulation.path_calling()

neuron = FHN(a, b, tau, I_ext)

def det_phase_portrait():
    #M.E. Yamakou et al. paper Fig.1 shows two trajectories w = -0.45, -0.46
    #A large "action potential" loop starting at w = -0.46
    #A small sub-threshold oscillation starting at w = -0.45
    v,w,v_e,w_e,J_e = simulation.deterministic(-1.00125,-0.46)

    return v,w,v_e,w_e

def add_noise_phase_portrait():
    v,w,v_e,w_e,J_e = simulation.additive_noise(-1.00125,-0.4)

    return v,w,v_e,w_e

def mult_noise_phase_portrait():
    """
    Why use SRK (Heun) instead of Euler?
    While the Euler-Maruyama method used for additive noise, multiplicative noise 
    (where noise is sigma*w*dW) makes the system much more sensitive.

    The Problem: In Euler methods, the noise is only calculated at the start of the step. 
    If the value of w changes significantly during dt, the noise term becomes inaccurate.

    The Solution: SRK takes a "predictor" step to see where the system is headed, then uses 
    that future value to "correct" the noise and drift estimates.
    """
    v,w,v_e,w_e,J_e = simulation.multiplicative_noise(-1.00125,-0.4)

    return v,w,v_e,w_e


print("====DASHBOARD====")
print("1. Deterministic FHN")
print("2. Stochastive Additive FHN")
print("3. Stochastive Multiplicative FHN")
ch = int(input('Please make your choice: '))
if(ch == 1):
    v,w,v_e,w_e = det_phase_portrait()
elif(ch == 2):
    v,w,v_e,w_e = add_noise_phase_portrait()
elif (ch == 3):
    v,w,v_e,w_e = mult_noise_phase_portrait()
else:
    print("Invalid Choice!")

V = np.linspace(-3,3,400)
W = np.linspace(-1.0,1.5,400)

v_null = V - ((V**3)/3) + I_ext
w_null = (V + a)/b

fig, ax = plt.subplots()

ax.plot(v, w, color='blue')
ax.plot(V, v_null, label = 'v-nullcline',color = 'lightpink')
ax.plot(V, w_null, label = 'w-nullcline',color = '#EFBF04')
ax.plot(v_e, w_e, 'ro', markersize=8, label=f'Eq Point ({v_e}, {w_e})')
ax.set_ylim(-1.0, 1.5)

ax.set_xlabel('v (membrane potential)')
ax.set_ylabel('w (recovery variable)')
ax.set_title('Phase Plane Portrait')
plt.show()