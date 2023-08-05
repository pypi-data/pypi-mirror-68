import setuptools

from distutils.util import convert_path

long_description ="""
# GPIOEmulator

The easiest way to use this package is to install using pip for python 2.7

```bash
$ sudo pip install GPIOEmulator
```

using pip3 for python 3

```bash
$ sudo pip3 install GPIOEmulator
```

To use the emulator just type the following at the beginning of your script.

```python
from GPIOEmulator.EmulatorGUI import GPIO
```

## Works with

- [python 2.7.15+](https://www.python.org/downloads/release/python-2715/)
- [python 3.6.8](https://www.python.org/downloads/release/3.6.8)

## Simulation

This library simulates the following functions which are used in the RPi.GPIO library.

- GPIO.setmode()
- GPIO.setwarnings()
- GPIO.setup()
- GPIO.input()
- GPIO.output()
"""

with open('requirements.txt', 'r') as requirements_file:
  requirements_text = requirements_file.read()

requirements = requirements_text.split()

pkg_ns = {}

ver_path = convert_path('GPIOEmulator/__init__.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), pkg_ns)

setuptools.setup(
      name='GPIOEmulator',
      version=pkg_ns['__version__'],
      description='This package was made with pip-boilerplate',
      url='https://github.com/codenio/',
      author='Aananth K',
      author_email='aananthraj1995@gmail.com',
      license='GPL-3.0',
      packages=setuptools.find_packages(),
      zip_safe=False,
      long_description_content_type="text/markdown",
      long_description=long_description,
      install_requires=requirements
)