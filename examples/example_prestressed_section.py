"""
Exemple de section précontrainte selon Eurocode 2

Cas académique : Poutre précontrainte avec torons
Section : 200×400mm, précontrainte par 4 torons Ø15mm

Référence : CEB-FIP Model Code 1990, exemples de précontrainte
"""
import numpy as np
import matplotlib.pyplot as plt
from opensection import RectangularSection, ConcreteEC2, PrestressingSteelEC2, RebarGroup, SectionSolver


def prestressed_beam_example():
    """Analyse d'une section précontrainte"""

    print("Analyse d'une section précontrainte")
    print("=" * 60)

    # Paramètres géométriques
    b = 0.2    # largeur (m)
    h = 0.4    # hauteur (m)

    print("Paramètres géométriques :")
    print(f"  Section : {b*1000:.0f}×{h*1000:.0f} mm")

    # Matériaux
    concrete = ConcreteEC2(fck=35)  # C35/45 pour précontrainte
    steel_reinf = SteelEC2(fyk=500)  # Armatures passives B500B

    # Acier de précontrainte (torons selon EN 10138)
    # Torons Y1860S7 (1860 MPa, 7 fils)
    prestress_steel = PrestressingSteelEC2(fp01k=1500)  # fp0.1k = 1500 MPa

    print("
Matériaux :")
    print(f"  Béton {concrete.fck} MPa (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier passif {steel_reinf.fyk} MPa (fyd = {steel_reinf.fyd:.2f} MPa)")
    print(f"  Précontrainte fp0.1k = {prestress_steel.fp01k} MPa")

    # Section géométrique
    section = RectangularSection(width=b, height=h)

    # Câbles de précontrainte
    # 4 torons Ø15mm en position parabolique
    n_strands = 4
    dia_strand = 0.015  # m
    Ap_strand = np.pi * (dia_strand/2)**2  # aire d'un toron

    # Position des torons (au 1/3 de la hauteur)
    y_strands = h/3  # position des torons

    # Précontrainte initiale
    P0 = 0.8 * prestress_steel.fp01k * Ap_strand * n_strands  # kN (80% fp0.1k)
    sigma_p0 = P0 / (Ap_strand * n_strands)  # MPa

    print("
Précontrainte :")
    print(f"  Torons : {n_strands}Ø{dia_strand*1000:.0f}mm")
    print(f"  Aire par toron : {Ap_strand*1e4:.1f} cm²")
    print(f"  Force initiale P₀ = {P0:.0f} kN")
    print(f"  Contrainte initiale σₚ₀ = {sigma_p0:.0f} MPa")

    # Pertes de précontrainte (approximation)
    # Perte instantanée : 15% (frottement, glissement, déformation)
    # Perte différée : 10% (fluage, retrait, relaxation)
    perte_instantanee = 0.15
    perte_differee = 0.10
    perte_totale = perte_instantanee + perte_differee * (1 - perte_instantanee)

    P_final = P0 * (1 - perte_totale)

    print("
Pertes de précontrainte :")
    print(f"  Perte instantanée : {perte_instantanee*100:.0f}%")
    print(f"  Perte différée : {perte_differee*100:.0f}%")
    print(f"  Perte totale : {perte_totale*100:.1f}%")
    print(f"  Force finale P∞ = {P_final:.0f} kN")

    # Armatures passives (minimum selon EC2)
    # Taux d'armature minimum : ρ_min = 0.26 * fctm / fyk ≥ 0.0013 * b*h
    rho_min = max(0.26 * np.sqrt(concrete.fck) / steel_reinf.fyk, 0.0013)
    As_min = rho_min * b * h

    rebars = RebarGroup()
    # 2 armatures Ø12mm en partie tendue
    rebars.add_rebar(y=-0.15, z=0.0, diameter=0.012, n=2)

    print("
Armatures passives :")
    print(f"  Taux minimum ρ_min = {rho_min*100:.3f}%")
    print(f"  As_min = {As_min*1e4:.1f} cm²")
    print(f"  Armatures : 2Ø12mm = {rebars.total_area*1e4:.1f} cm²")

    # Analyse de la section sous précontrainte seule
    print("
Analyse précontrainte seule :")

    # Créer solveur sans armatures passives pour voir l'effet précontrainte
    solver_prestress = SectionSolver(section, concrete, prestress_steel, RebarGroup())

    # Simulation de la précontrainte
    # Les torons sont modélisés comme des armatures avec contrainte initiale
    # Dans la pratique, il faudrait un modèle plus sophistiqué avec pertes

    # Pour simplifier, on applique directement la force de précontrainte
    # comme un effort normal négatif (compression)
    result_prestress = solver_prestress.solve(N=-P_final, My=0, Mz=0)

    print("  Convergence : " + ("OUI" if result_prestress.converged else "NON"))
    print(f"  ε₀ = {result_prestress.epsilon_0*1000:.2f} ‰")
    print(f"  σ_c,max = {result_prestress.sigma_c_max:.2f} MPa")

    # Analyse avec charges de service
    print("
Analyse charges de service :")

    # Charges de service : q_serv = 15 kN/m sur portée 8m
    # Moment de service : M_serv = q_serv * L²/8 = 15*8²/8 = 120 kN·m
    M_serv = 120  # kN·m

    # Effort normal dû aux charges permanentes (estimation)
    N_perm = 50   # kN (poids propre + finitions)

    # Combinaison quasi-permanente : précontrainte + charges perm
    result_service = solver_prestress.solve(N=-P_final + N_perm, My=0, Mz=M_serv)

    print(f"  Moment de service M = {M_serv} kN·m")
    print(f"  Effort permanent N_perm = {N_perm} kN")
    print(f"  Effort total = -P∞ + N_perm = {-P_final + N_perm:.0f} kN")
    print("  Convergence : " + ("OUI" if result_service.converged else "NON"))
    print(f"  ε₀ = {result_service.epsilon_0*1000:.2f} ‰")
    print(f"  σ_c,max = {result_service.sigma_c_max:.2f} MPa")

    # Vérification ouverture fissures (simplifiée)
    # L'ouverture de fissures ne doit pas dépasser w_max = 0.3mm
    # Cette vérification nécessiterait un modèle plus complet

    return result_prestress, result_service


def prestress_loss_study():
    """Étude de l'influence des pertes de précontrainte"""

    print("\n" + "=" * 60)
    print("ÉTUDE DES PERTES DE PRÉCONTRAINTE")
    print("=" * 60)

    # Configuration de base
    b, h = 0.2, 0.4
    concrete = ConcreteEC2(fck=35)
    section = RectangularSection(width=b, height=h)

    prestress_steel = PrestressingSteelEC2(fp01k=1500)
    dia_strand, n_strands = 0.015, 4
    Ap_strand = np.pi * (dia_strand/2)**2
    P0 = 0.8 * prestress_steel.fp01k * Ap_strand * n_strands

    # Différents scénarios de pertes
    scenarios = {
        'Aucune perte': 0.0,
        'Pertes instantanées seulement': 0.15,
        'Pertes EC2 typiques': 0.25,
        'Pertes élevées': 0.35
    }

    results = {}

    for scenario, perte_totale in scenarios.items():
        P_final = P0 * (1 - perte_totale)
        solver = SectionSolver(section, concrete, prestress_steel, RebarGroup())

        # Moment de service
        result = solver.solve(N=-P_final, My=0, Mz=120)

        if result.converged:
            results[scenario] = {
                'perte': perte_totale * 100,
                'P_final': P_final,
                'epsilon_0': result.epsilon_0,
                'sigma_c_max': result.sigma_c_max
            }

    # Tracé des résultats
    scenarios_list = list(results.keys())
    pertes = [results[s]['perte'] for s in scenarios_list]
    epsilons = [results[s]['epsilon_0'] * 1000 for s in scenarios_list]  # ‰
    sigmas = [results[s]['sigma_c_max'] for s in scenarios_list]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Déformation vs pertes
    ax1.bar(scenarios_list, epsilons, color='skyblue', alpha=0.8)
    ax1.set_ylabel('Déformation ε₀ (‰)')
    ax1.set_title('Déformation axiale vs Pertes')
    ax1.tick_params(axis='x', rotation=45)

    # Contrainte vs pertes
    ax2.bar(scenarios_list, sigmas, color='lightcoral', alpha=0.8)
    ax2.set_ylabel('Contrainte béton max σ_c (MPa)')
    ax2.set_title('Contrainte béton vs Pertes')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('prestress_losses_study.png', dpi=150, bbox_inches='tight')
    plt.show()

    # Affichage des résultats
    print("\nRésultats de l'étude :")
    print(f"{'Scénario':<25} {'Pertes':<8} {'ε₀':<8} {'σ_c':<8}")
    print("-" * 50)
    for scenario in scenarios_list:
        r = results[scenario]
        print(f"{scenario:<25} {r['perte']:<8.1f} {r['epsilon_0']*1000:<8.2f} {r['sigma_c_max']:<8.2f}")


if __name__ == "__main__":
    result_prestress, result_service = prestressed_beam_example()
    prestress_loss_study()

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("✓ Section précontrainte analysée selon EC2")
    print("✓ Effet des pertes de précontrainte étudié")
    print("✓ Comparaison précontrainte seule vs charges de service")
    print("✓ Étude paramétrique des pertes")
    print("\nRéférence : CEB-FIP Model Code 1990 - Exemples de précontrainte")
