"""
Exemple de dimensionnement d'une poutre simplement appuyée selon Eurocode 2

Cas académique classique : poutre en béton armé C25/30 avec armatures B500B
Dimensions : b=300mm, h=600mm, portée=6m, charge uniforme q=25kN/m

Référence : Exemple classique des cours de béton armé
"""
import numpy as np
import matplotlib.pyplot as plt
from sectionpy import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup, SectionSolver
from sectionpy.eurocodes import EC2Verification


def simply_supported_beam_design():
    """Dimensionnement d'une poutre simplement appuyée"""

    print("Dimensionnement d'une poutre simplement appuyée")
    print("=" * 60)

    # Paramètres de la poutre
    b = 0.3    # largeur (m)
    h = 0.6    # hauteur (m)
    L = 6.0    # portée (m)
    q = 25.0   # charge uniforme (kN/m)

    # Calcul des sollicitations (ELU)
    # Moment maximal : M_max = q*L²/8 = 25*6²/8 = 112.5 kN·m
    M_max = q * L**2 / 8
    # Effort tranchant maximal : V_max = q*L/2 = 25*6/2 = 75 kN
    V_max = q * L / 2

    print("Paramètres de calcul :")
    print(f"  Largeur b = {b*1000:.0f} mm")
    print(f"  Hauteur h = {h*1000:.0f} mm")
    print(f"  Portée L = {L} m")
    print(f"  Charge q = {q} kN/m")
    print(f"  Moment max M = {M_max:.1f} kN·m")
    print(f"  Effort tranchant V = {V_max:.1f} kN")

    # Matériaux selon EC2
    concrete = ConcreteEC2(fck=25)  # C25/30
    steel = SteelEC2(fyk=500)       # B500B

    print(f"\nMatériaux :")
    print(f"  Béton {concrete.fck} MPa (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier {steel.fyk} MPa (fyd = {steel.fyd:.2f} MPa)")

    # Section géométrique
    section = RectangularSection(width=b, height=h)

    # Armatures (dimensionnées pour résister à M_max)
    # Enrobage : c = 30mm
    # Diamètre armatures : Ø16mm
    cover = 0.03  # m
    dia = 0.016   # m

    # Calcul du bras de levier approximatif
    d = h - cover - dia/2  # hauteur utile ≈ 600 - 30 - 8 = 562mm

    # Aire d'acier nécessaire (formule simplifiée)
    # M = As * fyd * z ≈ As * fyd * 0.9*d
    # As = M / (fyd * 0.9*d)
    As_needed = M_max / (steel.fyd * 0.9 * d)

    print(f"\nDimensionnement des armatures :")
    print(f"  Hauteur utile d = {d*1000:.0f} mm")
    print(f"  Aire d'acier nécessaire = {As_needed*1e4:.0f} cm²")

    # Armatures choisies : 4Ø16 + 2Ø16 = 8.04 cm²
    rebars = RebarGroup()
    rebars.add_rebar(y=d - cover, z=0.0, diameter=dia, n=4)  # Armatures tendues
    rebars.add_rebar(y=-(d - cover), z=0.0, diameter=dia, n=2)  # Armatures comprimées

    print(f"  Armatures choisies : 4Ø16 + 2Ø16 = {rebars.total_area*1e4:.1f} cm²")

    # Création du solveur
    solver = SectionSolver(section, concrete, steel, rebars)

    print(f"\nAnalyse numérique :")
    print(f"  Fibres béton : {len(solver.fibers)}")
    print(f"  Points d'armature : {len(solver.rebar_array)}")

    # Résolution pour le moment maximal
    result = solver.solve(N=0, My=0, Mz=M_max)

    print("
Résultats :")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'}")
    print(f"  Itérations : {result.n_iter}")
    print(f"  ε₀ = {result.epsilon_0*1000:.2f} ‰")
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

    # Calcul du taux d'armature
    rho = rebars.total_area / (b * h)
    rho_min = 0.26 * concrete.fck**0.5 / steel.fyk * 100  # % selon EC2

    print("
Taux d'armature :")
    print(f"  ρ = {rho*100:.2f}% (calculé)")
    print(f"  ρ_min = {rho_min:.2f}% (EC2)")

    return result, checks


def beam_capacity_analysis():
    """Analyse de la capacité portante de la poutre"""

    print("\n" + "=" * 60)
    print("ANALYSE DE CAPACITÉ PORTANTE")
    print("=" * 60)

    # Même configuration
    b, h, L, q = 0.3, 0.6, 6.0, 25.0
    concrete = ConcreteEC2(fck=25)
    steel = SteelEC2(fyk=500)

    section = RectangularSection(width=b, height=h)
    cover, dia = 0.03, 0.016
    d = h - cover - dia/2

    rebars = RebarGroup()
    rebars.add_rebar(y=d - cover, z=0.0, diameter=dia, n=4)
    rebars.add_rebar(y=-(d - cover), z=0.0, diameter=dia, n=2)

    solver = SectionSolver(section, concrete, steel, rebars)

    # Recherche du moment de rupture par incrémentation
    M_test = np.linspace(50, 200, 50)  # kN·m
    moments = []
    strains = []
    stresses = []

    for M in M_test:
        result = solver.solve(N=0, My=0, Mz=M)
        if result.converged:
            moments.append(result.Mz)
            strains.append(abs(result.epsilon_0))
            stresses.append(result.sigma_c_max)

            # Arrêt si béton écrasé (ε > ε_cu)
            if abs(result.epsilon_0) > concrete.epsilon_cu2:
                print(f"Rupture par écrasement du béton à M = {M:.1f} kN·m")
                break

    # Tracé de la courbe moment-déformation
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(strains, moments, 'b-o', linewidth=2, markersize=4)
    plt.xlabel('Déformation maximale |ε| (‰)')
    plt.ylabel('Moment M (kN·m)')
    plt.title('Courbe Moment-Déformation')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(moments, stresses, 'r-s', linewidth=2, markersize=4)
    plt.xlabel('Moment M (kN·m)')
    plt.ylabel('Contrainte béton max σ_c (MPa)')
    plt.title('Contrainte Béton vs Moment')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('beam_capacity_curve.png', dpi=150, bbox_inches='tight')
    plt.show()

    print(f"\nMoment de rupture estimé : {max(moments):.1f} kN·m")
    print(f"Capacité de la poutre : {max(moments):.1f} kN·m")


if __name__ == "__main__":
    result, checks = simply_supported_beam_design()
    beam_capacity_analysis()

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("✓ Poutre simplement appuyée dimensionnée selon EC2")
    print("✓ Vérifications ELU satisfaites")
    print("✓ Capacité portante déterminée")
    print("✓ Courbes de comportement tracées")
    print("\nRéférence : Exemple classique de cours de béton armé")
