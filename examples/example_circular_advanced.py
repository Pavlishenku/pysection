"""
Exemple avancé : Poteau circulaire avec ferraillage circulaire
Démontre l'utilisation de l'enrobage automatique
"""

from opensection import CircularSection, ConcreteEC2, SteelEC2, RebarGroup
from opensection import SectionSolver
from opensection.validation import SectionValidator, ValidationError
import numpy as np


def main():
    print("=" * 70)
    print("EXEMPLE AVANCE : POTEAU CIRCULAIRE")
    print("=" * 70)
    print()
    
    # === 1. DÉFINITION DE LA SECTION ===
    print("1. Section circulaire")
    diameter = 0.5  # 50 cm
    section = CircularSection(diameter=diameter, n_points=36)
    print(f"   Diamètre : {diameter*100:.0f} cm")
    print(f"   Aire : {section.properties.area*1e4:.2f} cm²")
    print()
    
    # === 2. MATÉRIAUX ===
    print("2. Matériaux")
    concrete = ConcreteEC2(fck=30)
    steel = SteelEC2(fyk=500)
    print(f"   Béton : C{int(concrete.fck)}/37 (fcd = {concrete.fcd:.2f} MPa)")
    print(f"   Acier : B{int(steel.fyk)} (fyd = {steel.fyd:.2f} MPa)")
    print()
    
    # === 3. FERRAILLAGE CIRCULAIRE AVEC ENROBAGE AUTOMATIQUE ===
    print("3. Ferraillage circulaire avec enrobage automatique")
    rebars = RebarGroup()
    
    # Ferraillage circulaire : 8HA16 avec enrobage de 4 cm
    n_bars = 8
    diameter_rebar = 0.016  # 16 mm
    cover = 0.04  # 4 cm
    
    rebars.add_circular_array_with_cover(
        n_bars=n_bars,
        diameter_rebar=diameter_rebar,
        diameter_section=diameter,
        cover=cover,
        start_angle=0  # Première barre à droite
    )
    
    print(f"   Configuration : {n_bars}HA{int(diameter_rebar*1000)}")
    print(f"   Enrobage : {cover*100:.0f} cm")
    print(f"   Aire totale acier : {rebars.total_area*1e4:.2f} cm²")
    print(f"   Taux géométrique : {rebars.total_area/section.properties.area*100:.2f}%")
    
    # Afficher positions des armatures
    print(f"\n   Positions des armatures (avec enrobage {cover*100:.0f} cm) :")
    for i, rebar in enumerate(rebars.rebars):
        angle = i * 360 / n_bars
        distance_center = np.sqrt(rebar.y**2 + rebar.z**2)
        print(f"      Barre {i+1}: angle={angle:5.1f}°, "
              f"distance centre={distance_center*100:.2f} cm")
    print()
    
    # === 4. VALIDATION ===
    print("4. Validation de la section")
    try:
        SectionValidator.validate_all(
            section, concrete, steel, rebars,
            N=1000, M_y=0, M_z=150
        )
        print("   [OK] Section validée avec succès !")
    except ValidationError as e:
        print(f"   [ERREUR] {e}")
        return
    print()
    
    # === 5. RÉSOLUTION ===
    print("5. Résolution du poteau")
    
    # Créer le solver
    solver = SectionSolver(section, concrete, steel, rebars, fiber_area=0.0001)
    print(f"   Nombre de fibres béton : {len(solver.fibers)}")
    print(f"   Nombre d'armatures : {len(solver.rebar_array)}")
    print()
    
    # Cas de charge 1 : Compression centrée
    print("   Cas 1 : Compression centrée")
    N1 = 1000  # kN
    result1 = solver.solve(N=N1, My=0, Mz=0, tol=1e-3, max_iter=100)
    
    print(f"      N = {N1} kN")
    print(f"      Convergence : {'OUI' if result1.converged else 'NON'}")
    if result1.converged:
        print(f"      Iterations : {result1.n_iter}")
        print(f"      epsilon_0 = {result1.epsilon_0*1000:.3f} ‰")
        print(f"      sigma_c_max = {result1.sigma_c_max:.2f} MPa")
        print(f"      sigma_s_max = {result1.sigma_s_max:.2f} MPa")
    print()
    
    # Cas de charge 2 : Flexion composée
    print("   Cas 2 : Flexion composée")
    N2 = 1000  # kN
    M2 = 150   # kN·m
    result2 = solver.solve(N=N2, My=0, Mz=M2, tol=1e-3, max_iter=100)
    
    print(f"      N = {N2} kN, M = {M2} kN·m")
    print(f"      Convergence : {'OUI' if result2.converged else 'NON'}")
    if result2.converged:
        print(f"      Iterations : {result2.n_iter}")
        print(f"      epsilon_0 = {result2.epsilon_0*1000:.3f} ‰")
        print(f"      chi_z = {result2.chi_z:.6e} rad/m")
        print(f"      sigma_c_max = {result2.sigma_c_max:.2f} MPa")
        print(f"      sigma_s_max = {result2.sigma_s_max:.2f} MPa")
        print(f"      Profondeur AN = {result2.neutral_axis_depth*100:.2f} cm")
    print()
    
    # === 6. VÉRIFICATIONS EC2 ===
    print("6. Vérifications Eurocode 2")
    from opensection.eurocodes import EC2Verification
    
    if result2.converged:
        checks = EC2Verification.check_ULS(result2, concrete.fcd, steel.fyd)
        
        print(f"   Béton : {checks['concrete_stress']['ratio']:.2%} "
              f"({'OK' if checks['concrete_stress']['ok'] else 'NOK'})")
        print(f"   Acier : {checks['steel_stress']['ratio']:.2%} "
              f"({'OK' if checks['steel_stress']['ok'] else 'NOK'})")
    print()
    
    # === 7. COMPARAISON AVEC/SANS ENROBAGE ===
    print("7. Impact de l'enrobage")
    
    # Sans enrobage (position théorique au bord)
    rebars_no_cover = RebarGroup()
    radius_no_cover = diameter / 2 - diameter_rebar / 2
    
    # Avec enrobage (calculé automatiquement)
    radius_with_cover = diameter / 2 - cover - diameter_rebar / 2
    
    print(f"   Rayon effectif sans enrobage : {radius_no_cover*100:.2f} cm")
    print(f"   Rayon effectif avec enrobage {cover*100:.0f}cm : "
          f"{radius_with_cover*100:.2f} cm")
    print(f"   Réduction du bras de levier : "
          f"{(radius_no_cover - radius_with_cover)*100:.2f} cm")
    print()
    
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"Poteau circulaire D={diameter*100:.0f}cm avec {n_bars}HA{int(diameter_rebar*1000)}")
    print(f"Enrobage automatique : {cover*100:.0f} cm")
    print(f"Solver : {'Converge' if result2.converged else 'Ne converge pas'}")
    if result2.converged:
        print(f"Contraintes OK : "
              f"Béton {result2.sigma_c_max:.1f}/{concrete.fcd:.1f} MPa, "
              f"Acier {result2.sigma_s_max:.1f}/{steel.fyd:.1f} MPa")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

