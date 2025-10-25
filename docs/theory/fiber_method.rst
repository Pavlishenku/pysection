Fiber Method
============

Theoretical background of the fiber discretization method.

Principle
---------

The fiber method discretizes a cross-section into small fibers, each with:

* Position (y, z)
* Area A_i
* Material properties

Section Analysis
----------------

Strain Field
~~~~~~~~~~~~

Assuming plane sections remain plane (Bernoulli-Navier hypothesis):

.. math::

    \\varepsilon(y, z) = \\varepsilon_0 + \\chi_y \\cdot y + \\chi_z \\cdot z

where:

* ε₀ = axial strain at centroid
* χ_y, χ_z = curvatures around y and z axes

Fiber Stresses
~~~~~~~~~~~~~~

For each fiber i:

.. math::

    \\sigma_i = f(\\varepsilon_i)

where f is the material constitutive law (concrete or steel).

Internal Forces
~~~~~~~~~~~~~~~

Summing over all fibers:

.. math::

    N = \\sum_i \\sigma_i \\cdot A_i

    M_y = \\sum_i \\sigma_i \\cdot A_i \\cdot z_i

    M_z = \\sum_i \\sigma_i \\cdot A_i \\cdot y_i

Equilibrium
-----------

For given external loads (N_ext, M_y,ext, M_z,ext), find (ε₀, χ_y, χ_z) such that:

.. math::

    N - N_{ext} = 0

    M_y - M_{y,ext} = 0

    M_z - M_{z,ext} = 0

This system of 3 nonlinear equations is solved using Newton-Raphson.

Advantages
----------

* **Accurate** for nonlinear materials
* **General** - works for any section shape
* **Efficient** - linear in number of fibers
* **Robust** - well-conditioned problem

Discretization
--------------

Fiber Size
~~~~~~~~~~

Typical fiber areas: 10⁻⁴ to 10⁻³ m²

Smaller fibers → more accurate but slower

Mesh Quality
~~~~~~~~~~~~

* Regular grid for rectangular sections
* Adaptive refinement near boundaries
* Finer mesh near reinforcement

