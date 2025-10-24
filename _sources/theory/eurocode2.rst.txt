Eurocode 2 Theory
=================

Implementation of EN 1992-1-1 (Eurocode 2) for concrete structures.

Material Models
---------------

Concrete (EC2 § 3.1.7)
~~~~~~~~~~~~~~~~~~~~~~

Parabola-rectangle diagram:

.. math::

    \\sigma_c = f_{cd} \\left[1 - \\left(1 - \\frac{\\varepsilon_c}{\\varepsilon_{c2}}\\right)^n\\right]
    \\quad \\text{for } 0 \\leq \\varepsilon_c \\leq \\varepsilon_{c2}

    \\sigma_c = f_{cd}
    \\quad \\text{for } \\varepsilon_{c2} < \\varepsilon_c \\leq \\varepsilon_{cu2}

Parameters:

* f_cd = α_cc · f_ck / γ_c (design strength)
* ε_c2 = 2.0‰ (normal strength), varies for high strength
* ε_cu2 = 3.5‰ (normal strength)
* n = 2.0 (normal strength), varies for high strength

Steel (EC2 § 3.2.7)
~~~~~~~~~~~~~~~~~~~

Bilinear with optional hardening:

.. math::

    \\sigma_s = E_s \\cdot \\varepsilon_s
    \\quad \\text{for } |\\varepsilon_s| \\leq \\varepsilon_{yd}

    \\sigma_s = \\text{sign}(\\varepsilon_s) \\cdot f_{yd}
    \\quad \\text{for } \\varepsilon_{yd} < |\\varepsilon_s| \\leq \\varepsilon_{ud}

Parameters:

* f_yd = f_yk / γ_s (design yield strength)
* E_s = 200 GPa (elastic modulus)
* ε_ud ≈ 45‰ (ultimate strain)

Ultimate Limit State
--------------------

Verification (EC2 § 6.1)
~~~~~~~~~~~~~~~~~~~~~~~~

At ULS, check:

1. **Concrete stress**: σ_c ≤ f_cd
2. **Steel stress**: σ_s ≤ f_yd
3. **Concrete strain**: ε_c ≤ ε_cu2
4. **Steel strain**: ε_s ≤ ε_ud

Reinforcement Limits (EC2 § 9.2.1.1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Minimum reinforcement:

.. math::

    A_{s,min} = 0.26 \\frac{f_{ctm}}{f_{yk}} \\cdot b_t \\cdot d \\geq 0.0013 \\cdot b_t \\cdot d

Maximum reinforcement:

.. math::

    A_{s,max} = 0.04 \\cdot A_c

Serviceability Limit State
---------------------------

Stress Limitations (EC2 § 7.2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Concrete: σ_c ≤ 0.6 · f_ck (avoid nonlinear creep)
* Steel: σ_s ≤ 0.8 · f_yk (crack width control)

Crack Width (EC2 § 7.3)
~~~~~~~~~~~~~~~~~~~~~~~~

Maximum crack width depends on exposure class:

* XC1: w_max = 0.4 mm
* XC2-XC4: w_max = 0.3 mm
* XD1-XD3, XS1-XS3: w_max = 0.3 mm

Deflection (EC2 § 7.4)
~~~~~~~~~~~~~~~~~~~~~~

Limiting span/effective depth ratios to control deflection.

Safety Factors
--------------

Partial Safety Factors (EC2 § 2.4.2.4)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Concrete: γ_c = 1.5 (persistent and transient)
* Steel: γ_s = 1.15
* Structural steel: γ_M0 = 1.0

Long-term Effects (EC2 § 3.1.6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* α_cc = 0.85 (coefficient for long-term effects)

Cover Requirements
------------------

Nominal Cover (EC2 § 4.4.1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

    c_{nom} = c_{min} + \\Delta c_{dev}

where:

* c_min = minimum cover (durability + bond)
* Δc_dev = allowance for deviations (typically 10 mm)

Minimum cover depends on exposure class and structural class.

