import numpy as np
from pathlib import Path
import json

import Models.FHN as fhn 

BASE_DIR = Path(__file__).resolve().parent.parent  # points to project/
json_path = BASE_DIR / "config" / "fhn_params.json"

with open(json_path) as f:
    params = json.load(f)

# Access parameters
I_ext = params["fhn_parameters"]["I_ext"]
a = params["fhn_parameters"]["a"]
b = params["fhn_parameters"]["b"]
tau = params["fhn_parameters"]["tau"]

v = np.linspace(-2.5,2.5,400)
w = np.linspace(-1,2,400)
V,W = np.meshgrid(v,w)

dV = f(V,W)
dW = w(V,W)

