# py2cfg
Python3 control flow graph generator

`py2cfg` is a package that can be used to produce control flow graphs (CFGs) for Python 3 programs. 
The CFGs it generates can be easily visualised with graphviz and used for static analysis. 
This analysis is the main purpose of the module.

Below is an example of a piece of code that generates the Fibonacci sequence and the CFG produced for it with py2cfg.

```py
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib_gen = fib()
for _ in range(10):
    next(fib_gen)
```

![Fibonacci CFG](fib_cfg.png)

See `./examples/` for more examples

## Installation
To install simply run
```
pip3 install ccfg
```

## Usage
It can be used three ways:

### Via CLI

The default command is ccfg:
```py
ccfg <file.py>
``` 

This will create a <file>_cfg.png file, which contains the colored cfg of the file.

### Via wrapper
The `cfg` script present in the *wrapper/* folder of this repository can be used to directly generate the CFG of some Python program and visualise it.
```sh
python3 ccfg path_to_my_code.py
```

### Via import
To use py2cfg, simply import the module in your Python interpreter or program, and use the `py2cfg.CFGBuilder` class to build CFGs. 
For example, to build the CFG of a program defined in a file with the path *./example.py*, the following code can be used:

```py
from py2cfg import CFGBuilder

cfg = CFGBuilder().build_from_file('example', './example.py')
```

This returns the CFG for the code in *./example.py* in the `cfg` variable. 
The first parameter of `build_from_file` is the desired name for the CFG, and the second one is the path to the file containing the source code.
The produced CFG can then be visualised with:

```py
cfg.build_visual('exampleCFG', 'pdf')
```

The first paramter of `build_visual` is the desired name for the DOT file produced by the method, and the second one is the format to use for the visualisation.

# History
Note: this is a significantly re-worked fork of the following project:
* https://github.com/coetaur0/staticfg
* https://pypi.org/project/staticfg/
