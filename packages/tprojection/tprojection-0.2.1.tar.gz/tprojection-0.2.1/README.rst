
tprojection
===========


.. raw:: html

   <div class="row">

   <img src="examples/survived_cabin.png" height="250" width="385">
   <img src="examples/fare_cabin.png" height="250" width="385">
   <img src="examples/survived_fare.png" height="250" width="385">
   <img src="examples/fare_age.png" height="250" width="385">

   <div class="row">
   </div>


[![pypi] (https://img.shields.io/pypi/v/tprojection.svg)] (https://pypi.python.org/pypi/tprojection)

.. image:: https://travis-ci.org/mwaskom/seaborn.svg?branch=master
   :target: https://travis-ci.org/mwaskom/seaborn
   :alt: Build Status


.. image:: https://img.shields.io/codecov/c/github/greghor/tprojection
   :target: https://img.shields.io/codecov/c/github/greghor/tprojection
   :alt: Code cov


This library allows you to visually inspect the relation between a dependent variable (the target) and a predictor in a meaningful way. This library is particularly convenient when it is difficult to compute a traditionnal correlation coefficient, for instance when the target and the predictor are categorical.
And by the way, Tprojection stands for target projection.

Installation
------------

.. code-block::

   pip install tprojection


Basic usage
-----------

.. code-block::

    from tprojection import Tprojection

    tproj = Tprojection(df, "target", "predictor")
    tproj.plot()


Advanced usage
--------------

You can find several examples depicting more advanced functionalities in ``examples/examples.ipynb``

Credits
-------

This package was created with `Cookiecutter <https://github.com/audreyr/cookiecutter>`_ and the `cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`_ project template.
