<br>
<p align="center">
<h1 align="center"><strong>BestMan: A Versatile Mobile Manipulation Platform with Seamless
Sim2Real Integration and Modular Algorithm Deployment</strong></h1>
  <p align="center">
    College of Computer Science,Chongqing University&emsp;&emsp;&emsp;&emsp;Shanghai AI Laboratory
  </p>
  
  <p align="center">
    State Key Laboratory of Mechanical Transmission for Advanced Equipment, Chongqing University
  </p>
</p>

<div id="top" align="center">

![](docs/_static/BestMan/BestMan_logo_AL.png)

[![arxiv](https://img.shields.io/badge/arxiv-2410.13407-orange)](http://arxiv.org/abs/2410.13407)
[![paper](https://img.shields.io/badge/Paper-%F0%9F%93%96-yellow)](https://arxiv.org/pdf/2410.13407)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/facebookresearch/home-robot/blob/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://timothycrosley.github.io/isort/)
[![Document](https://img.shields.io/badge/Document-%F0%9F%93%98-green)](https://bestman-pybullet.readthedocs.io)

![](docs/static/asset/image/Asset_Overview.svg)

Welcome to the official repository of BestMan!

A mobile manipulator (with a wheel-base and arm) platform built on PyBullet simulation with unified hardware APIs.

</div>

## 📋 Contents

- [📋 Contents](#-contents)
- [🔥 News](#-news)
- [🎯 Framework](#-framework)
- [🏠 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [👨‍💻 Examples](#-examples)
  - [🚀 Run](#-run)
  - [🎇 Render](#-render)
- [📝 TODO List](#-todo-list)
- [🤝 Reference](#-reference)
- [👏 Acknowledgements](#-acknowledgements)
- [🚀 Working citing BestMan](#-working-citing-bestman)

## 🔥 News
- [2024-02] We released version 0.3.0, long version of the paper submitted to IROS 2025.
- [2024-11] We released version 0.2.0, optimizing modules such as Install and Robotics API.
- [2024-10] We release the [paper](http://arxiv.org/abs/2410.13407) of BestMan.

## 🎯 Framework

![Framework](docs/static/asset/image/BestMan_Framework.png)

## 🏠 Getting Started

### Prerequisites

> ***Note**: We recommand Ubuntu 22.04 and python version deault to 3.8.*

- Ubuntu 20.04, 22.04
- Conda 
  - Python 3.8, 3.9, 3.10

### Installation

We provide the installation guide [here](Install/install.md). You can install locally or use docker and verify the installation easily.

## 👨‍💻 Examples

### 🚀 Run

Enter `Examples` directory and run the demos. You can also modify the parameters corresponding to the demo.

### 🎇 Render

`open microwave` demo in **Overview** before blender rendering:

<video src="https://github.com/user-attachments/assets/fb8ef3ea-d045-4bbf-a28f-0bec56930aae"></video>

<br/>

We have improved the [pybullet-blender-recorder](https://github.com/huy-ha/pybullet-blender-recorder) to import pybullet scene into blender for better rendering

If you want to enable **pybullet-blender-recorder**, please：

1. Install the `pyBulletSimImporter.py` plugin under **Visualization/blender-render** directory in blender (Edit->Preferences->Add-ons->Install) (test on **blender3.6.5**) , and enalbe this plugin.

<img width="1040" alt="image" src="https://github.com/user-attachments/assets/ab9e99c7-64c8-40fe-bbfe-edc0c786b812">
  
2. Set `blender: Ture` in **Config/xxx.yaml**.

3. After running the demo, a pkl file will be generated and saved in **Examples/record** dir

4. Import the pkl files into blender.

> Note: This will freeze the current blender window before the processing is completed, please wait.

<img width="1040" alt="image" src="https://github.com/user-attachments/assets/c0fe66e8-347e-4ecc-b367-8b0c3592d329">

<br/>
<br/>

> Note: If the demo contains too many frames, you can change `pyBulletSimImporter.py`: ANIM_OT_import_pybullet_sim(): **skip_frames** parameters and reinstall in blender to reduce the number of imported frames.
<br/>

## 📝 TODO List

- \[x\] Release the platform with basic modules、functions and demos.
- \[x\] Polish APIs, related codes, and release documentation.
- \[x\] Release the paper with framework and demos Introduction.
- \[ \] Release the baseline models and benchmark modules.
- \[ \] Dynamically integrate digital assets.
- \[ \] Comprehensive improvement and further updates.


## 🤝 Reference

If you find this work useful, please consider citing:

```
@inproceedings{Yang2024BestManAM,
  title={BestMan: A Modular Mobile Manipulator Platform for Embodied AI with Unified Simulation-Hardware APIs},
  author={Kui Yang and Nieqing Cao and Yan Ding and Chao Chen},
  year={2024},
  url={https://api.semanticscholar.org/CorpusID:273403368}
}
```

## 👏 Acknowledgements

We would like to express our sincere gratitude to all the individuals and organizations who contributed to this project.

For a detailed list of acknowledgements, please refer to [appendix](docs/appendix.md).

## 🚀 Working citing BestMan

Research has already been conducted based on the BestMan platform. If you are interested, please visit [here](https://bestmanrobot.com/Works_Citing_BestMan) for more details.
