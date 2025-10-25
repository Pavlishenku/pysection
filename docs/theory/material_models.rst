Material Constitutive Models
============================

Detailed description of material stress-strain relationships.

Concrete Models
---------------

EC2 Parabola-Rectangle
~~~~~~~~~~~~~~~~~~~~~~~

Used for ultimate limit state design.

**Normal Strength (f_ck ≤ 50 MPa)**

* ε_c2 = 2.0‰
* ε_cu2 = 3.5‰
* n = 2.0

**High Strength (50 < f_ck ≤ 90 MPa)**

* ε_c2 = (2.0 + 0.085·(f_ck - 50)^0.53)‰
* ε_cu2 = (2.6 + 35·((90-f_ck)/100)^4)‰
* n = 1.4 + 23.4·((90-f_ck)/100)^4

Elastic Modulus
~~~~~~~~~~~~~~~

Secant modulus (EC2 Table 3.1):

.. math::

    E_{cm} = 22000 \\cdot \\left(\\frac{f_{ck} + 8}{10}\\right)^{0.3}

Steel Models
------------

EC2 Reinforcing Steel
~~~~~~~~~~~~~~~~~~~~~~

**Without Hardening**

Perfect elasto-plastic model:

* Elastic: σ_s = E_s · ε_s for |ε| ≤ ε_yd
* Plastic: σ_s = ±f_yd for ε_yd < |ε| ≤ ε_ud

**With Hardening**

Includes strain hardening:

* Elastic: σ_s = E_s · ε_s
* Hardening: σ_s = sign(ε)·[f_yd + E_sh·(|ε| - ε_yd)]
* E_sh = k · E_s (typically k = 0.01)

Prestressing Steel
~~~~~~~~~~~~~~~~~~

Simplified model (EC2 Annex D):

.. math::

    \\sigma_p = \\frac{f_{p0.1k}}{\\varepsilon_{p0.1k}} \\cdot \\varepsilon_p \\cdot 
    \\left(1 - \\left(\\frac{\\varepsilon_p}{\\varepsilon_{pu}}\\right)^m\\right)

where m ≈ 2.0.

Structural Steel (EC3)
~~~~~~~~~~~~~~~~~~~~~~

Similar to reinforcing steel but with:

* E_a = 210 GPa
* Different safety factors (γ_M0 = 1.0)

Sign Conventions
----------------

Concrete
~~~~~~~~

* **Compression**: Positive strain and stress
* **Tension**: Negative strain, typically neglected (σ_c = 0)

This follows traditional concrete design convention.

Steel
~~~~~

* **Tension**: Positive strain and stress
* **Compression**: Negative strain and stress

This follows mechanics convention.

Numerical Implementation
------------------------

Vectorized Computation
~~~~~~~~~~~~~~~~~~~~~~

For efficiency, use NumPy vectorized operations:

.. code-block:: python

    def stress_vectorized(self, epsilon):
        sigma = np.zeros_like(epsilon)
        # Compute for all fibers simultaneously
        mask = (epsilon >= 0) & (epsilon <= self.epsilon_c2)
        sigma[mask] = self.fcd * (...)
        return sigma

Tangent Modulus
~~~~~~~~~~~~~~~

For Newton-Raphson, need tangent modulus:

.. math::

    E_t = \\frac{d\\sigma}{d\\varepsilon}

Concrete:

* Parabolic branch: E_t = (f_cd · n / ε_c2) · (1 - ε/ε_c2)^(n-1)
* Plastic branch: E_t = 0
* Post-peak: E_t = 0

Steel:

* Elastic: E_t = E_s
* Plastic (no hardening): E_t = 0
* Plastic (with hardening): E_t = k · E_s

