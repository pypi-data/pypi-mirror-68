[![Build Status](https://travis-ci.org/cluster311/pywisc.svg?branch=master)](https://travis-ci.org/cluster311/pywisc)

# Py Wisc

Calculos para WISC en diferentes versiones y diferentes paises.  
**Status**: En desarrollo. No funciona todavía.

## Install

Publicado en [Pypi](https://pypi.org/project/pywisc/)

```
pip install pywisc
```

## Comandos

Esta aplicación se puede usar desde la línea de comandos

```
$ wisc
##########################
Calculador WISC 4. Versión español, Argentina
##########################
Fecha de nacimiento 
	Formato: Formatos permitidos: AAAA-MM-DD o DD/MM/AAAA. Por ejemplo 2020-12-01 o 01/12/2020
2014-03-12
Fecha de evaluación 
	Formato: Formatos permitidos: AAAA-MM-DD o DD/MM/AAAA. Por ejemplo 2020-12-01 o 01/12/2020
	Predeterminado: 2020-05-01

Comprension verbal-Semejanzas (CV-S):10
Comprension verbal-Vocabulario (CV-V):10
Comprension verbal-Comprensión (CV-C):10
Razonamiento Perceptivo-Construcción de cubos (RP-CC):10
Razonamiento Perceptivo-Conceptos (RP-Co):10
Razonamiento Perceptivo-Matrices (RP-M):10
Memoria Operativa-Retención de dígitos (MO-RD):10
Memoria Operativa-Letras y números (MO-LN):10
Velocidad de procesamiento-Claves (VP-Cl):10
Velocidad de procesamiento-Búsqueda de símbolos (VP-BS):10
Calc over {'S': 10, 'V': 10, 'C': 10, 'CC': 10, 'Co': 10, 'M': 10, 'RD': 10, 'LN': 10, 'Cl': 10, 'BS': 10}
CI calculado: 89
```

## En Python

```python
from pywisc.wisc import Wisc
from pywisc.evaluacion import Evaluacion


directas_por_subtest =  {'S': 10, 'V': 10, 'C': 10, 'CC': 10,
                         'Co': 10, 'M': 10, 'RD': 10, 'LN': 10,
                         'Cl': 10, 'BS': 10}

w = Wisc(wisc_version=4, language='es', country='ar')
e = Evaluacion(wisc=w)
reqs = {'born_date': '2014-03-01', 'test_date': '2020-04-29'}
e.validate_reqs(reqs=reqs)
e.calculate_age()
ci = e.calculate_ci(directas=directas_por_subtest)
assert ci == 89
```

## Tests

```
python -m pytest -s
```