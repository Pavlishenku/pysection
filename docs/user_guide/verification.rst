Verification
============

opensection provides tools to verify designs according to Eurocode 2.

EC2 Verification
----------------

.. autoclass:: opensection.EC2Verification
   :members:
   :undoc-members:

Ultimate Limit State (ULS)
--------------------------

Check ULS
~~~~~~~~~

.. code-block:: python

    import opensection as oc
    
    # After solving
    result = solver.solve(N=500, My=0, Mz=100)
    
    # Verify ULS
    checks = oc.EC2Verification.check_ULS(
        result,
        fcd=concrete.fcd,
        fyd=steel.fyd
    )
    
    # Check results
    if checks['concrete_stress']['ok']:
        print("✓ Concrete stress OK")
    else:
        print(f"✗ Concrete overstressed: {checks['concrete_stress']['ratio']:.1%}")
    
    if checks['steel_stress']['ok']:
        print("✓ Steel stress OK")
    else:
        print(f"✗ Steel overstressed: {checks['steel_stress']['ratio']:.1%}")

Verification Criteria
~~~~~~~~~~~~~~~~~~~~~

**Concrete Stress:**

σ_c,max ≤ f_cd

**Steel Stress:**

σ_s,max ≤ f_yd

**Strain Limits:**

* Concrete: ε_c ≤ ε_cu2 (typically 3.5‰)
* Steel: ε_s ≤ ε_ud (typically 45‰)

Serviceability Limit State (SLS)
---------------------------------

Check SLS
~~~~~~~~~

.. code-block:: python

    # SLS checks (if implemented)
    sls_checks = oc.EC2Verification.check_SLS(
        result,
        fck=concrete.fck,
        max_crack_width=0.0003  # 0.3 mm
    )

Typical SLS criteria:

* Concrete stress < 0.6·fck
* Crack width < w_max (depends on exposure class)
* Deflection < L/250 (for beams)

Reinforcement Ratio
-------------------

Check minimum and maximum reinforcement:

.. code-block:: python

    # Check reinforcement ratio
    As_total = rebars.total_area
    Ac = section.properties.area
    
    rho = As_total / Ac
    
    # EC2 limits
    rho_min = 0.26 * (concrete.fck ** 0.5) / steel.fyk
    rho_max = 0.04
    
    if rho < rho_min:
        print(f"Warning: ρ = {rho:.4f} < ρ_min = {rho_min:.4f}")
    elif rho > rho_max:
        print(f"Warning: ρ = {rho:.4f} > ρ_max = {rho_max:.4f}")
    else:
        print(f"✓ Reinforcement ratio OK: ρ = {rho:.4f}")

Cover Requirements
------------------

Minimum cover for durability and fire resistance:

.. code-block:: python

    # Exposure class requirements (EC2 Table 4.1)
    exposure_classes = {
        'XC1': 15,  # mm - dry or permanently wet
        'XC2': 25,  # mm - wet, rarely dry
        'XC3': 25,  # mm - moderate humidity
        'XC4': 30,  # mm - cyclic wet and dry
    }
    
    c_min = exposure_classes['XC3']
    c_nom = c_min + 10  # Execution tolerance
    
    print(f"Minimum cover: {c_min} mm")
    print(f"Nominal cover: {c_nom} mm")

Complete Verification Example
------------------------------

.. code-block:: python

    import opensection as oc
    
    # Define section
    section = oc.RectangularSection(width=0.3, height=0.5)
    concrete = oc.ConcreteEC2(fck=30)
    steel = oc.SteelEC2(fyk=500)
    
    # Add reinforcement
    rebars = oc.RebarGroup()
    rebars.add_rebar(y=0.21, z=0.0, diameter=0.020, n=3)
    rebars.add_rebar(y=-0.21, z=0.0, diameter=0.020, n=3)
    
    # Solve
    solver = oc.SectionSolver(section, concrete, steel, rebars)
    result = solver.solve(N=500, My=0, Mz=100)
    
    # Comprehensive verification
    print("=" * 60)
    print("VERIFICATION REPORT")
    print("=" * 60)
    
    # 1. Convergence
    print(f"\n1. Analysis:")
    print(f"   Converged: {'YES' if result.converged else 'NO'}")
    print(f"   Iterations: {result.n_iter}")
    
    # 2. ULS stress checks
    print(f"\n2. ULS Stress Verification:")
    checks = oc.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
    
    print(f"   Concrete: σ_c,max = {result.sigma_c_max:.2f} MPa")
    print(f"             f_cd = {concrete.fcd:.2f} MPa")
    print(f"             Ratio = {checks['concrete_stress']['ratio']:.1%}")
    print(f"             Status: {'OK' if checks['concrete_stress']['ok'] else 'FAIL'}")
    
    print(f"   Steel: σ_s,max = {result.sigma_s_max:.2f} MPa")
    print(f"          f_yd = {steel.fyd:.2f} MPa")
    print(f"          Ratio = {checks['steel_stress']['ratio']:.1%}")
    print(f"          Status: {'OK' if checks['steel_stress']['ok'] else 'FAIL'}")
    
    # 3. Reinforcement ratio
    print(f"\n3. Reinforcement Ratio:")
    As = rebars.total_area
    Ac = section.properties.area
    rho = As / Ac
    rho_min = 0.26 * (concrete.fck ** 0.5) / steel.fyk
    
    print(f"   As = {As*1e4:.2f} cm²")
    print(f"   Ac = {Ac*1e4:.2f} cm²")
    print(f"   ρ = {rho*100:.2f}%")
    print(f"   ρ_min = {rho_min*100:.2f}%")
    print(f"   Status: {'OK' if rho >= rho_min else 'FAIL'}")
    
    # 4. Overall verdict
    print(f"\n4. Overall Verdict:")
    all_ok = (result.converged and 
              checks['concrete_stress']['ok'] and
              checks['steel_stress']['ok'] and
              rho >= rho_min)
    
    if all_ok:
        print("   ✓ DESIGN VERIFIED - ALL CHECKS PASSED")
    else:
        print("   ✗ DESIGN FAILS - SEE DETAILS ABOVE")
    
    print("=" * 60)

