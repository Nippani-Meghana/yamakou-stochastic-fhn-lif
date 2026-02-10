from pathlib import Path
import json

def path_calling():
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
