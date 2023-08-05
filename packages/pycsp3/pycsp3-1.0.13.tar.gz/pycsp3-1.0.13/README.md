

This is the github to deal with the pypi of pycsp3 project:

To clone the project with pycsp3:

git clone --recurse-submodules https://github.com/xcsp3team/ppycsp3.git

To push a new version on pypi:

pip install wheel
pip install twine
python update_pypi_version.py

if you have a problem: 
pip install -U pip
pip install -U twine wheel setuptools
python update_pypi_version.py


