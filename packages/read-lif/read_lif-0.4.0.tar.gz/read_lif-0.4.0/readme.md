# read_lif

Load 3D confocal images from `lif` files as `numpy` arrays.

The code was originally written by Mathieu Leocmach in package [colloids](https://github.com/MathieuLeocmach/colloids).

## Install

- The most convenient way would be: `pip install read_lif`
- You can also Include the file `read_lif` in your project directory

## How to Use It

```python
import read_lif

reader = read_lif.Reader('lif_file.lif')
series = reader.getSeries()
chosen = series[0]  # choose first image in the lif file
# get a numpy array corresponding to the 1st time point & 1st channel
# the shape is (z, y, x)
image = chosen.getFrame(T=0, channel=0)
```
