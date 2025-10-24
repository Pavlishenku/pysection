Quick Start Guide
=================

This guide will help you get started with opensection quickly.

Basic Section Analysis
----------------------

Here's a simple example of analyzing a rectangular concrete section:

.. code-block:: python

    import opensection as ops

    # Define geometry
    section = ops.RectangularSection(width=0.3, height=0.5)

    # Define materials (Eurocode 2)
    concrete = ops.ConcreteEC2(fck=30)  # C30/37 concrete
    steel = ops.SteelEC2(fyk=500)       # B500B reinforcement

    # Add reinforcement
    rebars = ops.RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)  # 3HA20 top
    rebars.add_rebar(y=-0.20, z=0.0, diameter=0.020, n=3) # 3HA20 bottom

    # Create solver
    solver = ops.SectionSolver(section, concrete, steel, rebars)

    # Solve for given loads
    result = solver.solve(N=500, My=0, Mz=100)  # N in kN, M in kN·m

    # Check results
    print(f"Converged: {result.converged}")
    print(f"Max concrete stress: {result.sigma_c_max:.2f} MPa")
    print(f"Max steel stress: {result.sigma_s_max:.2f} MPa")

Understanding the Results
-------------------------

The solver returns a ``SolverResult`` object with:

* ``converged``: Boolean indicating if solution converged
* ``epsilon_0``: Axial strain at centroid
* ``chi_y``, ``chi_z``: Curvatures
* ``N``, ``My``, ``Mz``: Internal forces and moments
* ``sigma_c_max``: Maximum concrete stress
* ``sigma_s_max``: Maximum steel stress
* ``n_iter``: Number of iterations

Verification
------------

Use EC2 verification tools:

.. code-block:: python

    checks = ops.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
    
    print(f"Concrete OK: {checks['concrete_stress']['ok']}")
    print(f"Steel OK: {checks['steel_stress']['ok']}")

Creating Sections
-----------------

Rectangular Section
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    section = ops.RectangularSection(width=0.3, height=0.5)

Circular Section
~~~~~~~~~~~~~~~~

.. code-block:: python

    section = ops.CircularSection(diameter=0.5)

T-Section
~~~~~~~~~

.. code-block:: python

    section = ops.TSection(
        web_width=0.3,
        web_height=0.6,
        flange_width=0.8,
        flange_height=0.15
    )

Materials
---------

Concrete EC2
~~~~~~~~~~~~

.. code-block:: python

    # Standard concrete
    concrete = ops.ConcreteEC2(fck=30)  # C30/37
    
    # High-strength concrete
    concrete = ops.ConcreteEC2(fck=60)  # C60/75
    
    # Custom safety factors
    concrete = ops.ConcreteEC2(fck=30, gamma_c=1.5, alpha_cc=0.85)

Steel EC2
~~~~~~~~~

.. code-block:: python

    # Standard reinforcement
    steel = ops.SteelEC2(fyk=500)  # B500B
    
    # With strain hardening
    steel = ops.SteelEC2(fyk=500, include_hardening=True, k=0.01)

Reinforcement
-------------

Single Bars
~~~~~~~~~~~

.. code-block:: python

    rebars = ops.RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)

Linear Array
~~~~~~~~~~~~

.. code-block:: python

    rebars.add_linear_array(
        y1=0.20, z1=-0.10,
        y2=0.20, z2=0.10,
        n=5, diameter=0.016
    )

Circular Array
~~~~~~~~~~~~~~

.. code-block:: python

    rebars.add_circular_array(
        center_y=0.0, center_z=0.0,
        radius=0.20,
        n=8, diameter=0.020
    )

Visualization
-------------

Plot Section
~~~~~~~~~~~~

.. code-block:: python

    plotter = ops.SectionPlotter(section, rebars)
    plotter.plot()
    plotter.save("section.png")

Generate Report
~~~~~~~~~~~~~~~

.. code-block:: python

    report = ops.ReportGenerator()
    report.add_section_info(section, concrete, steel, rebars)
    report.add_results(result)
    print(report.generate())

Next Steps
----------

* See :doc:`/examples/basic_section` for complete examples
* Read :doc:`/api/solver` for detailed API reference
* Learn about :doc:`/theory/fiber_method` for theoretical background

