Section Solver
==============

The section solver is the core of opensection, computing the internal forces
and strains for a given section under applied loads.

Section Solver
--------------

.. autoclass:: opensection.SectionSolver
   :members:
   :undoc-members:

Solver Result
-------------

.. autoclass:: opensection.SolverResult
   :members:
   :undoc-members:

How It Works
------------

The solver uses the fiber method with Newton-Raphson iteration:

1. **Fiber Discretization**: Section is divided into small fibers
2. **Strain Field**: Assume planar sections remain planar: ε(y,z) = ε₀ + χ_y·y + χ_z·z
3. **Material Laws**: Compute fiber stresses from strains
4. **Equilibrium**: Sum forces and moments from all fibers
5. **Newton-Raphson**: Iterate until equilibrium is satisfied

Usage
-----

Basic Solve
~~~~~~~~~~~

.. code-block:: python

    import opensection as ops
    
    # Setup
    section = ops.RectangularSection(width=0.3, height=0.5)
    concrete = ops.ConcreteEC2(fck=30)
    steel = ops.SteelEC2(fyk=500)
    rebars = ops.RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)
    
    # Create solver
    solver = ops.SectionSolver(section, concrete, steel, rebars)
    
    # Solve for N and M
    result = solver.solve(N=500, My=0, Mz=100)  # kN, kN·m
    
    print(f"Converged: {result.converged}")
    print(f"Iterations: {result.n_iter}")

Checking Results
~~~~~~~~~~~~~~~~

.. code-block:: python

    if result.converged:
        print(f"Axial strain: {result.epsilon_0*1000:.3f} ‰")
        print(f"Curvature: {result.chi_z:.6e} rad/m")
        print(f"Max concrete stress: {result.sigma_c_max:.2f} MPa")
        print(f"Max steel stress: {result.sigma_s_max:.2f} MPa")
        print(f"Neutral axis depth: {result.neutral_axis_depth:.3f} m")
    else:
        print(f"Did not converge ({result.reason})")
        print(f"Iterations: {result.n_iter}")

Advanced Options
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Custom tolerance and max iterations
    result = solver.solve(
        N=500, My=0, Mz=100,
        tol=1e-4,              # Force tolerance in kN
        max_iter=100,          # Maximum iterations
        use_relative_tol=False # Absolute tolerance
    )

Fiber Mesh Control
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Fine mesh (more accurate, slower)
    solver = ops.SectionSolver(
        section, concrete, steel, rebars,
        fiber_area=0.00005  # m²
    )
    
    # Coarse mesh (faster, less accurate)
    solver = ops.SectionSolver(
        section, concrete, steel, rebars,
        fiber_area=0.0005  # m²
    )

Sign Conventions
----------------

**Forces and Moments:**

* **N > 0**: Compression
* **N < 0**: Tension
* **My**: Moment around y-axis (out-of-plane)
* **Mz**: Moment around z-axis (in-plane)

**Coordinates:**

* **y**: Vertical axis (+ upward)
* **z**: Horizontal axis (+ rightward)
* Origin at section centroid

**Strains:**

* **Compression**: Positive
* **Tension**: Negative

Convergence
-----------

The solver uses Newton-Raphson with line search for robust convergence:

.. code-block:: python

    # Check convergence history
    if result.converged:
        print("Residual norms:")
        for i, res in enumerate(result.residual_norm_history):
            print(f"  Iter {i+1}: {res:.6e}")

Common Issues
~~~~~~~~~~~~~

**No Convergence:**

* Try different initial guess (adjust applied loads)
* Reduce tolerance
* Increase max iterations
* Check if section/loads are physical

**Singular Matrix:**

* Section may be unstable (too little reinforcement)
* Loading case may be extreme
* Check fiber mesh quality

Performance Tips
----------------

1. **Mesh Size**: Start with default, refine if needed
2. **Tolerance**: Use 1e-3 for most cases, 1e-4 for precision
3. **Iterations**: Usually converges in 5-10 iterations
4. **Caching**: Reuse solver for multiple load cases

API Validation
--------------

.. autofunction:: opensection.validate_and_solve

