# rmodel

UI for an R-like experience of simple statistical modelling, but in Python.

# installation

````{bash}
pip3 install rmodel
````
or git-clone it.

# example

Install **matplotlib** separately first with
````{bash}
pip3 install matplotlib
````

Then, to fit to a second order polynomial, simply do:

````{python}
from rmodel.polyfit import polyfit

P = polyfit(x=[1,2,3,4], y=[1.2, 3.5, 4.4, 5.5], deg=2)
P.plot()
````

The model stores the data and can provide fits, coefficients, results, and errors quite easily:

```{python}
P.fitted()
P.coef
P.res()
P.error_l1()
P.average_l1()
```
