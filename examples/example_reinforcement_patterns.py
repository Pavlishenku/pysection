"""
Exemple : Différentes dispositions de ferraillage
"""

import numpy as np
import opensection as ops

try:
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("matplotlib non disponible - graphiques désactivés")


def example_simple_two_layers():
    """Exemple simple: 2 nappes d'armatures"""
    print("\n" + "=" * 70)
    print("EXEMPLE 1 : DEUX NAPPES D'ARMATURES (HAUT ET BAS)")
    print("=" * 70)

    # Section
    width = 0.3
    height = 0.5

    # Armatures
    rebars = ops.RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)  # 3HA20 haut
    rebars.add_rebar(y=-0.20, z=0.0, diameter=0.020, n=3)  # 3HA20 bas

    print(f"\nSection: {width}m x {height}m")
    print(f"Armatures:")
    print(f"  Nappe haute: 3HA20 à y=0.20m")
    print(f"  Nappe basse: 3HA20 à y=-0.20m")
    print(f"  Aire totale: {rebars.total_area*1e4:.2f} cm²")

    # Visualisation
    if HAS_MATPLOTLIB:
        plot_section_with_rebars(width, height, rebars, "reinforcement_simple.png")


def example_linear_array():
    """Exemple: nappe linéaire d'armatures"""
    print("\n" + "=" * 70)
    print("EXEMPLE 2 : NAPPE LINÉAIRE D'ARMATURES")
    print("=" * 70)

    # Section
    width = 0.4
    height = 0.6

    # Armatures avec nappe linéaire
    rebars = ops.RebarGroup()

    # Nappe supérieure : 5 barres espacées
    rebars.add_linear_array(y1=-0.15, z1=-0.15, y2=-0.15, z2=0.15, n=5, diameter=0.016)

    # Nappe inférieure : 3 barres
    rebars.add_rebar(y=0.25, z=-0.10, diameter=0.020, n=1)
    rebars.add_rebar(y=0.25, z=0.0, diameter=0.020, n=1)
    rebars.add_rebar(y=0.25, z=0.10, diameter=0.020, n=1)

    print(f"\nSection: {width}m x {height}m")
    print(f"Armatures:")
    print(f"  Nappe haute: 5HA16 en nappe linéaire")
    print(f"  Nappe basse: 3HA20")
    print(f"  Total: {rebars.n_rebars} barres")
    print(f"  Aire totale: {rebars.total_area*1e4:.2f} cm²")

    # Visualisation
    if HAS_MATPLOTLIB:
        plot_section_with_rebars(width, height, rebars, "reinforcement_linear_array.png")


def example_circular_array():
    """Exemple: nappe circulaire pour poteau"""
    print("\n" + "=" * 70)
    print("EXEMPLE 3 : NAPPE CIRCULAIRE (POTEAU CIRCULAIRE)")
    print("=" * 70)

    # Section circulaire
    diameter = 0.5

    # Armatures en cercle
    rebars = ops.RebarGroup()
    n_bars = 8
    rebars.add_circular_array(center_y=0.0, center_z=0.0, radius=0.20, n=n_bars, diameter=0.020)

    print(f"\nSection: Ø{diameter}m")
    print(f"Armatures:")
    print(f"  {n_bars}HA20 en nappe circulaire")
    print(f"  Rayon de la nappe: 0.20m")
    print(f"  Aire totale: {rebars.total_area*1e4:.2f} cm²")

    # Visualisation
    if HAS_MATPLOTLIB:
        plot_circular_section_with_rebars(diameter, rebars, "reinforcement_circular.png")


def example_complex_pattern():
    """Exemple: disposition complexe avec plusieurs nappes"""
    print("\n" + "=" * 70)
    print("EXEMPLE 4 : DISPOSITION COMPLEXE (POUTRE HAUTE)")
    print("=" * 70)

    # Section en T (approximée par rectangles)
    width = 0.6  # Large semelle
    height = 0.8

    # Armatures complexes
    rebars = ops.RebarGroup()

    # Nappe supérieure (zone comprimée) : 5HA16
    rebars.add_linear_array(y1=0.35, z1=-0.25, y2=0.35, z2=0.25, n=5, diameter=0.016)

    # Nappe inférieure (zone tendue) : 2 nappes
    # Nappe 1 : 4HA25
    rebars.add_linear_array(y1=-0.35, z1=-0.20, y2=-0.35, z2=0.20, n=4, diameter=0.025)

    # Nappe 2 (légèrement au-dessus) : 3HA20
    rebars.add_linear_array(y1=-0.30, z1=-0.15, y2=-0.30, z2=0.15, n=3, diameter=0.020)

    # Armatures latérales (peau) : 2HA12 de chaque côté
    rebars.add_rebar(y=0.0, z=-0.28, diameter=0.012, n=1)
    rebars.add_rebar(y=0.0, z=0.28, diameter=0.012, n=1)

    print(f"\nSection: {width}m x {height}m")
    print(f"Armatures:")
    print(f"  Nappe haute: 5HA16")
    print(f"  Nappe basse 1: 4HA25")
    print(f"  Nappe basse 2: 3HA20")
    print(f"  Armatures de peau: 2HA12")
    print(f"  Total: {rebars.n_rebars} barres")
    print(f"  Aire totale: {rebars.total_area*1e4:.2f} cm²")

    # Visualisation
    if HAS_MATPLOTLIB:
        plot_section_with_rebars(width, height, rebars, "reinforcement_complex.png")


def example_cover_helpers():
    """Exemple: utilisation des helpers pour enrobage automatique"""
    print("\n" + "=" * 70)
    print("EXEMPLE 5 : HELPERS POUR ENROBAGE AUTOMATIQUE")
    print("=" * 70)

    from opensection.reinforcement.helpers import CoverHelper

    # Section
    width = 0.3
    height = 0.5
    diameter = 0.020
    cover = 0.03

    print(f"\nSection: {width}m x {height}m")
    print(f"Enrobage: {cover*100:.0f} mm")
    print(f"Diamètre barres: {diameter*1000:.0f} mm")

    # Calculer positions avec enrobage
    y_top, z_top = CoverHelper.rectangular_position_with_cover("top", width, height, diameter, cover)
    y_bottom, z_bottom = CoverHelper.rectangular_position_with_cover(
        "bottom", width, height, diameter, cover
    )

    print(f"\nPositions calculées:")
    print(f"  Haut: y={y_top:.3f}m, z={z_top:.3f}m")
    print(f"  Bas: y={y_bottom:.3f}m, z={z_bottom:.3f}m")

    # Créer une nappe avec le helper
    positions = CoverHelper.layer_positions_with_cover(
        position="top", width=width, height=height, n_bars=4, diameter=diameter, cover=cover
    )

    print(f"\nNappe de 4 barres en haut:")
    for i, (y, z) in enumerate(positions):
        print(f"  Barre {i+1}: y={y:.3f}m, z={z:.3f}m")

    # Créer les armatures
    rebars = ops.RebarGroup()
    for y, z in positions:
        rebars.add_rebar(y=y, z=z, diameter=diameter, n=1)

    # Nappe du bas
    positions_bottom = CoverHelper.layer_positions_with_cover(
        position="bottom", width=width, height=height, n_bars=4, diameter=diameter, cover=cover
    )

    for y, z in positions_bottom:
        rebars.add_rebar(y=y, z=z, diameter=diameter, n=1)

    print(f"\nTotal: {rebars.n_rebars} barres")

    # Visualisation
    if HAS_MATPLOTLIB:
        plot_section_with_rebars(width, height, rebars, "reinforcement_with_cover.png")


def plot_section_with_rebars(width, height, rebars, filename):
    """Trace la section avec les armatures"""
    fig, ax = plt.subplots(figsize=(8, 10))

    # Dessiner la section
    rect = plt.Rectangle(
        (-width / 2, -height / 2), width, height, fill=False, edgecolor="black", linewidth=2
    )
    ax.add_patch(rect)

    # Dessiner les armatures
    for rebar in rebars.rebars:
        for i in range(rebar.n):
            circle = plt.Circle(
                (rebar.z, rebar.y),
                rebar.diameter / 2,
                color="red",
                fill=True,
                alpha=0.7,
                edgecolor="darkred",
                linewidth=1.5,
            )
            ax.add_patch(circle)

    # Axes
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.3)

    # Limites et aspect
    margin = 0.1
    ax.set_xlim(-width / 2 - margin, width / 2 + margin)
    ax.set_ylim(-height / 2 - margin, height / 2 + margin)
    ax.set_aspect("equal")

    # Labels
    ax.set_xlabel("z [m]", fontsize=12)
    ax.set_ylabel("y [m]", fontsize=12)
    ax.set_title(f"Section {width}m x {height}m\n{rebars.n_rebars} armatures", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"✓ Graphique sauvegardé: {filename}")
    plt.close()


def plot_circular_section_with_rebars(diameter, rebars, filename):
    """Trace la section circulaire avec les armatures"""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Dessiner la section
    circle_section = plt.Circle((0, 0), diameter / 2, fill=False, edgecolor="black", linewidth=2)
    ax.add_patch(circle_section)

    # Dessiner les armatures
    for rebar in rebars.rebars:
        for i in range(rebar.n):
            circle = plt.Circle(
                (rebar.z, rebar.y),
                rebar.diameter / 2,
                color="red",
                fill=True,
                alpha=0.7,
                edgecolor="darkred",
                linewidth=1.5,
            )
            ax.add_patch(circle)

    # Axes
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.3)

    # Limites et aspect
    margin = 0.1
    ax.set_xlim(-diameter / 2 - margin, diameter / 2 + margin)
    ax.set_ylim(-diameter / 2 - margin, diameter / 2 + margin)
    ax.set_aspect("equal")

    # Labels
    ax.set_xlabel("z [m]", fontsize=12)
    ax.set_ylabel("y [m]", fontsize=12)
    ax.set_title(f"Section Ø{diameter}m\n{rebars.n_rebars} armatures", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"✓ Graphique sauvegardé: {filename}")
    plt.close()


def main():
    print("=" * 70)
    print("EXEMPLES DE DISPOSITIONS DE FERRAILLAGE")
    print("=" * 70)

    if not HAS_MATPLOTLIB:
        print("\n⚠ matplotlib non installé - graphiques désactivés")
        print("Pour visualiser, installez: pip install matplotlib\n")

    example_simple_two_layers()
    example_linear_array()
    example_circular_array()
    example_complex_pattern()
    example_cover_helpers()

    print("\n" + "=" * 70)
    print("EXEMPLES TERMINÉS")
    print("=" * 70)

    if HAS_MATPLOTLIB:
        print("\nGraphiques générés:")
        print("  - reinforcement_simple.png")
        print("  - reinforcement_linear_array.png")
        print("  - reinforcement_circular.png")
        print("  - reinforcement_complex.png")
        print("  - reinforcement_with_cover.png")


if __name__ == "__main__":
    main()

