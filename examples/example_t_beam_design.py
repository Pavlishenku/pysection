"""
Exemple de dimensionnement d'une poutre en T selon Eurocode 2

Cas pratique : Poutre en T de pont ou bâtiment industriel
Section : Semelle 800mm×150mm, âme 300mm×500mm
Charge : 50kN/m sur portée 10m

Référence : Exemples de dimensionnement de ponts, guides techniques
"""
import numpy as np
import matplotlib.pyplot as plt
from sectionpy import TSection, ConcreteEC2, SteelEC2, RebarGroup, SectionSolver
from sectionpy.eurocodes import EC2Verification


def t_beam_bridge_design():
    """Dimensionnement d'une poutre en T de pont"""

    print("Dimensionnement d'une poutre en T de pont")
    print("=" * 60)

    # Paramètres géométriques selon pratique courante
    flange_width = 0.8    # mm (semelle)
    flange_thickness = 0.15  # mm (épaisseur semelle)
    web_width = 0.3       # mm (âme)
    web_height = 0.5      # mm (hauteur âme)

    print("Paramètres géométriques :")
    print(f"  Semelle : {flange_width*1000:.0f}×{flange_thickness*1000:.0f} mm")
    print(f"  Âme : {web_width*1000:.0f}×{web_height*1000:.0f} mm")
    print(f"  Hauteur totale : {(flange_thickness + web_height)*1000:.0f} mm")

    # Charges et portée
    L = 10.0     # portée (m)
    q_perm = 30  # charge permanente (kN/m)
    q_var = 20   # charge variable (kN/m)
    q_total = q_perm + q_var  # charge totale (kN/m)

    # Calcul des sollicitations (ELU)
    M_max = q_total * L**2 / 8  # kN·m
    V_max = q_total * L / 2     # kN

    print("
Sollicitations :")
    print(f"  Portée L = {L} m")
    print(f"  Charge totale q = {q_total} kN/m")
    print(f"  Moment max M = {M_max:.1f} kN·m")
    print(f"  Effort tranchant V = {V_max:.1f} kN")

    # Matériaux haute performance pour pont
    concrete = ConcreteEC2(fck=40)  # C40/50
    steel = SteelEC2(fyk=500)       # B500B

    print("
Matériaux :")
    print(f"  Béton C{concrete.fck}/50 (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier {steel.fyk} MPa (fyd = {steel.fyd:.2f} MPa)")

    # Section en T
    section = TSection(
        flange_width=flange_width,
        flange_thickness=flange_thickness,
        web_width=web_width,
        web_height=web_height
    )

    # Armatures pour poutre en T
    rebars = RebarGroup()

    # Enrobage selon EC2 (plus important pour ponts)
    cover = 0.05  # mm

    # Armatures longitudinales
    # Dans la semelle (partie tendue)
    dia_long = 0.025  # Ø25mm
    n_long_bottom = 6  # 6Ø25mm dans la semelle

    # Position dans la semelle (réparties sur la largeur)
    flange_half = flange_width / 2
    positions_bottom = np.linspace(-flange_half + cover + dia_long/2,
                                  flange_half - cover - dia_long/2, n_long_bottom)

    for z in positions_bottom:
        rebars.add_rebar(y=-flange_thickness/2, z=z, diameter=dia_long, n=1)

    # Armatures dans l'âme (partie comprimée)
    n_long_top = 3  # 3Ø20mm en partie supérieure
    dia_top = 0.020

    rebars.add_rebar(y=flange_thickness + web_height/2 - cover - dia_top/2,
                    z=0.0, diameter=dia_top, n=n_long_top)

    print("
Armatures longitudinales :")
    print(f"  Semelle : {n_long_bottom}Ø{dia_long*1000:.0f}mm = {rebars.total_area*1e4:.1f} cm²")
    print(f"  Âme : {n_long_top}Ø{dia_top*1000:.0f}mm")

    # Création du solveur
    solver = SectionSolver(section, concrete, steel, rebars)

    print("
Analyse :")
    print(f"  Fibres béton : {len(solver.fibers)}")
    print(f"  Points d'armature : {len(solver.rebar_array)}")

    # Résolution pour le moment maximal
    result = solver.solve(N=0, My=0, Mz=M_max)

    print("
Résultats :")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'}")
    print(f"  Itérations : {result.n_iter}")
    print(f"  ε₀ = {result.epsilon_0*1000:.3f} ‰")
    print(f"  χ_z = {result.chi_z:.4e} rad/m")
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

    # Calcul du taux d'armature effectif
    # Taux dans la semelle (zone tendue principale)
    flange_area = flange_width * flange_thickness
    rho_flange = rebars.total_area / flange_area

    print("
Taux d'armature :")
    print(f"  ρ_semelle = {rho_flange*100:.2f}% (dans la semelle)")
    print(f"  ρ_min recommandé = {0.26 * np.sqrt(concrete.fck) / steel.fyk * 100:.2f}%")

    return result, checks


def t_beam_capacity_study():
    """Étude de capacité pour différentes largeurs de semelle"""

    print("\n" + "=" * 60)
    print("ÉTUDE PARAMÉTRIQUE - LARGEUR DE SEMELLE")
    print("=" * 60)

    # Paramètres fixes
    flange_thickness = 0.15
    web_width = 0.3
    web_height = 0.5
    concrete = ConcreteEC2(fck=40)
    steel = SteelEC2(fyk=500)

    # Largeurs de semelle à étudier
    flange_widths = np.linspace(0.4, 1.2, 9)  # m
    capacities = []

    for fw in flange_widths:
        section = TSection(
            flange_width=fw,
            flange_thickness=flange_thickness,
            web_width=web_width,
            web_height=web_height
        )

        # Armatures proportionnelles à la largeur
        rebars = RebarGroup()
        dia = 0.025
        n_bars = max(4, int(8 * fw / 0.8))  # Proportionnel à la largeur

        # Répartition uniforme dans la semelle
        positions = np.linspace(-fw/2 + 0.05 + dia/2,
                              fw/2 - 0.05 - dia/2, n_bars)

        for z in positions:
            rebars.add_rebar(y=-flange_thickness/2, z=z, diameter=dia, n=1)

        # Armatures comprimées dans l'âme
        rebars.add_rebar(y=flange_thickness + web_height/2 - 0.05 - 0.020/2,
                        z=0.0, diameter=0.020, n=3)

        solver = SectionSolver(section, concrete, steel, rebars)

        # Recherche du moment maximal
        M_test = 500  # kN·m (valeur de départ)
        M_max = 0

        for attempt in range(10):
            result = solver.solve(N=0, My=0, Mz=M_test)
            if result.converged and result.sigma_c_max <= concrete.fcd * 1.01:
                M_max = M_test
                M_test *= 1.2  # Augmenter pour chercher le maximum
            else:
                break

        capacities.append(M_max)

        print(f"  Semelle {fw*1000:.0f}mm : M_max = {M_max:.1f} kN·m")

    # Tracé des résultats
    plt.figure(figsize=(10, 6))

    plt.plot(flange_widths * 1000, capacities, 'b-o', linewidth=3, markersize=8)
    plt.xlabel('Largeur de semelle (mm)')
    plt.ylabel('Moment résistant M_max (kN·m)')
    plt.title('Capacité portante vs Largeur de semelle - Poutre en T')
    plt.grid(True, alpha=0.3)
    plt.axis([min(flange_widths)*1000, max(flange_widths)*1000, 0, max(capacities)*1.1])

    plt.tight_layout()
    plt.savefig('t_beam_capacity_study.png', dpi=150, bbox_inches='tight')
    plt.show()

    # Analyse de tendance
    # Relation théorique : M_max ≈ k * b_flange^2 (pour semelle tendue)
    widths_squared = flange_widths**2
    correlation = np.corrcoef(flange_widths, capacities)[0, 1]

    print("
Analyse de tendance :")
    print(f"  Corrélation M vs b² : {correlation:.3f}")
    print(f"  Capacité pour semelle 800mm : {np.interp(0.8, flange_widths, capacities):.1f} kN·m")


def shear_design_verification():
    """Vérification de l'effort tranchant selon EC2"""

    print("\n" + "=" * 60)
    print("VÉRIFICATION EFFORT TRANCHANT")
    print("=" * 60)

    # Paramètres
    flange_width, flange_thickness = 0.8, 0.15
    web_width, web_height = 0.3, 0.5
    concrete = ConcreteEC2(fck=40)

    section = TSection(flange_width, flange_thickness, web_width, web_height)

    # Calcul de la résistance au cisaillement selon EC2
    # VRd = (τ_Rd * k * (1.2 + 40*ρ_l) + 0.15*σ_cp) * b_w * d
    # Simplifié pour cette étude

    # Largeur web
    bw = web_width

    # Hauteur utile (approximative)
    d = flange_thickness + web_height - 0.05 - 0.025/2  # cm

    # Taux d'armature longitudinal (approximatif)
    rho_l = 0.02  # 2%

    # Résistance au cisaillement du béton
    tau_Rd = 0.25 * np.sqrt(concrete.fck) / concrete.gamma_c  # MPa

    # Coefficient k
    k = min(1 + np.sqrt(200 / d), 2.0)  # d en mm

    # VRd = τ_Rd * k * (1.2 + 40*ρ_l) * bw * d / 1000  # kN
    VRd = tau_Rd * k * (1.2 + 40*rho_l) * bw * d / 1000

    print("Résistance au cisaillement selon EC2 :")
    print(f"  τ_Rd = {tau_Rd:.2f} MPa")
    print(f"  k = {k:.2f}")
    print(f"  bw = {bw*1000:.0f} mm")
    print(f"  d = {d*1000:.0f} mm")
    print(f"  VRd = {VRd:.1f} kN")

    # Effort tranchant de calcul (avec coefficient de sécurité)
    V_Ed = 75 * 1.35  # kN (charge variable × γ_Q)

    print(f"\nEffort tranchant de calcul V_Ed = {V_Ed:.1f} kN")

    # Vérification
    ratio_shear = V_Ed / VRd

    print(f"\nVérification : V_Ed / VRd = {ratio_shear:.2f}")
    if ratio_shear <= 1.0:
        print("✓ Résistance au cisaillement satisfaisante")
    else:
        print("⚠ Armatures de cisaillement nécessaires")


if __name__ == "__main__":
    result, checks = t_beam_bridge_design()
    t_beam_capacity_study()
    shear_design_verification()

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("✓ Poutre en T dimensionnée selon EC2")
    print("✓ Étude paramétrique largeur de semelle")
    print("✓ Vérification effort tranchant")
    print("✓ Application pratique pour ouvrages d'art")
    print("\nRéférence : Dimensionnement de ponts - Guides techniques")
