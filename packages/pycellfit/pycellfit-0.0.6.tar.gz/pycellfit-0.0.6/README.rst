=========
pycellfit
=========

.. image:: https://travis-ci.com/NilaiVemula/pycellfit.svg?branch=master
  :target: https://travis-ci.com/NilaiVemula/pycellfit
.. image:: https://codecov.io/gh/NilaiVemula/pycellfit/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/NilaiVemula/pycellfit
.. image:: https://readthedocs.org/projects/pycellfit/badge/?version=latest
  :target: https://pycellfit.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
.. image:: https://badge.fury.io/py/pycellfit.svg
  :target: https://badge.fury.io/py/pycellfit

Project Description
-------------------
**pycellfit**: an open-source Python implementation of the CellFIT method of inferring cellular forces developed by Brodland et al.

**Author**: Nilai Vemula, Vanderbilt University (working under Dr. Shane Hutson, Vanderbilt University)

**Project Goal**: To develop an open-source version of CellFIT, a toolkit for inferring tensions along cell membranes and pressures inside cells based on cell geometries and their curvilinear boundaries. (See [1]_.)

**Project Timeline**: Initial project started in August 2019 with work based off of XJ Xu. This repository was re-made in May 2020 in order to restart repository structure.

**Project Status**: **Early development/Planning**

Getting Started
---------------
This project is available on  `PyPI <https://pypi.org/project/pycellfit/>`_. For now, simply clone this repository and ... ??

Making a development virtual environment (in Windows command prompt):
Assuming you are in the base directory of this repository

.. code-block:: console

   > python -m venv pycellfit_dev
   
   > pycellfit_dev\Scripts\activate
   
   > pip install -r requirements_dev.txt
   
Dependencies
^^^^^^^^^^^^
* numpy
* twine

Features
--------
This section will include a list of features available in the package and maybe a check-list of things to add

Examples
--------
This section will walk through an example of the basic pycellfit pipeline.

Future Goals
------------
The final implementation of pycellfit will be as a web-app based on the Django framework.

References
----------
.. [1] Brodland GW, Veldhuis JH, Kim S, Perrone M, Mashburn D, et al. (2014) CellFIT: A Cellular Force-Inference Toolkit Using Curvilinear Cell Boundaries. PLOS ONE 9(6): e99116. https://doi.org/10.1371/journal.pone.0099116

