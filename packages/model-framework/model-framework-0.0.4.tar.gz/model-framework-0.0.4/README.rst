.. image:: https://img.shields.io/pypi/v/model-framework.svg?style=flat
   :target: https://pypi.org/project/model-framework/
   :alt: Latest PyPI version

.. image:: https://readthedocs.org/projects/mframework/badge/?version=latest
    :target: https://mframework.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
    :target: https://github.com/airinnova/model-framework/blob/master/LICENSE.txt
    :alt: License

.. image:: https://travis-ci.org/airinnova/model-framework.svg?branch=master
    :target: https://travis-ci.org/airinnova/model-framework
    :alt: Build status

.. image:: https://codecov.io/gh/airinnova/model-framework/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/airinnova/model-framework
    :alt: Coverage

|

.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/docs/source/_static/images/logo.png
   :target: https://github.com/airinnova/model-framework/
   :alt: logo

⚠ **Work in progress!** This project is in an early prototyping phase.

Vision
======

This *Python* package provides two classes (``FeatureSpec()`` and ``ModelSpec()``) to build simple, understandable and consistent user interfaces for (physics) models. A *model* is made up of *features*, and each feature is made up of *properties*. The *developer* defines the *model* using specifications of model *features* and feature *properties* (user input).

The end-user of the final model object can only interact with safe "setter" and "getter" methods of the specified model object. Due to the small number of simple methods which follow a clear "key-value paradigm" the model API is very easy to learn and to document. As a model developer, you can easily enforce user-input checks to avoid invalid data. Expected input is defined in a simple schema format, and user-input checks are performed when data entered by the user.

Basic system
------------

* Provide specification classes that enable to easily define a complex (physics) models (e.g. a beam structure)
* A *model* is made up of one or more *features* (singleton/non-singleton)

    * A model has user methods ``add_feature``, ``set_feature`` and ``get``/``iter``

* Each feature has one or more *properties* (singleton/non-singleton)

    * A feature has user methods ``set``/``add`` and ``get``/``iter`` methods to interact with properties

Additional features
-------------------

* Built-in validation of user data using *schemadicts*
* Serialization of the entire model to disk (e.g. JSON) and deserialization
* Auto-generation of user-documentation for the model interface
* Model generation based on default values provided in the specifications in case of missing user input (!?)
* Abstract method ``run()`` to run the entire model
* Attach immediate actions to model definitions (?)

Basic usage
===========

Developer code
--------------

The model developer provides the specification of the model. Two classes are available:

    * Class ``FeatureSpec()`` defines a feature with its properties.
    * Class ``ModelSpec()`` defines a model with its features.

.. code:: python

    fspec_global = FeatureSpec()
    fspec_global.add_prop_spec('name', str)
    fspec_global.add_prop_spec('mass', float)
    fspec_global.add_prop_spec('pax', int)

    fspec_wing = FeatureSpec()
    fspec_wing.add_prop_spec('span', float)
    fspec_wing.add_prop_spec('area', {'type': float, '>': 0})

    mspec_aircraft = ModelSpec()
    mspec_aircraft.add_feature_spec('global', fspec_global, singleton=True)
    mspec_aircraft.add_feature_spec('wing', fspec_wing, singleton=False)

    Aircraft = mspec_aircraft.getUserModel()

User code
---------

The end-user builds the model with actual values. Errors are thrown if invalid data is provided.

.. code:: python

    from somewhere import Aircraft

    ac = Aircraft()

    glob_info = ac.add_feature('global')
    glob_info.set('name', 'BoxWing')
    glob_info.set('mass', 10e3)
    glob_info.set('pax', 20)

    main_wing = ac.add_feature('wing')
    main_wing.set('span', 20)
    main_wing.set('area', 40)

    horiz_tail = ac.add_feature('wing')
    horiz_tail.set('span', 6)
    horiz_tail.set('area', 12)

    ac.run()

* A *model* has the following user methods

    * ``set_feature()`` (for singleton features)
    * ``add_feature()`` (for non-singleton features)
    * ``get()``
    * ``iter()`` (for non-singleton features)

* A *feature* has the following user methods

    * ``set()`` (for singleton features)
    * ``add()`` (for non-singleton features)
    * ``get()``
    * ``iter()`` (for non-singleton features)

Installation
============

*Model-Framework* is available on `PyPI <https://pypi.org/project/model-framework/>`_ and may simply be installed with

.. code::

    pip install model-framework

License
=======

**License:** Apache-2.0
