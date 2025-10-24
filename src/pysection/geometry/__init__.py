"""
Geometry module for SectionPy

This module provides classes for representing cross-section geometry,
computing geometric properties, and creating fiber meshes for analysis.
"""

from pysection.geometry.contour import Contour, Point
from pysection.geometry.properties import GeometricProperties
from pysection.geometry.section import CircularSection, RectangularSection, Section, TSection

__all__ = [
    "Point",
    "Contour",
    "GeometricProperties",
    "Section",
    "RectangularSection",
    "CircularSection",
    "TSection",
]
