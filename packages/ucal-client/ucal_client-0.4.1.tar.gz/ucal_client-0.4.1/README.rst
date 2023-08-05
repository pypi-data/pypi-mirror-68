Description
-----------
Python client for server from UcalManager server (https://bitbucket.org/zimka_b/ucal_manager/).

Install
-------

To install package run in terminal (or anaconda prompt):
::

   pip install -e git+https://bitbucket.org/zimka_b/ucal_client.git#egg=ucal_client

Tests
-----
To check tests run in terminal (or anaconda prompt):
::

  pip install pytest
  pytest --pyargs ucal_client

Usage
-----
See `example.ipynb` for examples and description.

Docs
----
To build docs goto docs/ and run *make.bat html*
To generate docs from scratch:
::
  
  mkdir docs/
  cd docs/
  sphinx-quickstart
  # modify docs/source/conf.py to be able to import ucal_client
  # modify source/*.rst to include necessary modules
  # build docs

See https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/ for details.

