import os
import dill
from plumbum import local
from pathlib import Path

def get_env_path(env_name):
    "get python path in conda env"
    env_path = Path(os.environ["CONDA_PREFIX"]) / "envs" / env_name / "bin" / "python"
    if not env_path.exists():
        raise FileNotFoundError(f"Python not found in {env_path}")
    return env_path

def serialize(data_dict, file):
    "serialize data_dict to file"
    serialized_data_dict = {name: dill.dumps(data) for name, data in data_dict.items()}
    with open(file, "wb") as f:
        dill.dump(serialized_data_dict, f)

def deserialize(file):
    "deserialize data_dict from file"
    with open(file, "rb") as f:
        data_dict = dill.load(f)
        return {name: dill.loads(data) for name, data in data_dict.items()}
            
class Submodule:
    
    def __init__(self):
        self.data_dict = {}
    
    def call(self, input_data, env_name, script_path, verbose=False):
        project_dir = Path(__file__).parent.parent
        script_abspath = project_dir / script_path
        print(
            f"[Submodule call] \033[34mInfo\033[0m: Start run submodule {script_path} in {env_name}"
        )
        pkl_file = script_abspath.parent / "data.pkl"
        serialize(input_data, pkl_file)
        python = local[get_env_path(env_name)]
        cmd = python[script_abspath]
        output = cmd()
        if verbose:
            print(output)
        
        print(
            f"[Submodule call] \033[34mInfo\033[0m: End run submodule {script_path} in {env_name}!"
        )
        return deserialize(pkl_file)
