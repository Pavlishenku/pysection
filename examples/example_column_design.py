"""
Exemple de dimensionnement d'un poteau en béton armé selon Eurocode 2

Cas pratique : Poteau de bâtiment avec charge axiale importante et excentricité
Dimensions : 400×400mm, hauteur=3m, N_Ed=1500kN, e=50mm

Référence : Guide de dimensionnement EC2, exemples pratiques
"""
import numpy as np
import matplotlib.pyplot as plt
from opensection import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup, SectionSolver
from opensection.eurocodes import EC2Verification


def column_design_example():
    """Dimensionnement d'un poteau selon EC2"""

    print("Dimensionnement d'un poteau en béton armé")
    print("=" * 60)

    # Paramètres du poteau
    b = 0.4    # largeur (m)
    h = 0.4    # hauteur (m)
    L_col = 3.0  # hauteur d'étage (m)
    N_Ed = 1500  # Effort normal de calcul (kN)
    e = 0.05     # Excentricité accidentelle (m)

    # Calcul du moment dû à l'excentricité
    M_Ed = N_Ed * e  # kN·m

    print("Paramètres du poteau :")
    print(f"  Section : {b*1000:.0f}×{h*1000:.0f} mm")
    print(f"  Hauteur : {L_col} m")
    print(f"  Effort axial N_Ed = {N_Ed} kN")
    print(f"  Excentricité e = {e*1000:.0f} mm")
    print(f"  Moment M_Ed = {M_Ed:.1f} kN·m")

    # Matériaux selon EC2
    concrete = ConcreteEC2(fck=30)  # C30/37
    steel = SteelEC2(fyk=500)       # B500B

    print("
Matériaux :")
    print(f"  Béton {concrete.fck} MPa (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier {steel.fyk} MPa (fyd = {steel.fyd:.2f} MPa)")

    # Section géométrique
    section = RectangularSection(width=b, height=h)

    # Armatures pour poteau (armatures longitudinales + cadres)
    # Enrobage : c = 40mm (poteau)
    cover = 0.04  # m
    dia_long = 0.020  # Ø20mm armatures longitudinales
    dia_trans = 0.010  # Ø10mm cadres

    # Nombre d'armatures longitudinales (typiquement 4 à 8 pour poteau carré)
    n_long = 8  # 8 armatures Ø20

    # Position des armatures (cercle inscrit dans la section)
    r = (min(b, h) - 2*cover - dia_long) / 2  # rayon du cercle d'armatures

    rebars = RebarGroup()

    # Placement symétrique des armatures
    for i in range(n_long):
        angle = 2 * np.pi * i / n_long
        y = r * np.cos(angle)
        z = r * np.sin(angle)
        rebars.add_rebar(y=y, z=z, diameter=dia_long, n=1)

    print("
Armatures :")
    print(f"  Armatures longitudinales : {n_long}Ø{dia_long*1000:.0f} = {rebars.total_area*1e4:.1f} cm²")
    print(f"  Enrobage : {cover*1000:.0f} mm")

    # Création du solveur
    solver = SectionSolver(section, concrete, steel, rebars)

    print("
Analyse :")
    print(f"  Fibres béton : {len(solver.fibers)}")
    print(f"  Points d'armature : {len(solver.rebar_array)}")

    # Résolution pour les sollicitations
    result = solver.solve(N=N_Ed, My=0, Mz=M_Ed)

    print("
Résultats :")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'}")
    print(f"  Itérations : {result.n_iter}")
    print(f"  ε₀ = {result.epsilon_0*1000:.2f} ‰")
    print(f"  χ_y = {result.chi_y:.2e} rad/m")
    print(f"  χ_z = {result.chi_z:.2e} rad/m")
    print(f"  σ_c,max = {result.sigma_c_max:.2f} MPa")
    print(f"  σ_s,max = {result.sigma_s_max:.2f} MPa")

    # Vérifications EC2
    checks = EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)

    print("
Vérifications ELU :")
    concrete_check = checks['concrete_stress']
    steel_check = checks['steel_stress']

    print(f"  Béton : {concrete_check['ratio']:.2%} - {'OK' if concrete_check['ok'] else 'NOK'}")
    print(f"  Acier : {steel_check['ratio']:.2%} - {'OK' if steel_check['ok'] else 'NOK'}")

    # Vérification de stabilité (flambement)
    # Slenderness ratio λ = L_col / i_min
    I_min = b * h**3 / 12  # Inertie minimale
    i_min = np.sqrt(I_min / (b * h))  # Rayon de giration
    lambda_col = L_col / i_min

    print("
Stabilité :")
    print(f"  Inertie I_min = {I_min*1e6:.0f} cm⁴")
    print(f"  Rayon de giration i_min = {i_min*1000:.1f} mm")
    print(f"  Élancement λ = {lambda_col:.1f}")

    if lambda_col < 25:
        print("  ✓ Poteau court (pas de vérification flambement nécessaire)")
    else:
        print("  ⚠ Poteau élancé (vérification flambement recommandée)")

    return result, checks


def column_interaction_diagram():
    """Tracé du diagramme d'interaction N-M pour le poteau"""

    print("\n" + "=" * 60)
    print("DIAGRAMME D'INTERACTION N-M")
    print("=" * 60)

    # Configuration identique
    b, h = 0.4, 0.4
    concrete = ConcreteEC2(fck=30)
    steel = SteelEC2(fyk=500)

    section = RectangularSection(width=b, height=h)
    cover, dia_long = 0.04, 0.020
    r = (min(b, h) - 2*cover - dia_long) / 2

    rebars = RebarGroup()
    for i in range(8):
        angle = 2 * np.pi * i / 8
        y = r * np.cos(angle)
        z = r * np.sin(angle)
        rebars.add_rebar(y=y, z=z, diameter=dia_long, n=1)

    solver = SectionSolver(section, concrete, steel, rebars)

    # Points du diagramme d'interaction
    # Pour différents niveaux de moment, trouver N maximal
    M_values = np.linspace(0, 200, 20)  # kN·m
    N_max_values = []

    for M in M_values:
        # Recherche dichotomique du N maximal pour ce M
        N_min, N_max = 0, 2000  # kN

        for _ in range(15):  # 15 itérations pour précision ~1kN
            N_test = (N_min + N_max) / 2
            result = solver.solve(N=N_test, My=0, Mz=M)

            if result.converged and result.sigma_c_max <= concrete.fcd * 1.01:  # Marge 1%
                N_min = N_test
            else:
                N_max = N_test

        N_max_values.append(N_min)

    # Résistance pure en compression (M=0)
    result_comp = solver.solve(N=2000, My=0, Mz=0)
    N_pure_comp = result_comp.N if result_comp.converged else 0

    # Tracé du diagramme
    plt.figure(figsize=(10, 6))

    plt.plot(M_values, N_max_values, 'b-', linewidth=3, label='Capacité portante')
    plt.axhline(y=N_pure_comp, color='r', linestyle='--',
               label=f'Compression pure: {N_pure_comp:.0f} kN')
    plt.axvline(x=M_Ed, color='g', linestyle='--',
               label=f'Charge de calcul: M={M_Ed:.1f} kN·m')
    plt.axhline(y=N_Ed, color='g', linestyle='--',
               label=f'Charge de calcul: N={N_Ed} kN')

    plt.xlabel('Moment M (kN·m)')
    plt.ylabel('Effort axial N (kN)')
    plt.title('Diagramme d\'interaction N-M - Poteau 400×400mm')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis([0, max(M_values), 0, max(N_max_values)*1.1])

    plt.tight_layout()
    plt.savefig('column_interaction_diagram.png', dpi=150, bbox_inches='tight')
    plt.show()

    print(f"\nRésistance en compression pure : {N_pure_comp:.0f} kN")
    print(f"Réduction due au moment : {(N_pure_comp - max(N_max_values))/N_pure_comp*100:.1f}%")


if __name__ == "__main__":
    result, checks = column_design_example()
    column_interaction_diagram()

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("✓ Poteau dimensionné selon EC2")
    print("✓ Vérifications ELU et stabilité")
    print("✓ Diagramme d'interaction N-M tracé")
    print("✓ Méthode de recherche dichotomique pour capacité maximale")
    print("\nRéférence : Guide pratique EC2 - Dimensionnement des poteaux")
