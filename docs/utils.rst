Utils Module
============

The ``utils`` module provides utility functions for unit conversions, mathematical helpers, and physical constants.

.. automodule:: opensection.utils
   :members:
   :undoc-members:
   :show-inheritance:

Unit Conversions
----------------

.. autoclass:: opensection.utils.UnitConverter
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.Force
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.Length
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.Stress
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.Area
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.Moment
   :members:
   :undoc-members:

Constants
---------

.. autoclass:: opensection.utils.MaterialConstants
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.NumericalConstants
   :members:
   :undoc-members:

.. autoclass:: opensection.utils.GeometricConstants
   :members:
   :undoc-members:

Mathematical Helpers
--------------------

.. autofunction:: opensection.utils.safe_divide

.. autofunction:: opensection.utils.normalize_vector

.. autofunction:: opensection.utils.is_converged

.. autofunction:: opensection.utils.clamp

.. autofunction:: opensection.utils.interpolate_linear

.. autofunction:: opensection.utils.angle_between_vectors

.. autofunction:: opensection.utils.sign_with_zero

.. autofunction:: opensection.utils.smooth_min

.. autofunction:: opensection.utils.smooth_max

.. autofunction:: opensection.utils.rotation_matrix_2d

.. autofunction:: opensection.utils.check_positive_definite


Unit System
-----------

opensection uses the following internal unit system:

* **Length**: meters (m)
* **Force**: kilonewtons (kN)
* **Stress**: megapascals (MPa)
* **Moment**: kilonewton-meters (kN·m)
* **Area**: square meters (m²)
* **Inertia**: meters to the fourth power (m⁴)

Key Conversion
~~~~~~~~~~~~~~

The most important conversion to understand in opensection is:

.. math::

   \\sigma (\\text{MPa}) \\times A (\\text{m}^2) = F (\\text{MN})

Since :math:`1 \\text{ MPa} = 1 \\text{ N/mm}^2` and :math:`1 \\text{ m}^2 = 10^6 \\text{ mm}^2`:

.. math::

   \\sigma (\\text{MPa}) \\times A (\\text{m}^2) = \\sigma (\\text{N/mm}^2) \\times 10^6 (\\text{mm}^2) = F \\times 10^6 (\\text{N}) = F (\\text{MN})

To convert to kilonewtons (kN), multiply by 1000:

.. math::

   F (\\text{kN}) = \\sigma (\\text{MPa}) \\times A (\\text{m}^2) \\times 1000

This is handled automatically by the :meth:`opensection.utils.UnitConverter.stress_area_to_force` method.

Examples
--------

Unit Conversions
~~~~~~~~~~~~~~~~

.. code-block:: python

   from opensection.utils import Length, Force, UnitConverter
   
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
   from opensection.utils import safe_divide, clamp, is_converged
   
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

   from opensection.utils import MaterialConstants, NumericalConstants
   
   # Material properties
   E_steel = MaterialConstants.E_STEEL_DEFAULT  # 200000 MPa
   gamma_c = MaterialConstants.GAMMA_C_DEFAULT  # 1.5
   
   # Numerical parameters
   tolerance = NumericalConstants.TOL_FORCE_DEFAULT  # 1e-6 kN
   max_iter = NumericalConstants.MAX_ITER_DEFAULT    # 50

