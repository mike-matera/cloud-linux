"""
Randomizers for KROZ apps.

Applications that would like to be repeatable based on random seed should use
the randomizers defined here.

This module provides an interface that can be properly seeded in a multithreaded
application. Each library that uses randomization should get a randomizer from
here. Any questions that use randomness should use the functions here instead of
the ones in the `random` module.

This is a drop-in replacement for the `random` library. All you need to do is:

```python
import kroz.random as random
```
"""

import random as sys_random

from kroz import KrozApp

_inst = sys_random.Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
choices = _inst.choices
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
binomialvariate = _inst.binomialvariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits
randbytes = _inst.randbytes


def setup():
    global _inst
    _inst.seed(a=KrozApp.appconfig("random_seed"), version=2)


KrozApp.setup_hook(hook=setup)
