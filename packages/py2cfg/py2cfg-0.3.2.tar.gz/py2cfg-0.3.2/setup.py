# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py2cfg']

package_data = \
{'': ['*']}

modules = \
['fib_cfg']
install_requires = \
['astor>=0.8.1,<0.9.0', 'graphviz>=0.11,<0.12']

entry_points = \
{'console_scripts': ['py2cfg = py2cfg._runner:main']}

setup_kwargs = {
    'name': 'py2cfg',
    'version': '0.3.2',
    'description': 'Converts python source code to colorfor Control Flow Graphs (CFGs).',
    'long_description': "# py2cfg\nPython3 control flow graph generator\n\n`py2cfg` is a package that can be used to produce control flow graphs (CFGs) for Python 3 programs. \nThe CFGs it generates can be easily visualised with graphviz and used for static analysis. \nThis analysis is the main purpose of the module.\n\nBelow is an example of a piece of code that generates the Fibonacci sequence and the CFG produced for it with py2cfg.\n\n```py\ndef fib():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\nfib_gen = fib()\nfor _ in range(10):\n    next(fib_gen)\n```\n\n![Fibonacci CFG](fib_cfg.png)\n\nSee `./examples/` for more examples\n\n## Installation\nTo install simply run\n```\npip3 install ccfg\n```\n\n## Usage\nIt can be used three ways:\n\n### Via CLI\n\nThe default command is ccfg:\n```py\nccfg <file.py>\n``` \n\nThis will create a <file>_cfg.png file, which contains the colored cfg of the file.\n\n### Via wrapper\nThe `cfg` script present in the *wrapper/* folder of this repository can be used to directly generate the CFG of some Python program and visualise it.\n```sh\npython3 ccfg path_to_my_code.py\n```\n\n### Via import\nTo use py2cfg, simply import the module in your Python interpreter or program, and use the `py2cfg.CFGBuilder` class to build CFGs. \nFor example, to build the CFG of a program defined in a file with the path *./example.py*, the following code can be used:\n\n```py\nfrom py2cfg import CFGBuilder\n\ncfg = CFGBuilder().build_from_file('example', './example.py')\n```\n\nThis returns the CFG for the code in *./example.py* in the `cfg` variable. \nThe first parameter of `build_from_file` is the desired name for the CFG, and the second one is the path to the file containing the source code.\nThe produced CFG can then be visualised with:\n\n```py\ncfg.build_visual('exampleCFG', 'pdf')\n```\n\nThe first paramter of `build_visual` is the desired name for the DOT file produced by the method, and the second one is the format to use for the visualisation.\n\n# History\nNote: this is a significantly re-worked fork of the following project:\n* https://github.com/coetaur0/staticfg\n* https://pypi.org/project/staticfg/\n",
    'author': 'Joe Studer',
    'author_email': 'jmsxw4@mst.edu',
    'url': 'https://git.mst.edu/autograding/py2cfg',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
