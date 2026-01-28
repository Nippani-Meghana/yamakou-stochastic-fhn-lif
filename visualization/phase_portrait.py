import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json
from Models.FHN import FHN

# BASE_DIR = Path(__file__).resolve().parent.parent
# __file__ is the path to the current Python script.
# Path(__file__).resolve() converts it into an absolute path.
# .parent goes one folder up. .parent.parent goes two folders up.
BASE_DIR = Path(__file__).resolve().parent.parent  # points to project/

# This uses Python’s pathlib “/” operator to join paths safely.
json_path = BASE_DIR / "config" / "fhn_params.json"

# Opens the JSON file for reading. The with statement ensures it automatically closes afterward.
with open(json_path) as f:
# Reads the JSON file and converts it into a Python dictionary (dict).
    params = json.load(f)

    
# Access parameters
I_ext = params["fhn_parameters"]["I_ext"]
a = params["fhn_parameters"]["a"]
b = params["fhn_parameters"]["b"]
tau = params["fhn_parameters"]["tau"]

dt = 0.01        # timestep
T = 1000           # total time
steps = int(T/dt)

v = np.zeros(steps)
w = np.zeros(steps)
t = np.linspace(0, T, steps)
neuron = FHN(a, b, tau, I_ext)

# Initial conditions
v[0] = -1.00125
w[0] = -0.46  #M.E. Yamakou et al. paper Fig.1 shows two trajectories w = -0.45, -0.46
#A large "action potential" loop starting at w = -0.46
#A small sub-threshold oscillation starting at w = -0.45

# Time evolution loop
for i in range(1, steps):
    v[i] = v[i-1] + neuron.f(v[i-1], w[i-1])*dt
    w[i] = w[i-1] + neuron.g(v[i-1], w[i-1])*dt

v_e, w_e = neuron.get_equilibrium()  

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