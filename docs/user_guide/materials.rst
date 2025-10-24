Materials
=========

opensection implements material constitutive laws according to Eurocodes.

Concrete
--------

Concrete EC2
~~~~~~~~~~~~

.. autoclass:: opensection.ConcreteEC2
   :members:
   :undoc-members:

The concrete model follows EN 1992-1-1 (Eurocode 2) with a parabola-rectangle diagram.

**Stress-strain relationship:**

For ``0 ≤ ε ≤ ε_c2`` (parabolic branch)::

    σ_c = f_cd [1 - (1 - ε/ε_c2)^n]

For ``ε_c2 < ε ≤ ε_cu2`` (plastic branch)::

    σ_c = f_cd

For ``ε > ε_cu2`` (failure)::

    σ_c = 0

where:

* ``f_cd`` = design compressive strength
* ``ε_c2`` = strain at peak stress
* ``ε_cu2`` = ultimate strain
* ``n`` = exponent (2.0 for normal strength, varies for high strength)

Steel
-----

Reinforcing Steel EC2
~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: opensection.SteelEC2
   :members:
   :undoc-members:

Bilinear model with optional strain hardening.

**Stress-strain relationship:**

For ``|ε| ≤ ε_yd`` (elastic)::

    σ_s = E_s · ε

For ``ε_yd < |ε| ≤ ε_ud`` (plastic without hardening)::

    σ_s = sign(ε) · f_yd

For ``ε_yd < |ε| ≤ ε_ud`` (plastic with hardening)::

    σ_s = sign(ε) · [f_yd + E_sh · (|ε| - ε_yd)]

where ``E_sh = k · E_s`` is the hardening modulus.

Prestressing Steel EC2
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: opensection.PrestressingSteelEC2
   :members:
   :undoc-members:

Structural Steel EC3
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: opensection.StructuralSteelEC3
   :members:
   :undoc-members:

Examples
--------

Concrete Classes
~~~~~~~~~~~~~~~~

.. code-block:: python

    import opensection as oc
    
    # Standard concrete classes
    c20 = oc.ConcreteEC2(fck=20)  # C20/25
    c30 = oc.ConcreteEC2(fck=30)  # C30/37
    c40 = oc.ConcreteEC2(fck=40)  # C40/50
    
    # High-strength concrete
    c60 = oc.ConcreteEC2(fck=60)  # C60/75
    c80 = oc.ConcreteEC2(fck=80)  # C80/95
    
    print(f"C30/37: fcd = {c30.fcd:.2f} MPa")
    print(f"C30/37: Ecm = {c30.Ecm:.0f} MPa")

Custom Safety Factors
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Custom partial safety factor
    concrete = oc.ConcreteEC2(fck=30, gamma_c=1.2)
    
    # Custom long-term effects coefficient
    concrete = oc.ConcreteEC2(fck=30, alpha_cc=1.0)

Steel Grades
~~~~~~~~~~~~

.. code-block:: python

    # Common grades
    b400 = oc.SteelEC2(fyk=400)  # B400
    b500 = oc.SteelEC2(fyk=500)  # B500
    
    # With strain hardening
    steel = oc.SteelEC2(fyk=500, include_hardening=True, k=0.01)
    
    print(f"B500: fyd = {b500.fyd:.2f} MPa")
    print(f"B500: Es = {b500.Es:.0f} MPa")

Stress-Strain Curves
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    
    concrete = oc.ConcreteEC2(fck=30)
    
    # Generate strain range
    epsilon = np.linspace(0, 0.004, 100)
    
    # Compute stresses
    sigma = concrete.stress_vectorized(epsilon)
    
    # Plot
    plt.plot(epsilon * 1000, sigma)
    plt.xlabel('Strain [‰]')
    plt.ylabel('Stress [MPa]')
    plt.title('Concrete Stress-Strain Curve')
    plt.grid(True)
    plt.show()

Material Properties
-------------------

Concrete Properties
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    concrete = oc.ConcreteEC2(fck=30)
    
    print(f"fck = {concrete.fck} MPa")
    print(f"fcd = {concrete.fcd:.2f} MPa")
    print(f"Ecm = {concrete.Ecm:.0f} MPa")
    print(f"ε_c2 = {concrete.epsilon_c2*1000:.2f} ‰")
    print(f"ε_cu2 = {concrete.epsilon_cu2*1000:.2f} ‰")

Steel Properties
~~~~~~~~~~~~~~~~

.. code-block:: python

    steel = oc.SteelEC2(fyk=500)
    
    print(f"fyk = {steel.fyk} MPa")
    print(f"fyd = {steel.fyd:.2f} MPa")
    print(f"Es = {steel.Es:.0f} MPa")
    print(f"ε_yd = {steel.epsilon_yk*1000:.2f} ‰")
    print(f"ε_ud = {steel.epsilon_ud*1000:.1f} ‰")

