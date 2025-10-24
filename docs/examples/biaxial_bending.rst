Biaxial Bending
===============

Analysis under combined axial force and biaxial bending moments.

See ``examples/example_biaxial_bending.py`` for complete code.

Basic Example
-------------

.. code-block:: python

    import sectionpy as oc
    
    # Square column
    section = oc.RectangularSection(width=0.4, height=0.4)
    concrete = oc.ConcreteEC2(fck=30)
    steel = oc.SteelEC2(fyk=500)
    
    # Corner reinforcement
    rebars = oc.RebarGroup()
    rebars.add_rebar(y=0.15, z=0.15, diameter=0.025, n=1)
    rebars.add_rebar(y=0.15, z=-0.15, diameter=0.025, n=1)
    rebars.add_rebar(y=-0.15, z=0.15, diameter=0.025, n=1)
    rebars.add_rebar(y=-0.15, z=-0.15, diameter=0.025, n=1)
    
    # Solve for biaxial moment
    solver = oc.SectionSolver(section, concrete, steel, rebars)
    result = solver.solve(N=1000, My=50, Mz=75)  # kN, kN·m
    
    print(f"Converged: {result.converged}")
    print(f"Max stress concrete: {result.sigma_c_max:.2f} MPa")

Biaxial Interaction Surface
----------------------------

For complete capacity assessment, generate 3D interaction surface:

.. code-block:: python

    import numpy as np
    
    # Grid of moments
    My_vals = np.linspace(-200, 200, 15)
    Mz_vals = np.linspace(-200, 200, 15)
    
    # For each axial force level
    for N in [0, 500, 1000, 1500, 2000]:
        surface_points = []
        
        for My in My_vals:
            for Mz in Mz_vals:
                try:
                    result = solver.solve(N=N, My=My, Mz=Mz)
                    if result.converged:
                        surface_points.append((My, Mz, N))
                except:
                    pass
        
        # Plot surface for this N level

Applications
------------

Biaxial bending occurs in:

* **Columns** under eccentric loads
* **Corner columns** in buildings
* **Bridge piers** under seismic loads
* **Wind turbine towers**

