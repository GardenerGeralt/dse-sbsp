Documentation Standards
-----------------------

Proper documentation is crucial for making you code easier to 
use and maintain for the rest of the team. In this document, 
three methods of code documentation are proposed in order of
importance.

### Docstrings

Docstrings are a very straightforward and useful way of 
documenting a function, and I hope that you will make one for 
every function you write. When you hover over a function with 
a docstring, your IDE will display information about the 
function's purpose, inputs, and outputs. Below is a 
(shortened) example docstring from the `numpy.linspace()` 
function.

```python
def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0):
    """
    Return evenly spaced numbers over a specified interval.
    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].
    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True
        Size of spacing between samples.
    Examples
    --------
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    """
```

In our case we do not have to be this extensive, but this 
example should demonstrate how to document most things in a
docstring. Also, notice that docstrings are written in 
Markdown format.

For additional information on docstrings, refer to the 
PEP 257 standard.

---

### Self-explanatory Naming

You can avoid writing comments by clearly naming your 
variables, functions, classes, and constants. That means 
**no names that are shorter than three letters**. When 
naming something, just ask yourself if someone else would 
understand what that thing is/does just based on its name.
Although, you might still need to add a comment sometimes.

---

### Module Documentation

This should usually not be necessary, but if you find it 
useful to document your code more extensively, you can create
a Markdown file for your module in the `docs` directory.
