===
w7x
===


.. image:: https://img.shields.io/pypi/v/w7x.svg
        :target: https://pypi.python.org/pypi/w7x

.. image:: https://img.shields.io/travis/dboe/w7x.svg
        :target: https://travis-ci.com/dboe/w7x

.. image:: https://readthedocs.org/projects/w7x/badge/?version=latest
        :target: https://w7x.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dboe/w7x/shield.svg
     :target: https://pyup.io/repos/github/dboe/w7x/
     :alt: Updates


Wendelstein 7-X tools providing easy acces and error-catching for Field-Line-Tracers, VMEC-Web-Service and EXTENDER and much more.


* Free software: MIT License
* Documentation: https://w7x.readthedocs.io.


Features
--------

The w7x package provides convenience methods for Magnetic Field evaluations around the stellarator Wendelstein 7-X.
The zen of the package (in addition to the zen of python) is the following:
* be intuitive
* Tell the user what he does wrong (the web services often fail without a clue for the user).
* Provide proper defaults for your functions.

The module includes handy wrapper methods for the following web-services:
* FieldLineTracing (see "http://webservices.ipp-hgw.mpg.de/docs/fieldlinetracer.html"). Namespace: w7x.flt
* VMEC (see "http://webservices.ipp-hgw.mpg.de/docs/vmec.html"). Namespace: w7x.vmec
* EXTENDER (see "http://webservices.ipp-hgw.mpg.de/docs/extender.html"). Namespace: w7x.extender

The package provides explicit classes for the osa types of the web-services provided.
The main starting point for the use of services is the Run() class e.g.
```python
import w7x
run = w7x.flt.Run()
lcfs_points = run.find_lcfs()  # returns one point on the lcfs
```
Most services are started from this class.

We utilize the tfields module in order to take care of proper coordinate transformations since some web-service tools need special coordinate systems.

Note
----

If you want to use the divertor or baffle evaluator (for example see `diffusion mapping example<https://gitlab.mpcdf.mpg.de/dboe/w7x/tree/master/examples/diffusion_mapping.py>`, i.e. build an evaluator object like so:

.. code-block:: python

    divertor_evaluator = w7x.evaluation.TracerEvaluator.from_loader(
        w7x.Defaults.Paths.divertor_upper_tiles_template_path)

the require
