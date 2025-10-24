"""
Example: Section Visualization and Report Generation

This example demonstrates how to:
1. Create sections
2. Solve for given loads
3. Generate text reports
4. Visualize sections with fiber mesh
5. Save plots to files

Author: SectionPy Contributors
"""

import matplotlib.pyplot as plt

from sectionpy.geometry.section import CircularSection, RectangularSection
from sectionpy.materials.concrete import ConcreteEC2
from sectionpy.materials.steel import SteelEC2
from sectionpy.postprocess.report import ReportGenerator
from sectionpy.postprocess.visualization import SectionPlotter
from sectionpy.reinforcement.rebar import RebarGroup
from sectionpy.solver.section_solver import SectionSolver

print("=" * 70)
print("SectionPy - VISUALIZATION AND REPORT GENERATION EXAMPLE")
print("=" * 70)
print()

# ============================================================================
# EXAMPLE 1: Rectangular Section with Report
# ============================================================================
print("EXAMPLE 1: Rectangular Section Analysis with Report")
print("-" * 70)

# Define section
b, h = 0.3, 0.5
section_rect = RectangularSection(width=b, height=h)

# Define materials
concrete = ConcreteEC2(fck=30)  # C30/37
steel = SteelEC2(fyk=500)  # B500B

# Add reinforcement
rebars = RebarGroup()
rebars.add_rebar(y=-0.20, z=0.0, diameter=0.020, n=3)  # 3Ø20 bottom
rebars.add_rebar(y=0.20, z=0.0, diameter=0.016, n=2)  # 2Ø16 top

print(f"\nSection: {b*1000:.0f}x{h*1000:.0f} mm")
print(f"Concrete: C30/37 (fcd = {concrete.fcd:.2f} MPa)")
print(f"Steel: B500B (fyd = {steel.fyd:.2f} MPa)")
print("Reinforcement: 3D20 + 2D16")

# Solve
solver = SectionSolver(section_rect, concrete, steel, rebars)
result = solver.solve(N=500, My=0, Mz=100)

# Generate report
print("\n" + "=" * 70)
print("TEXT REPORT:")
print("=" * 70)
report = ReportGenerator.generate_text_report(result)
# Print with UTF-8 encoding handling for Windows console
try:
    print(report)
except UnicodeEncodeError:
    # Fallback for Windows console
    print(report.encode('ascii', 'replace').decode('ascii'))

# Visualize section
print("\nGenerating visualization...")
fig1, ax1 = SectionPlotter.plot_section(section_rect, show_fibers=False)
ax1.set_title(f"Rectangular Section {b*1000:.0f}x{h*1000:.0f} mm")

# Add rebars to plot
for rebar in rebars.rebars:
    ax1.plot(rebar.y, rebar.z, "ro", markersize=8, markeredgewidth=1, markeredgecolor="k")

plt.savefig("section_rectangular.png", dpi=150, bbox_inches="tight")
print("  -> Saved: section_rectangular.png")

# ============================================================================
# EXAMPLE 2: Circular Section with Fiber Mesh
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: Circular Section with Fiber Mesh Visualization")
print("-" * 70)

diameter = 0.4
section_circ = CircularSection(diameter=diameter, n_points=24)

# Add circular rebar arrangement
import numpy as np

rebars_circ = RebarGroup()
n_bars = 8
radius_bars = diameter / 2 - 0.05
for i in range(n_bars):
    angle = 2 * np.pi * i / n_bars
    y = radius_bars * np.cos(angle)
    z = radius_bars * np.sin(angle)
    rebars_circ.add_rebar(y=y, z=z, diameter=0.020, n=1)

print(f"\nCircular section: D{diameter*1000:.0f} mm")
print(f"Reinforcement: {n_bars}D20 in circle")

# Solve
solver_circ = SectionSolver(section_circ, concrete, steel, rebars_circ, fiber_area=0.0001)
result_circ = solver_circ.solve(N=800, My=0, Mz=50)

print(f"\nLoads: N = 800 kN, M = 50 kN·m")
print(f"Convergence: {'YES' if result_circ.converged else 'NO'}")
print(f"Iterations: {result_circ.n_iter}")
print(f"Max concrete stress: {result_circ.sigma_c_max:.2f} MPa")

# Visualize with fibers
fig2, ax2 = SectionPlotter.plot_section(section_circ, show_fibers=True)
ax2.set_title(f"Circular Section D{diameter*1000:.0f} mm - Fiber Mesh")

# Add rebars
for rebar in rebars_circ.rebars:
    ax2.plot(rebar.y, rebar.z, "ro", markersize=10, markeredgewidth=1.5, markeredgecolor="k")

plt.savefig("section_circular_fibers.png", dpi=150, bbox_inches="tight")
print("\n  -> Saved: section_circular_fibers.png")

# ============================================================================
# EXAMPLE 3: Comparison Plot
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Multiple Sections Comparison")
print("-" * 70)

fig3, axes = plt.subplots(1, 2, figsize=(14, 7))

# Plot rectangular
SectionPlotter.plot_section(section_rect, show_fibers=False)
plt.sca(axes[0])
plt.cla()
for contour in section_rect.contours:
    points = contour.to_array()
    axes[0].plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    axes[0].fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lightblue")
for rebar in rebars.rebars:
    axes[0].plot(rebar.y, rebar.z, "ro", markersize=8)
axes[0].set_aspect("equal")
axes[0].grid(True, alpha=0.3)
axes[0].set_xlabel("y (m)")
axes[0].set_ylabel("z (m)")
axes[0].set_title("Rectangular Section")

# Plot circular
for contour in section_circ.contours:
    points = contour.to_array()
    axes[1].plot(points[:, 0], points[:, 1], "b-", linewidth=2)
    axes[1].fill(points[:, 0], points[:, 1], alpha=0.3, facecolor="lightgreen")
for rebar in rebars_circ.rebars:
    axes[1].plot(rebar.y, rebar.z, "ro", markersize=8)
axes[1].set_aspect("equal")
axes[1].grid(True, alpha=0.3)
axes[1].set_xlabel("y (m)")
axes[1].set_ylabel("z (m)")
axes[1].set_title("Circular Section")

plt.tight_layout()
plt.savefig("section_comparison.png", dpi=150, bbox_inches="tight")
print("\n  -> Saved: section_comparison.png")

# ============================================================================
# EXAMPLE 4: Detailed Report with EC2 Verification
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Detailed Report with Code Checks")
print("-" * 70)

from sectionpy.eurocodes.verification import EC2Verification

# Generate extended report
print("\n" + "=" * 70)
print("EXTENDED ANALYSIS REPORT")
print("=" * 70)
print()
print("SECTION PROPERTIES:")
print(f"  Type: Rectangular {b*1000:.0f}x{h*1000:.0f} mm")
props = section_rect.properties
print(f"  Area: {props.area*1e4:.2f} cm^2")
print(f"  I_yy: {props.I_yy*1e8:.2f} cm^4")
print(f"  I_zz: {props.I_zz*1e8:.2f} cm^4")
print()
print("MATERIALS:")
print(f"  Concrete C30/37:")
print(f"    fck = {concrete.fck:.1f} MPa")
print(f"    fcd = {concrete.fcd:.2f} MPa")
print(f"    Ecm = {concrete.Ecm:.0f} MPa")
print(f"  Steel B500B:")
print(f"    fyk = {steel.fyk:.1f} MPa")
print(f"    fyd = {steel.fyd:.2f} MPa")
print(f"    Es = {steel.Es:.0f} MPa")
print()
print("REINFORCEMENT:")
total_As = sum(3.14159 * (d / 2) ** 2 * n for y, z, d, n in [(r.y, r.z, r.diameter, r.n) for r in rebars.rebars])
print(f"  Total As = {total_As*1e4:.2f} cm^2")
print(f"  Reinforcement ratio = {total_As/(b*h)*100:.2f} %")
print()

# Solver results
print("SOLVER RESULTS:")
print(f"  Convergence: {'YES' if result.converged else 'NO'}")
print(f"  Iterations: {result.n_iter}")
print(f"  Deformation: eps_0 = {result.epsilon_0*1000:.3f} per mil")
print(f"  Curvature: chi_z = {result.chi_z:.6e} rad/m")
print(f"  Neutral axis depth: {result.neutral_axis_depth*100:.2f} cm")
print()
print("STRESSES:")
print(f"  sigma_c,max = {result.sigma_c_max:.2f} MPa")
print(f"  sigma_s,max = {result.sigma_s_max:.2f} MPa")
print()

# EC2 verification
checks = EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
print("EUROCODE 2 VERIFICATION (ULS):")
print(f"  Concrete stress: {checks['concrete_stress']['ratio']*100:.1f}% - {'OK' if checks['concrete_stress']['ok'] else 'FAIL'}")
print(f"  Steel stress: {checks['steel_stress']['ratio']*100:.1f}% - {'OK' if checks['steel_stress']['ok'] else 'FAIL'}")

print("\n" + "=" * 70)
print("\nAll visualizations saved successfully!")
print("=" * 70)

# Show all plots
plt.show()

