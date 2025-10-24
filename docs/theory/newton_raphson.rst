Newton-Raphson Method
=====================

Iterative solution of the equilibrium equations.

Formulation
-----------

Find **d** = [ε₀, χ_y, χ_z] such that:

.. math::

    F(d) = S

where:

* F(d) = internal forces [N, M_y, M_z]
* S = external loads

Newton-Raphson Iteration
------------------------

Starting from initial guess d⁰, iterate:

.. math::

    K^{(k)} \\cdot \\Delta d^{(k)} = -(F(d^{(k)}) - S)

    d^{(k+1)} = d^{(k)} + \\alpha^{(k)} \\cdot \\Delta d^{(k)}

where:

* K = tangent stiffness matrix (3×3)
* α = line search parameter

Tangent Matrix
--------------

The tangent stiffness matrix is:

.. math::

    K_{ij} = \\frac{\\partial F_i}{\\partial d_j}

For fiber method:

.. math::

    K = \\sum_f E_t^f \\cdot A_f \\cdot \\begin{bmatrix}
        1 & y_f & z_f \\\\
        z_f & z_f y_f & z_f^2 \\\\
        y_f & y_f^2 & y_f z_f
    \\end{bmatrix}

where E_t is the tangent modulus of the fiber material.

Line Search
-----------

To ensure convergence, use backtracking line search:

1. Start with α = 1
2. If ||R(d + α·Δd)|| < ||R(d)||, accept
3. Otherwise, reduce α ← β·α (β ≈ 0.5) and retry
4. Continue until improvement or α < α_min

Convergence Criteria
--------------------

Stop when:

.. math::

    \\|F(d) - S\\| < \\text{tol}

Typical tolerance: 10⁻³ to 10⁻⁴ kN

Initial Guess
-------------

Good initial guess improves convergence:

* Use linear elastic solution
* Estimate ε₀ from axial load
* Start with zero curvatures

Robustness
----------

For difficult cases:

* Reduce tolerance
* Increase max iterations
* Use continuation method (load stepping)
* Check physical validity of inputs

