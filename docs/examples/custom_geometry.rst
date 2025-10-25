Custom Geometry
===============

Creating custom section geometries.

See ``examples/example_custom_sections.py`` for detailed examples.

Polygon Sections
----------------

.. code-block:: python

    from opensection import Section, Contour, Point
    
    # Define vertices
    points = [
        Point(0, 0),
        Point(0.4, 0),
        Point(0.4, 0.2),
        Point(0.3, 0.2),
        Point(0.3, 0.6),
        Point(0, 0.6)
    ]
    
    # Create contour and section
    contour = Contour(points)
    section = Section(contour)
    
    # Get properties
    props = section.properties
    print(f"Area: {props.area:.4f} m²")
    print(f"Centroid: {props.centroid}")

Hexagonal Section
-----------------

.. code-block:: python

    import numpy as np
    
    # Generate hexagon vertices
    n_sides = 6
    radius = 0.3
    angles = np.linspace(0, 2*np.pi, n_sides+1)[:-1]
    
    points = [
        Point(radius * np.cos(a), radius * np.sin(a))
        for a in angles
    ]
    
    contour = Contour(points)
    section = Section(contour)

Complex Shapes
--------------

For more complex shapes, you can:

1. Define the outer boundary
2. Define internal voids (holes)
3. Combine multiple contours

.. code-block:: python

    # Hollow section
    outer_points = [...]  # Outer boundary
    inner_points = [...]  # Inner void
    
    outer_contour = Contour(outer_points)
    inner_contour = Contour(inner_points, is_hole=True)
    
    section = Section(outer_contour, holes=[inner_contour])

