Interaction Diagrams
====================

Generating N-M interaction diagrams for sections.

Example Code
------------

See ``examples/example_interaction_diagram.py`` for complete examples including:

* Rectangular section interaction diagram
* Circular section interaction diagram
* Comparison of different reinforcement configurations

Basic Usage
-----------

.. code-block:: python

    import opensection as ops
    
    # Setup section
    section = ops.RectangularSection(width=0.3, height=0.5)
    concrete = ops.ConcreteEC2(fck=30)
    steel = ops.SteelEC2(fyk=500)
    
    # Symmetric reinforcement
    rebars = ops.RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)
    rebars.add_rebar(y=-0.20, z=0.0, diameter=0.020, n=3)
    
    # Create solver and diagram
    solver = ops.SectionSolver(section, concrete, steel, rebars)
    diagram = ops.InteractionDiagram(solver)
    
    # Generate interaction curve
    M_vals, N_vals = diagram.compute_NM_curve(n_points=20)

Plotting
--------

.. code-block:: python

    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 8))
    plt.plot(M_vals, N_vals, 'bo-', linewidth=2)
    plt.fill_between(M_vals, 0, N_vals, alpha=0.2)
    plt.xlabel('Moment M [kN·m]')
    plt.ylabel('Axial Force N [kN]')
    plt.title('Interaction Diagram N-M')
    plt.grid(True)
    plt.savefig('interaction_diagram.png')
    plt.show()

Physical Meaning
----------------

The interaction diagram shows the capacity envelope of a section:

* **Points inside** the curve are safe
* **Points on** the curve represent ultimate capacity
* **Points outside** the curve indicate failure

Key regions:

* **Top**: Pure compression
* **Bottom**: Pure tension (if applicable)
* **Maximum M**: Balanced failure
* **Intermediate**: Compression with bending or tension with bending

