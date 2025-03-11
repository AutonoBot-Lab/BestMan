# Installation

## Install with conda (Linux)

### Basic Env

> ***Note**: This will only install the basic module. For other algorithm submodules, please follow the instructions [Algorithm Submodule Env](#algorithm-submodule-env) to install as needed.*

1. Pull the repository and update the submodule

```
git clone https://github.com/AutonoBot-Lab/BestMan_Pybullet.git
cd BestMan_Pybullet
git submodule update --init --recursive
```

2. Run the following script to add the project to the PYTHON search path
```
cd Install
chmod 777 pythonpath.sh
bash pythonpath.sh
source ~/.bashrc
```


3. Install ffmpeg to enable video record
```
sudo apt update && sudo apt install ffmpeg
```

4. Configure related libraries and links to support OpenGL rendering (If it already exists, skip this step.)
```
sudo apt update && sudo apt install -y libgl1-mesa-glx libglib2.0-0
sudo mkdir /usr/lib/dri
sudo ln -s /lib/x86_64-linux-gnu/dri/swrast_dri.so /usr/lib/dri/swrast_dri.so
```

5. Install gcc/g++ 9 (If it already exists, skip this step.)
```
sudo apt install -y build-essential gcc-9 g++-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 9
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 9
sudo update-alternatives --config gcc  # choice gcc-9
sudo update-alternatives --config g++  # choice g++-9

# Make sure gcc and g++ versions are consistent (conda enviroment don't install gcc to prevent problems caused by inconsistent versions)
gcc -v
g++ -v
```

6. Configure mamba to speed up the conda environment construction (**Optional**, skip if installation is slow or fails)
```
conda install mamba -n base -c conda-forge
```

7. Create basic conda environment

> ***Note**: If you want to install for other python version, please change to basic_env_pyxxx.yaml.*

```
conda(mamba) env create -f basic_env_py38.yaml
conda(mamba) activate BestMan
```

### Algorithm Submodule Env

> ***Note**: In order to prevent conflicts in environment dependencies between different algorithm submodules in each module, we isolate the environments of each algorithm submodule of BestMan from each other for efficient management and calling.*

If you want to install and use centain submodule, please see `install.md` in submodule dir. Such as:

- [Lang SAM](../Perception/Object_detection/Lang_SAM/install.md)
- [AnyGrasp](../Perception/Grasp_Pose_Estimation/AnyGrasp/install.md)
- [URDFormer](../DigitalTwin/urdformer/install.md)
- [ACDC](../DigitalTwin/acdc/install.md)
- [PDDLStream](../Task_Planning/pddlstream/install.md)

During the installation of these submodules, due to different GPU driver versions, the correspondence between torch, cuda and related library versions may need to be adjusted. It is recommended to refer to [here](https://pytorch.org/get-started/previous-versions/)


## Install with Docker (Windows)

> ***Note**: Docker image does not include submodules such as LangSAM and Anygrasp, only basic installation.*

1. Pull BestMan docker image

```
docker pull crpi-9cw0y3g974qhulj0.cn-hangzhou.personal.cr.aliyuncs.com/leeyanyu/bestman:0.1.0
```

2. Create docker container

```
docker run -it --gpus all --name BestMan crpi-9cw0y3g974qhulj0.cn-hangzhou.personal.cr.aliyuncs.com/leeyanyu/bestman:0.1.0
```

3. Install [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/), Start and keep running in the background.

4. Execute `echo $DISPLAY` inside the container, Make sure the result is `host.docker.internal:0` so that it can be visualized on the host machine, if not:

```
export DISPLAY=host.docker.internal:0
```


## Install with Docker (Linux)

Coming soon
