Basic Section Analysis
======================

This example demonstrates basic section analysis with sectionpy.

Simple Rectangular Section
---------------------------

.. literalinclude:: ../../examples/example_basic.py
   :language: python
   :lines: 1-64

Output
~~~~~~

When you run this example, you should see::

    sectionpy - Exemple de calcul de section
    ============================================================
    
    Section: 0.3m x 0.5m
    Béton: C30/37 (fcd = 17.00 MPa)
    Acier: B500B (fyd = 434.78 MPa)
    
    Armatures: 5 barres, As = 13.45 cm²
    Fibres béton: 1421
    
    Sollicitations: N = 500 kN, M = 100 kN·m
    
    Résolution...
    
    RÉSULTATS:
      Convergence: OUI
      Itérations: 6
      e0 = -0.064 ‰
      χ_z = -1.042039e-04 rad/m
      s_c,max = 10.78 MPa
      s_s,max = 233.90 MPa
      Profondeur AN = 0.012 m
    
    VÉRIFICATIONS ELU:
      Béton: 63.41% - OK
      Acier: 53.80% - OK

Explanation
-----------

This example shows:

1. **Section Definition**: Creating a 30cm × 50cm rectangular section
2. **Materials**: Using EC2 concrete (C30/37) and steel (B500B)
3. **Reinforcement**: Adding rebars with automatic discretization
4. **Analysis**: Solving for given axial force and bending moment
5. **Verification**: Checking EC2 ULS criteria

Key Points
----------

* The solver uses fiber method with Newton-Raphson iteration
* Convergence is typically achieved in 5-10 iterations
* Results include internal forces, stresses, and strains
* EC2 verification checks stress limits automatically

