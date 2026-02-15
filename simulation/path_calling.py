from pathlib import Path
import json

def path_calling_fhn():
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

    return I_ext,a,b,tau

def path_calling_lif():
    # BASE_DIR = Path(__file__).resolve().parent.parent
    # __file__ is the path to the current Python script.
    # Path(__file__).resolve() converts it into an absolute path.
    # .parent goes one folder up. .parent.parent goes two folders up.
    BASE_DIR = Path(__file__).resolve().parent.parent  # points to project/

    # This uses Python’s pathlib “/” operator to join paths safely.
    json_path = BASE_DIR / "config" / "lif_params.json"

    # Opens the JSON file for reading. The with statement ensures it automatically closes afterward.
    with open(json_path) as f:
    # Reads the JSON file and converts it into a Python dictionary (dict).
        params = json.load(f)

        
    # Access parameters
    I_ext = params["lif_parameters"]["I_ext"]
    R = params["lif_parameters"]["R"]
    V_r = params["lif_parameters"]["V_r"]
    sigma = params["lif_parameters"]["sigma"]
    tau = params["lif_parameters"]["tau"]
    
    return I_ext, R, V_r, sigma, tau