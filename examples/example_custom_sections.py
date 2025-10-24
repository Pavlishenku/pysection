"""
Example: Custom/Arbitrary Section Contours

This example demonstrates how to:
1. Create custom polygon contours (L-shape, T-shape, trapezoid)
2. Create sections with holes (hollow sections)
3. Analyze custom sections with the solver
4. Visualize complex geometries

Author: SectionPy Contributors
"""

import matplotlib.pyplot as plt
import numpy as np

from pysection.geometry import Contour, Point
from pysection.geometry.section import Section
from pysection.materials.concrete import ConcreteEC2
from pysection.materials.steel import SteelEC2
from pysection.postprocess.report import ReportGenerator
from pysection.postprocess.visualization import SectionPlotter
from pysection.reinforcement.rebar import RebarGroup
from pysection.solver.section_solver import SectionSolver

print("=" * 70)
print("SectionPy - CUSTOM SECTION CONTOURS EXAMPLE")
print("=" * 70)
print()

# ============================================================================
# EXAMPLE 1: L-Shaped Section
# ============================================================================
print("EXAMPLE 1: L-Shaped Section")
print("-" * 70)

# Define L-shape vertices (in meters)
# 300mm x 400mm L-shape with 150mm legs
vertices_L = [
    (0.0, 0.0),    # Bottom-left
    (0.3, 0.0),    # Bottom-right
    (0.3, 0.15),   # Inner corner (right)
    (0.15, 0.15),  # Inner corner (top of vertical leg)
    (0.15, 0.4),   # Top of vertical leg
    (0.0, 0.4),    # Top-left
]

contour_L = Contour.polygon(vertices_L)
section_L = Section([contour_L])

print(f"L-section properties:")
props_L = section_L.properties
print(f"  Area: {props_L.area*1e4:.2f} cm^2")
print(f"  Centroid: y={props_L.centroid[0]*100:.2f} cm, z={props_L.centroid[1]*100:.2f} cm")

# Add reinforcement
rebars_L = RebarGroup()
rebars_L.add_rebar(y=0.075, z=0.05, diameter=0.016, n=2)   # Bottom of horizontal leg
rebars_L.add_rebar(y=0.075, z=0.35, diameter=0.016, n=2)   # Top of vertical leg
rebars_L.add_rebar(y=0.225, z=0.05, diameter=0.012, n=2)   # End of horizontal leg

print(f"  Reinforcement: 4D16 + 2D12")

# Solve
concrete = ConcreteEC2(fck=30)
steel = SteelEC2(fyk=500)

solver_L = SectionSolver(section_L, concrete, steel, rebars_L, fiber_area=0.001)
result_L = solver_L.solve(N=300, My=0, Mz=50)

print(f"\nLoads: N=300 kN, Mz=50 kN.m")
print(f"Convergence: {'YES' if result_L.converged else 'NO'}")
print(f"Max concrete stress: {result_L.sigma_c_max:.2f} MPa")
print(f"Max steel stress: {result_L.sigma_s_max:.2f} MPa")

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# L-section
ax = axes[0, 0]
for contour in section_L.contours:
    points = contour.to_array()
    ax.plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    ax.fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lightblue")
for rebar in rebars_L.rebars:
    ax.plot(rebar.y, rebar.z, "ro", markersize=8)
ax.plot(props_L.centroid[0], props_L.centroid[1], "r+", markersize=15, markeredgewidth=2)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel("y (m)")
ax.set_ylabel("z (m)")
ax.set_title("L-Shaped Section (300x400 mm)")

# ============================================================================
# EXAMPLE 2: T-Shaped Section
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: T-Shaped Section (T-Beam)")
print("-" * 70)

# T-shape: 400mm wide flange, 100mm thick flange, 100mm wide web, 300mm web height
vertices_T = [
    (-0.2, 0.0),    # Left of flange
    (0.2, 0.0),     # Right of flange
    (0.2, 0.1),     # Right bottom of flange
    (0.05, 0.1),    # Right of web
    (0.05, 0.4),    # Top right of web
    (-0.05, 0.4),   # Top left of web
    (-0.05, 0.1),   # Left of web
    (-0.2, 0.1),    # Left bottom of flange
]

contour_T = Contour.polygon(vertices_T)
section_T = Section([contour_T])

props_T = section_T.properties
print(f"T-section properties:")
print(f"  Area: {props_T.area*1e4:.2f} cm^2")
print(f"  Centroid z: {props_T.centroid[1]*100:.2f} cm from bottom")

# Add reinforcement
rebars_T = RebarGroup()
rebars_T.add_rebar(y=0.0, z=0.05, diameter=0.020, n=3)    # Bottom of flange
rebars_T.add_rebar(y=0.0, z=0.35, diameter=0.012, n=2)    # Top of web

print(f"  Reinforcement: 3D20 bottom, 2D12 top")

solver_T = SectionSolver(section_T, concrete, steel, rebars_T, fiber_area=0.001)
result_T = solver_T.solve(N=400, My=0, Mz=100)

print(f"\nLoads: N=400 kN, Mz=100 kN.m")
print(f"Convergence: {'YES' if result_T.converged else 'NO'}")
print(f"Max concrete stress: {result_T.sigma_c_max:.2f} MPa")

# Visualize
ax = axes[0, 1]
for contour in section_T.contours:
    points = contour.to_array()
    ax.plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    ax.fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lightgreen")
for rebar in rebars_T.rebars:
    ax.plot(rebar.y, rebar.z, "ro", markersize=8)
ax.plot(props_T.centroid[0], props_T.centroid[1], "r+", markersize=15, markeredgewidth=2)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel("y (m)")
ax.set_ylabel("z (m)")
ax.set_title("T-Shaped Section (400x400 mm)")

# ============================================================================
# EXAMPLE 3: Trapezoidal Section
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Trapezoidal Section")
print("-" * 70)

# Trapezoid: bottom 500mm, top 300mm, height 500mm
vertices_trap = [
    (0.0, 0.0),     # Bottom-left
    (0.5, 0.0),     # Bottom-right
    (0.4, 0.5),     # Top-right
    (0.1, 0.5),     # Top-left
]

contour_trap = Contour.polygon(vertices_trap)
section_trap = Section([contour_trap])

props_trap = section_trap.properties
print(f"Trapezoid section properties:")
print(f"  Area: {props_trap.area*1e4:.2f} cm^2")

# Add reinforcement
rebars_trap = RebarGroup()
rebars_trap.add_rebar(y=0.25, z=0.05, diameter=0.020, n=4)   # Bottom
rebars_trap.add_rebar(y=0.25, z=0.45, diameter=0.012, n=2)   # Top

solver_trap = SectionSolver(section_trap, concrete, steel, rebars_trap, fiber_area=0.001)
result_trap = solver_trap.solve(N=500, My=0, Mz=100)

print(f"\nLoads: N=500 kN, Mz=100 kN.m")
print(f"Convergence: {'YES' if result_trap.converged else 'NO'}")
print(f"Max concrete stress: {result_trap.sigma_c_max:.2f} MPa")

# Visualize
ax = axes[1, 0]
for contour in section_trap.contours:
    points = contour.to_array()
    ax.plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    ax.fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lightyellow")
for rebar in rebars_trap.rebars:
    ax.plot(rebar.y, rebar.z, "ro", markersize=8)
ax.plot(props_trap.centroid[0], props_trap.centroid[1], "r+", markersize=15, markeredgewidth=2)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel("y (m)")
ax.set_ylabel("z (m)")
ax.set_title("Trapezoidal Section (500x500 mm)")

# ============================================================================
# EXAMPLE 4: Hollow Rectangular Section (with hole)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Hollow Rectangular Section")
print("-" * 70)

# Outer rectangle: 400x600mm
outer = Contour.rectangle(width=0.4, height=0.6)

# Inner rectangle (hole): 200x300mm
inner = Contour.rectangle(width=0.2, height=0.3)
inner.is_hole = True

section_hollow = Section([outer, inner])

props_hollow = section_hollow.properties
print(f"Hollow section properties:")
print(f"  Outer: 400x600 mm")
print(f"  Inner: 200x300 mm (hole)")
print(f"  Net area: {props_hollow.area*1e4:.2f} cm^2")

# Add reinforcement in corners
rebars_hollow = RebarGroup()
rebars_hollow.add_rebar(y=-0.15, z=-0.25, diameter=0.020, n=1)
rebars_hollow.add_rebar(y=0.15, z=-0.25, diameter=0.020, n=1)
rebars_hollow.add_rebar(y=-0.15, z=0.25, diameter=0.020, n=1)
rebars_hollow.add_rebar(y=0.15, z=0.25, diameter=0.020, n=1)

solver_hollow = SectionSolver(section_hollow, concrete, steel, rebars_hollow, fiber_area=0.001)
result_hollow = solver_hollow.solve(N=600, My=0, Mz=150)

print(f"\nLoads: N=600 kN, Mz=150 kN.m")
print(f"Convergence: {'YES' if result_hollow.converged else 'NO'}")
print(f"Max concrete stress: {result_hollow.sigma_c_max:.2f} MPa")

# Visualize
ax = axes[1, 1]
for contour in section_hollow.contours:
    points = contour.to_array()
    ax.plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    if contour.is_hole:
        ax.fill(points[:, 0], points[:, 1], alpha=0.5, facecolor="white")
    else:
        ax.fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lightcoral")
for rebar in rebars_hollow.rebars:
    ax.plot(rebar.y, rebar.z, "ro", markersize=10)
ax.plot(props_hollow.centroid[0], props_hollow.centroid[1], "r+", markersize=15, markeredgewidth=2)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.set_xlabel("y (m)")
ax.set_ylabel("z (m)")
ax.set_title("Hollow Rectangular Section (400x600 mm)")

plt.tight_layout()
plt.savefig("custom_sections.png", dpi=150, bbox_inches="tight")
print("\n-> Saved: custom_sections.png")

# ============================================================================
# EXAMPLE 5: Hexagonal Section
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 5: Hexagonal Section")
print("-" * 70)

# Create hexagon
n_sides = 6
radius = 0.25
vertices_hex = []
for i in range(n_sides):
    angle = 2 * np.pi * i / n_sides
    y = radius * np.cos(angle)
    z = radius * np.sin(angle)
    vertices_hex.append((y, z))

contour_hex = Contour.polygon(vertices_hex)
section_hex = Section([contour_hex])

props_hex = section_hex.properties
print(f"Hexagonal section properties:")
print(f"  Radius (inscribed circle): {radius*1000:.0f} mm")
print(f"  Area: {props_hex.area*1e4:.2f} cm^2")

# Add reinforcement in a circle
rebars_hex = RebarGroup()
n_bars = 6
radius_bars = 0.15
for i in range(n_bars):
    angle = 2 * np.pi * i / n_bars
    y = radius_bars * np.cos(angle)
    z = radius_bars * np.sin(angle)
    rebars_hex.add_rebar(y=y, z=z, diameter=0.016, n=1)

print(f"  Reinforcement: 6D16 in circular array")

solver_hex = SectionSolver(section_hex, concrete, steel, rebars_hex, fiber_area=0.001)
result_hex = solver_hex.solve(N=350, My=0, Mz=60)

print(f"\nLoads: N=350 kN, Mz=60 kN.m")
print(f"Convergence: {'YES' if result_hex.converged else 'NO'}")
print(f"Max concrete stress: {result_hex.sigma_c_max:.2f} MPa")

# Visualize hexagon
fig2, ax2 = plt.subplots(figsize=(8, 8))
for contour in section_hex.contours:
    points = contour.to_array()
    ax2.plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    ax2.fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lavender")
for rebar in rebars_hex.rebars:
    ax2.plot(rebar.y, rebar.z, "ro", markersize=10)
ax2.plot(props_hex.centroid[0], props_hex.centroid[1], "r+", markersize=15, markeredgewidth=2)
ax2.set_aspect("equal")
ax2.grid(True, alpha=0.3)
ax2.set_xlabel("y (m)")
ax2.set_ylabel("z (m)")
ax2.set_title("Hexagonal Section")
plt.savefig("hexagonal_section.png", dpi=150, bbox_inches="tight")
print("-> Saved: hexagonal_section.png")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print()
print("Custom section shapes analyzed:")
print(f"  1. L-shape:      Area = {props_L.area*1e4:.2f} cm^2, sigma_c = {result_L.sigma_c_max:.1f} MPa")
print(f"  2. T-shape:      Area = {props_T.area*1e4:.2f} cm^2, sigma_c = {result_T.sigma_c_max:.1f} MPa")
print(f"  3. Trapezoid:    Area = {props_trap.area*1e4:.2f} cm^2, sigma_c = {result_trap.sigma_c_max:.1f} MPa")
print(f"  4. Hollow rect:  Area = {props_hollow.area*1e4:.2f} cm^2, sigma_c = {result_hollow.sigma_c_max:.1f} MPa")
print(f"  5. Hexagon:      Area = {props_hex.area*1e4:.2f} cm^2, sigma_c = {result_hex.sigma_c_max:.1f} MPa")
print()
print("All sections converged successfully!")
print("=" * 70)

plt.show()

