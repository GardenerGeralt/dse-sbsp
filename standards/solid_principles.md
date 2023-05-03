Write SOLID Code
----------------

SOLID is a set of software development principles, commonly 
used in Agile software projects of any scale. It has strong
benefits in making code easier to use, reuse, and maintain.

[Wikipedia: SOLID](https://en.wikipedia.org/wiki/SOLID):

> - The **S**ingle-responsibility principle: "There should 
never be more than one reason for a class to change." 
In other words, every class should have only one responsibility.
> - The **O**pen–closed principle: "Software entities ... 
should be open for extension, but closed for modification."
> - The **L**iskov substitution principle: "Functions that use 
pointers or references to base classes must be able to use 
objects of derived classes without knowing it." See also 
design by contract. *(this is less relevant to us)*
> - The **I**nterface segregation principle: "Clients should 
not be forced to depend upon interfaces that they do not use." 
> - The **D**ependency inversion principle: "Depend upon 
abstractions, **not** concretions."

I know this is a bit cryptic, so the following examples should
make things clear.

### Single-responsibility principle:

Every class should only have one purpose, and every function 
should do only one thing. There should then be interface 
functions that join them.

Do this:
```python
def read_data():
    return ...  # this function only reads the data

def orbit_period(altitude):
    return ...  # this function only calculates orbit period

def main():  # this function acts as the interface
    data = read_data()
    return orbit_period(data['altitude'])
```

Not this:
```python
def main():
    ...  # line that reads the data
    ...  # line that calculates orbit period
    return ...  # this function acts as the interface
```

### Open-closed principle:

Once you have pushed your code to dev, that means it is 
ready for use. Therefore, if you then proceed to change that 
code, that may break any code made by your teammates using 
your code. Hence: **never modify, - only extend**. You may, 
of course, modify and prototype in your own branch as much
as you want, before publishing to dev.

### Interface segregation principle:

This circles back to the single-responsibility principle. 
Create interface functions to communicate between regular 
functions. This will (hopefully) ensure that any changes to
a specific function `abc()` do **not** propagate any further 
than the interface function. That is, you might have to 
change the interface after changing the function `abc()`, 
but at least you will not have to do that for every single 
other function that uses `abc()`

### Dependency inversion principle:

Now this one is perhaps the most cryptic of all. Basically,
what it says is that you should not change the way your code 
looks on the outside because of how it works on the inside, 
but do the opposite. This is, again, so that the end user
(be that a customer or a teammate) does not have to re-learn 
how to use your code.
