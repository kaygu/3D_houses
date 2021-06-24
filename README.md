# 3D Houses

## Description

We are LIDAR PLANES, active in the Geospatial industry. We would like to use our data to launch a new branch in the insurance business. So, we need you to build a solution with our data to model a house in 3D with only a home address.

## Installation

```shell
git clone git@github.com:kaygu/3D_houses.git
cd 3D_houses
pipwin install -r requirements.txt 
```

## Prerequisite

* Download [Digital Surface Model](https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dsm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DSM,%20raster,%201m) (DSM) & [Digital Terrain Model](https://www.geopunt.be/download?container=dhm-vlaanderen-ii-dtm-raster-1m&title=Digitaal%20Hoogtemodel%20Vlaanderen%20II,%20DTM,%20raster,%201m) (DTM) folders
* Unzip the folders in `./data/DTM/` and `./data/DSM/`
* Name of the folders can be changed in [main.py](https://github.com/kaygu/3D_houses/blob/main/main.py) global variable

## Usage

```shell
python3 main.py
```

## How it works
![3dhouses (5)](https://user-images.githubusercontent.com/50581015/123280735-51479600-d509-11eb-841e-a063cc10c205.png)

## Contributors

[Jesus Bueno](https://github.com/jejobueno)\
[Hakan Ergin](https://github.com/hakanErgin)
