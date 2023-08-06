# PyIFS
A python3 package for infinite feature selection

### Installation
```sh
$ pip install PyIFS
```

### How to use
```python
import PyIFS
inf = PyIFS.InfFS()
[RANKED, WEIGHT] = inf.infFS(x, y, alpha, supervision, verbose)
```
###### INPUT:
+ `x` is a T by n matrix, where T is the number of samples and n the number of features
+ `y` is a column vector with class labels
+ `alpha` is the mixing parameter
+ `supervision` is a boolean variable (0 = unsupervised version, 1 = supervised version)
+ `verbose` is a boolean variable (0, 1)
###### OUTPUT:
+ `RANKED` are indices of columns in `x` ordered by attribute importance
+ `WEIGHT` are attribute weights with large positive weights assigned to important attributes