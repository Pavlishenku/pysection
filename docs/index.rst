sectionpy Documentation
=====================

.. image:: https://img.shields.io/pypi/v/sectionpy.svg
   :target: https://pypi.org/project/sectionpy/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/sectionpy.svg
   :target: https://pypi.org/project/sectionpy/
   :alt: Python versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

Welcome to sectionpy (Professional Concrete Section Analysis), a Python package for structural 
concrete design according to Eurocodes.

**sectionpy** provides tools for:

* Section analysis using fiber discretization
* Material constitutive laws (EC2, EC3)
* Interaction diagram generation
* Eurocode-compliant verification
* Visualization and reporting

Quick Start
-----------

Installation::

    pip install sectionpy

Basic usage:

.. code-block:: python

    import sectionpy as oc

    # Define section and materials
    section = oc.RectangularSection(width=0.3, height=0.5)
    concrete = oc.ConcreteEC2(fck=30)
    steel = oc.SteelEC2(fyk=500)

    # Add reinforcement
    rebars = oc.RebarGroup()
    rebars.add_rebar(y=0.0, z=-0.20, diameter=0.020, n=3)

    # Analyze
    solver = oc.SectionSolver(section, concrete, steel, rebars)
    result = solver.solve(N=500, My=0, Mz=100)

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user_guide/installation
   user_guide/quickstart
   user_guide/geometry
   user_guide/materials
   user_guide/solver
   user_guide/verification

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/basic_section
   examples/interaction_diagram
   examples/custom_geometry
   examples/biaxial_bending

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/geometry
   api/materials
   api/reinforcement
   api/solver
   api/eurocodes
   api/interaction
   api/postprocess
   utils

.. toctree::
   :maxdepth: 2
   :caption: Theory

   theory/fiber_method
   theory/newton_raphson
   theory/eurocode2
   theory/material_models

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

