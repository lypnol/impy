# Impy

IMP language interpreter with formal coverage testing.  
Labeling is optional on programs (see examples).

## Install and usage

impy runs under python 3.6 or higher, install dependencies with pip:
```
pip install -r requirements.txt
```

```
usage: im.py [-h]
             [-t {TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} [{TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} ...]
             | --all-tests] [-i INPUT | -gp | -gf] [--timeout TIMEOUT]
             [--k-paths K_PATHS] [--i-loops I_LOOPS]
             source

IMP language interpreter

positional arguments:
  source                Path to source code file

optional arguments:
  -h, --help            show this help message and exit
  -t {TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} [{TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} ...], --tests {TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} [{TA,TD,TC,k-TC,i-TB,TDef,TU,TDU} ...]
                        Runs specific coverage tests
  --all-tests           Runs all available coverage tests
  -i INPUT, --input INPUT
                        Input state set for tests (json file)
  -gp, --generate-pass  Generate state set that passes coverage tests
  -gf, --generate-fail  Generate state set that fails coverage tests
  --timeout TIMEOUT     States generation timeout (seconds)
  --k-paths K_PATHS     Paramter of k-TC test
  --i-loops I_LOOPS     Paramter of i-TB test
```

## Examples

Run IMP program
```
$ ./im.py examples/src/prog1.imp
Enter initial state
x: 5
Program terminated 0.213 ms.
x: -3
```

Run AllAssignmentsTest on prog1.imp:
```
$ ./im.py examples/src/prog1.imp -t TA -i examples/tests/TA.json
AllAssignmentsTest pass
```
 