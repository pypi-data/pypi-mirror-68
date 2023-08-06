Utilities (mapping, unmapping, calculating enclosing polygon) for space filling curves (currently only Hilbert). Future plans include minimizing the enclosing polygon, calculating centroids, and supporting more curves like Peano.

### Examples:

Map 31 from the 1-dimension domain [0,64) to x,y in [0,16):

```python
>>> from sfcurves import hilbert
>>> hilbert.forward(31, 64)
(3, 4)
```

Reverse map (3,4) to the 1-dimension [0,64):

```python
>>> hilbert.reverse(3, 4, 64)
31
```

If you're mapping the entire domain, then using the generator is considerably faster:

```python
>>> g = hilbert.generator(64)
>>> next(g)
(0, 0)
>>> next(g)
(0, 1)
```

Calculate an enclosing polygon for the mapped points 0 thru 6 in the 1-dimension domain [0,64) 

```python
>>> hilbert.outline(0, 6, 64)
[(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 0), (2, 0), (1, 0), (1, 1), (0, 1)]
```

