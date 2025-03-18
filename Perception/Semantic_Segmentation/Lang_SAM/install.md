# Installation of lang-segment-anything

- Python 3.11

```
conda create -n lang-segment-anything -y python=3.11
conda activate lang-segment-anything
```

- Install torch
  
```
pip install torch==2.4.1 torchvision==0.19.1 --extra-index-url https://download.pytorch.org/whl/cu124
```

- Install lang-segment-anything

```
pip install -U git+https://github.com/starry521/lang-segment-anything
```

- Other package

```
pip install yacs
```