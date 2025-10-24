"""
Exemple : Génération de diagrammes d'interaction N-M
"""

import numpy as np
import opensection as ops

try:
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("matplotlib non disponible - graphiques désactivés")


def example_rectangular_section_interaction():
    """Génère un diagramme d'interaction pour une section rectangulaire"""
    print("\n" + "=" * 70)
    print("DIAGRAMME D'INTERACTION - SECTION RECTANGULAIRE")
    print("=" * 70)

    # Définir la section
    width = 0.3  # m
    height = 0.5  # m
    section = ops.RectangularSection(width=width, height=height)

    print(f"\nSection: {width}m x {height}m")
    print(f"Aire: {section.properties.area*1e4:.2f} cm²")

    # Matériaux
    concrete = ops.ConcreteEC2(fck=30)
    steel = ops.SteelEC2(fyk=500)

    print(f"\nMatériaux:")
    print(f"  Béton: C30/37 (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier: B500B (fyd = {steel.fyd:.2f} MPa)")

    # Armatures symétriques
    rebars = ops.RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)  # 3HA20 haut
    rebars.add_rebar(y=-0.20, z=0.0, diameter=0.020, n=3)  # 3HA20 bas

    print(f"\nArmatures:")
    print(f"  Haut: 3HA20")
    print(f"  Bas: 3HA20")
    print(f"  As,tot = {rebars.total_area*1e4:.2f} cm²")

    # Créer le solver
    solver = ops.SectionSolver(section, concrete, steel, rebars)

    print(f"\nMaillage: {len(solver.fibers)} fibres de béton")

    # Créer le diagramme d'interaction
    diagram = ops.InteractionDiagram(solver)

    print("\nCalcul des points de la courbe d'interaction...")

    # Calculer plusieurs points de la courbe N-M
    N_values = np.linspace(0, 3000, 20)  # kN
    M_capacity = []
    N_capacity = []

    for N in N_values:
        # Recherche du moment résistant pour cet effort normal
        for M_trial in np.linspace(250, 50, 15):
            try:
                result = solver.solve(N=N, My=0, Mz=M_trial, tol=1e-2)
                if result.converged:
                    M_capacity.append(result.Mz)
                    N_capacity.append(result.N)
                    print(f"  N = {result.N:6.1f} kN, M = {result.Mz:6.1f} kN·m [iter={result.n_iter}]")
                    break
            except Exception:
                continue

    print(f"\n{len(M_capacity)} points calculés sur la courbe d'interaction")

    # Tracer le diagramme
    if HAS_MATPLOTLIB and len(M_capacity) > 0:
        plt.figure(figsize=(10, 8))

        plt.plot(M_capacity, N_capacity, "bo-", linewidth=2, markersize=6, label="Courbe d'interaction")
        plt.fill_between(M_capacity, 0, N_capacity, alpha=0.2, color="blue", label="Zone admissible")

        # Points particuliers
        # Flexion pure (N≈0)
        if len(M_capacity) > 0:
            idx_flex = np.argmin(N_capacity)
            plt.plot(
                M_capacity[idx_flex],
                N_capacity[idx_flex],
                "ro",
                markersize=10,
                label=f"Flexion pure (M={M_capacity[idx_flex]:.1f} kN·m)",
            )

        # Compression max
        idx_comp = np.argmax(N_capacity)
        plt.plot(
            M_capacity[idx_comp],
            N_capacity[idx_comp],
            "go",
            markersize=10,
            label=f"Compression max (N={N_capacity[idx_comp]:.1f} kN)",
        )

        plt.xlabel("Moment Mz [kN·m]", fontsize=12)
        plt.ylabel("Effort normal N [kN] (+ compression)", fontsize=12)
        plt.title("Diagramme d'interaction N-M (Section rectangulaire)", fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.savefig("interaction_diagram_rectangular.png", dpi=150)
        print("\n✓ Graphique sauvegardé: interaction_diagram_rectangular.png")
        plt.close()


def example_circular_section_interaction():
    """Génère un diagramme d'interaction pour une section circulaire"""
    print("\n" + "=" * 70)
    print("DIAGRAMME D'INTERACTION - SECTION CIRCULAIRE")
    print("=" * 70)

    # Définir la section
    diameter = 0.5  # m
    section = ops.CircularSection(diameter=diameter)

    print(f"\nSection: Ø {diameter}m")
    print(f"Aire: {section.properties.area*1e4:.2f} cm²")

    # Matériaux
    concrete = ops.ConcreteEC2(fck=30)
    steel = ops.SteelEC2(fyk=500)

    print(f"\nMatériaux:")
    print(f"  Béton: C30/37 (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier: B500B (fyd = {steel.fyd:.2f} MPa)")

    # Armatures circulaires
    rebars = ops.RebarGroup()
    n_bars = 8
    rebars.add_circular_array(center_y=0.0, center_z=0.0, radius=0.20, n=n_bars, diameter=0.020)

    print(f"\nArmatures:")
    print(f"  {n_bars}HA20 en nappe circulaire")
    print(f"  As,tot = {rebars.total_area*1e4:.2f} cm²")

    # Créer le solver
    solver = ops.SectionSolver(section, concrete, steel, rebars)

    print(f"\nMaillage: {len(solver.fibers)} fibres de béton")

    print("\nCalcul des points de la courbe d'interaction...")

    # Calculer plusieurs points
    N_values = np.linspace(100, 4000, 20)  # kN
    M_capacity = []
    N_capacity = []

    for N in N_values:
        # Recherche du moment résistant
        for M_trial in np.linspace(350, 100, 15):
            try:
                result = solver.solve(N=N, My=0, Mz=M_trial, tol=1e-2)
                if result.converged:
                    M_capacity.append(result.Mz)
                    N_capacity.append(result.N)
                    print(f"  N = {result.N:6.1f} kN, M = {result.Mz:6.1f} kN·m [iter={result.n_iter}]")
                    break
            except Exception:
                continue

    print(f"\n{len(M_capacity)} points calculés sur la courbe d'interaction")

    # Tracer le diagramme
    if HAS_MATPLOTLIB and len(M_capacity) > 0:
        plt.figure(figsize=(10, 8))

        plt.plot(M_capacity, N_capacity, "ro-", linewidth=2, markersize=6, label="Courbe d'interaction")
        plt.fill_between(M_capacity, 0, N_capacity, alpha=0.2, color="red", label="Zone admissible")

        plt.xlabel("Moment Mz [kN·m]", fontsize=12)
        plt.ylabel("Effort normal N [kN] (+ compression)", fontsize=12)
        plt.title("Diagramme d'interaction N-M (Section circulaire)", fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best")
        plt.tight_layout()
        plt.savefig("interaction_diagram_circular.png", dpi=150)
        print("\n✓ Graphique sauvegardé: interaction_diagram_circular.png")
        plt.close()


def example_comparison_different_reinforcement():
    """Compare des diagrammes avec différentes quantités d'armatures"""
    print("\n" + "=" * 70)
    print("COMPARAISON - INFLUENCE DU FERRAILLAGE")
    print("=" * 70)

    # Section de base
    section = ops.RectangularSection(width=0.3, height=0.5)
    concrete = ops.ConcreteEC2(fck=30)
    steel = ops.SteelEC2(fyk=500)

    print("\nSection: 0.3m x 0.5m")
    print("Béton: C30/37")
    print("Acier: B500B")

    # Trois configurations d'armatures
    configs = [
        {"name": "Faible (4HA16)", "n_bars": 2, "diameter": 0.016},
        {"name": "Moyenne (6HA20)", "n_bars": 3, "diameter": 0.020},
        {"name": "Forte (8HA25)", "n_bars": 4, "diameter": 0.025},
    ]

    results_all = []

    for config in configs:
        print(f"\n--- Configuration: {config['name']} ---")

        rebars = ops.RebarGroup()
        rebars.add_rebar(y=0.20, z=0.0, diameter=config["diameter"], n=config["n_bars"])
        rebars.add_rebar(y=-0.20, z=0.0, diameter=config["diameter"], n=config["n_bars"])

        print(f"As,tot = {rebars.total_area*1e4:.2f} cm²")

        solver = ops.SectionSolver(section, concrete, steel, rebars)

        N_values = np.linspace(100, 2500, 15)
        M_capacity = []
        N_capacity = []

        for N in N_values:
            for M_trial in np.linspace(200, 50, 10):
                try:
                    result = solver.solve(N=N, My=0, Mz=M_trial, tol=1e-2)
                    if result.converged:
                        M_capacity.append(result.Mz)
                        N_capacity.append(result.N)
                        break
                except Exception:
                    continue

        results_all.append({"config": config, "M": M_capacity, "N": N_capacity})
        print(f"  {len(M_capacity)} points calculés")

    # Tracer la comparaison
    if HAS_MATPLOTLIB:
        plt.figure(figsize=(12, 8))

        colors = ["blue", "green", "red"]
        for i, res in enumerate(results_all):
            if len(res["M"]) > 0:
                plt.plot(
                    res["M"],
                    res["N"],
                    "o-",
                    color=colors[i],
                    linewidth=2,
                    markersize=5,
                    label=res["config"]["name"],
                )

        plt.xlabel("Moment Mz [kN·m]", fontsize=12)
        plt.ylabel("Effort normal N [kN] (+ compression)", fontsize=12)
        plt.title(
            "Influence de la quantité d'armatures sur le diagramme N-M",
            fontsize=14,
            fontweight="bold",
        )
        plt.grid(True, alpha=0.3)
        plt.legend(loc="best", fontsize=11)
        plt.tight_layout()
        plt.savefig("interaction_comparison_reinforcement.png", dpi=150)
        print("\n✓ Graphique sauvegardé: interaction_comparison_reinforcement.png")
        plt.close()


def main():
    print("=" * 70)
    print("EXEMPLES DE DIAGRAMMES D'INTERACTION N-M")
    print("=" * 70)

    if not HAS_MATPLOTLIB:
        print("\n⚠ matplotlib non installé - graphiques désactivés")
        print("Pour visualiser, installez: pip install matplotlib\n")

    example_rectangular_section_interaction()
    example_circular_section_interaction()
    example_comparison_different_reinforcement()

    print("\n" + "=" * 70)
    print("EXEMPLES TERMINÉS")
    print("=" * 70)


if __name__ == "__main__":
    main()

