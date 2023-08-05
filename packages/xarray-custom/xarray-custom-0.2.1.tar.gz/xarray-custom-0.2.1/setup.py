# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_custom']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'xarray>=0.15,<0.16']

setup_kwargs = {
    'name': 'xarray-custom',
    'version': '0.2.1',
    'description': 'Data classes for custom xarray constructors',
    'long_description': '# xarray-custom\n\n[![PyPI](https://img.shields.io/pypi/v/xarray-custom.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/xarray-custom/)\n[![Python](https://img.shields.io/pypi/pyversions/xarray-custom.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/xarray-custom/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/xarray-custom/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/xarray-custom/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\n:zap: Data classes for custom xarray constructors\n\n## TL;DR\n\nxarray-custom is a Python package which helps to create custom DataArray classes in the same manner as [the Python\'s native dataclass](https://docs.python.org/3/library/dataclasses.html).\nHere is an introduction code of what the package provides:\n\n```python\nfrom xarray_custom import coordtype, dataarrayclass\n\n\n@dataarrayclass((\'x\', \'y\'), float, \'custom\')\nclass CustomDataArray:\n    x: coordtype(\'x\', int)\n    y: coordtype(\'y\', int)\n    z: coordtype((\'x\', \'y\'), str) = \'spam\'\n\n    def double(self):\n        """Custom DataArray method which doubles values."""\n        return self * 2\n\n\ndataarray = CustomDataArray([[0, 1], [2, 3]], x=[2, 2], y=[3, 3])\nonesarray = CustomDataArray.ones(shape=(3, 3))\ndoubled = dataarray.custom.double()\n```\n\nThe key points are:\n\n- Custom DataArray instances with fixed dimensions and coordinates can easily be created.\n- Default values and dtype can be specified via a class decorator and class variable annotations.\n- NumPy-like special factory functions like ``ones()`` are provided as class methods.\n- Custom DataArray methods can be used via a custom accessor.\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/xarray-custom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
