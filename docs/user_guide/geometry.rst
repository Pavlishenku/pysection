Geometry
========

opensection supports various section geometries for concrete design.

Section Types
-------------

Rectangular Section
~~~~~~~~~~~~~~~~~~~

.. autoclass:: opensection.RectangularSection
   :members:
   :undoc-members:

Circular Section
~~~~~~~~~~~~~~~~

.. autoclass:: opensection.CircularSection
   :members:
   :undoc-members:

T-Section
~~~~~~~~~

.. autoclass:: opensection.TSection
   :members:
   :undoc-members:

Custom Sections
~~~~~~~~~~~~~~~

.. autoclass:: opensection.Section
   :members:
   :undoc-members:

Geometric Properties
--------------------

.. autoclass:: opensection.GeometricProperties
   :members:
   :undoc-members:

Contours
--------

.. autoclass:: opensection.Contour
   :members:
   :undoc-members:

.. autoclass:: opensection.Point
   :members:
   :undoc-members:

Examples
--------

Creating a Rectangular Section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import opensection as oc

    section = oc.RectangularSection(width=0.3, height=0.5)
    props = section.properties
    
    print(f"Area: {props.area:.4f} m²")
    print(f"Centroid: {props.centroid}")
    print(f"Inertia Iy: {props.Iy:.6f} m⁴")
    print(f"Inertia Iz: {props.Iz:.6f} m⁴")

Creating a Circular Section
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    section = oc.CircularSection(diameter=0.5)
    props = section.properties
    
    print(f"Area: {props.area:.4f} m²")

Creating a Custom Section
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from opensection import Section, Contour, Point
    
    # Define vertices of polygon
    points = [
        Point(0, 0),
        Point(0.3, 0),
        Point(0.3, 0.5),
        Point(0, 0.5)
    ]
    
    contour = Contour(points)
    section = Section(contour)

Fiber Discretization
--------------------

Sections are discretized into fibers for analysis:

.. code-block:: python

    # Create fiber mesh
    fibers = section.create_fiber_mesh(fiber_area=0.0001)
    
    # Each fiber has: [y, z, area]
    print(f"Number of fibers: {len(fibers)}")

The fiber area parameter controls the discretization fineness. Smaller values
give more accurate results but slower computation.

