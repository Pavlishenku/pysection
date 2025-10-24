"""
Solver module for SectionPy

This module provides numerical solvers for section analysis
using fiber discretization and Newton-Raphson method.
"""

from sectionpy.solver.section_solver import SectionSolver, SolverResult

__all__ = [
    "SectionSolver",
    "SolverResult",
]
