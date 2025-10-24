Utils Module
============

The ``utils`` module provides utility functions for unit conversions, mathematical helpers, and physical constants.

.. automodule:: sectionpy.utils
   :members:
   :undoc-members:
   :show-inheritance:

Unit Conversions
----------------

.. autoclass:: sectionpy.utils.UnitConverter
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.Force
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.Length
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.Stress
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.Area
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.Moment
   :members:
   :undoc-members:

Constants
---------

.. autoclass:: sectionpy.utils.MaterialConstants
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.NumericalConstants
   :members:
   :undoc-members:

.. autoclass:: sectionpy.utils.GeometricConstants
   :members:
   :undoc-members:

Mathematical Helpers
--------------------

.. autofunction:: sectionpy.utils.safe_divide

.. autofunction:: sectionpy.utils.normalize_vector

.. autofunction:: sectionpy.utils.is_converged

.. autofunction:: sectionpy.utils.clamp

.. autofunction:: sectionpy.utils.interpolate_linear

.. autofunction:: sectionpy.utils.angle_between_vectors

.. autofunction:: sectionpy.utils.sign_with_zero

.. autofunction:: sectionpy.utils.smooth_min

.. autofunction:: sectionpy.utils.smooth_max

.. autofunction:: sectionpy.utils.rotation_matrix_2d

.. autofunction:: sectionpy.utils.check_positive_definite


Unit System
-----------

sectionpy uses the following internal unit system:

* **Length**: meters (m)
* **Force**: kilonewtons (kN)
* **Stress**: megapascals (MPa)
* **Moment**: kilonewton-meters (kN·m)
* **Area**: square meters (m²)
* **Inertia**: meters to the fourth power (m⁴)

Key Conversion
~~~~~~~~~~~~~~

The most important conversion to understand in sectionpy is:

.. math::

   \\sigma (\\text{MPa}) \\times A (\\text{m}^2) = F (\\text{MN})

Since :math:`1 \\text{ MPa} = 1 \\text{ N/mm}^2` and :math:`1 \\text{ m}^2 = 10^6 \\text{ mm}^2`:

.. math::

   \\sigma (\\text{MPa}) \\times A (\\text{m}^2) = \\sigma (\\text{N/mm}^2) \\times 10^6 (\\text{mm}^2) = F \\times 10^6 (\\text{N}) = F (\\text{MN})

To convert to kilonewtons (kN), multiply by 1000:

.. math::

   F (\\text{kN}) = \\sigma (\\text{MPa}) \\times A (\\text{m}^2) \\times 1000

This is handled automatically by the :meth:`sectionpy.utils.UnitConverter.stress_area_to_force` method.

Examples
--------

Unit Conversions
~~~~~~~~~~~~~~~~

.. code-block:: python

   from sectionpy.utils import Length, Force, UnitConverter
   
   # Convert 500 mm to meters
   length_m = Length.mm_to_m(500)  # 0.5 m
   
   # Convert stress and area to force
   sigma = 10.0  # MPa
   area = 0.01   # m² (100 cm²)
   force = UnitConverter.stress_area_to_force(sigma, area)  # 100 kN

Mathematical Helpers
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from sectionpy.utils import safe_divide, clamp, is_converged
   
   # Safe division
   result = safe_divide(10, 0, default=0.0)  # Returns 0.0 instead of error
   
   # Clamp values
   value = clamp(15, min_val=0, max_val=10)  # Returns 10
   
   # Check convergence
   residual = np.array([1e-7, 1e-8])
   converged = is_converged(residual, tolerance=1e-6)  # Returns True

Constants
~~~~~~~~~

.. code-block:: python

   from sectionpy.utils import MaterialConstants, NumericalConstants
   
   # Material properties
   E_steel = MaterialConstants.E_STEEL_DEFAULT  # 200000 MPa
   gamma_c = MaterialConstants.GAMMA_C_DEFAULT  # 1.5
   
   # Numerical parameters
   tolerance = NumericalConstants.TOL_FORCE_DEFAULT  # 1e-6 kN
   max_iter = NumericalConstants.MAX_ITER_DEFAULT    # 50

