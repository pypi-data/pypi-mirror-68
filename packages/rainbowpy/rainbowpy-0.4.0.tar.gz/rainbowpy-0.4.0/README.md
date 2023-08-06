[![Travis CI w/ Logo](https://img.shields.io/travis/grburgess/rainbowpy/master.svg?logo=travis)](https://travis-ci.org/grburgess/rainbowpy)
[![codecov](https://codecov.io/gh/grburgess/rainbowpy/branch/master/graph/badge.svg)](https://codecov.io/gh/grburgess/rainbowpy)
![PyPI](https://img.shields.io/pypi/v/rainbowpy?style=plastic)
## status
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/grburgess/rainbowpy/master?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/grburgess/rainbowpy?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/grburgess/rainbowpy?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/grburgess/rainbowpy?style=for-the-badge)


# rainbowpy

![alt text](https://raw.githubusercontent.com/grburgess/rainbowpy/master/logo.png)

some of my own custom color tools

```bash
pip install rainbowpy
```


## quick intro

rainbowpy is a simple tool to handle building color maps from a list of colors. There will likely me more features in the future.

You can create a YAML file and place it in:

```bash
$HOME/.rainbowpy/custom_maps.yml
```

which will be read on import will add the created color maps to your mpl library:

The format is

```yaml
apples:
  - "#28CC5F"
  - "#29D48"
  - "#F3232"

iri:
  - "#FEFBE9"
  - "#FCF7D5"
  - "#f5f3c1"
  - "#eaf0b5"
  - "#ddecb5"
  - "#d0e7ca"
  - "#c2e3d2"
  - "#b5ddd8"
  - "#a8d8dc"
  - "#9bd2e1"
  - "#8dcbe4"
  - "#81c4e7"
  - "#7bbce7"
  - "#7eb2e4"
  - "#88a5dd"
  - "#9398d2"
  - "#9b8ac4"
  - "#9d7db2"
  - "#9a709e"
  - "#906388"
  - "#805770"
  - "#684957"
  - "#46353a"


```

```python
import matplotlib.pyplot as plt
import rainbowpy

```

```python

N = 1000
array_dg = np.random.uniform(0, 10, size=(N, 2))
colors = np.random.uniform(-2, 2, size=(N,))
fig, ax = plt.subplots()


ax.scatter(array_dg[:, 0], array_dg[:, 1], c=colors, cmap="iri")


```





![png](rainbowpy_2_1.png)



Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
