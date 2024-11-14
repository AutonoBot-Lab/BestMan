# Object model

## Overview

Here are the object resources that can be used in BestMan：

| Object Resource   |  Reference | Description |
| -------- | -------- | -------- |
| [Kitchen_world_models](https://github.com/starry521/Kitchen_world_models/tree/e3b15702a11d9aa7f409f5eacad88e75ef53b006)  | [kitchen-models](https://github.com/zt-yang/kitchen-models/tree/64f1a7696c6517cf9b7681ad21b02404364e33f5) | Kitchen Worlds **articulated** object urdf models, which comes from [PartNet Mobility dataset](https://sapien.ucsd.edu/browse)
| [URDF_models](https://github.com/yding25/URDF_models/tree/4f5c0f342b202f9aeaec95d53b138d87e213f2c9)  | [pybullet-URDF-models](https://github.com/ChenEating716/pybullet-URDF-models) | Collection of **rigid** object urdf models, part of it comes from [YCB dataset](http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/)
| [URDFormer_models](https://drive.google.com/file/d/1aP6-XEzAGtmEBiDXangddSJ_IcvERlA4/view) | / | URDFormer officially provides five object categories for generation: **cabinet**, **oven**, **dishwasher**, **fridge** and **washer** urdf models and one scene type: **kitchen**
| [Free3D](https://free3d.com/3d-models/) | / | Provides object models, but not articulated object

## Object extension

1. [URDFormer](../../../DigitalTwin/urdformer/README.md)

You can use URDFormer submodule to generate urdf model from image

2. [deemos hyperhuman](https://hyperhuman.deemos.com/rodin)

You can use hyperhuman to generate 2D RGB image to 3D model
