# Energy performance of buildings

This library provides helpers for energy performance of buildings computation.

## Installing

### With PIP

```sh
pip install epb
```

### With Poetry

```sh
poetry add epb
```

## Usage

```py
from epb.utils import Regulator, energy_class, total_consumption


eclass = energy_class(Regulator.BRUSSELS, 100)
# eclass == "C+"


tconsum = total_consumption(100, 250)
# tconsum == 25_000
```
