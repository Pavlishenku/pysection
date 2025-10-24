"""
Validation module with analytical reference cases and validators
"""

from sectionpy.validation.analytical_cases import (
    RectangularBeamCase,
    TBeamCase,
    ValidationDatabase,
)
from sectionpy.validation.exceptions import (
    GeometryValidationError,
    LoadValidationError,
    MaterialValidationError,
    RebarValidationError,
    ValidationError,
)
from sectionpy.validation.validators import (
    GeometryValidator,
    LoadValidator,
    MaterialValidator,
    RebarValidator,
    SectionValidator,
)

__all__ = [
    # Analytical cases
    "RectangularBeamCase",
    "TBeamCase",
    "ValidationDatabase",
    # Exceptions
    "ValidationError",
    "GeometryValidationError",
    "MaterialValidationError",
    "RebarValidationError",
    "LoadValidationError",
    # Validators
    "GeometryValidator",
    "MaterialValidator",
    "RebarValidator",
    "LoadValidator",
    "SectionValidator",
]
