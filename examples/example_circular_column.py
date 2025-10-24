"""
Exemple : Poteau circulaire en béton armé
"""
import sectionpy as sp


def main():
    print("=" * 70)
    print("EXEMPLE : POTEAU CIRCULAIRE EN BETON ARME")
    print("=" * 70)
    print()
    
    # Geometrie
    diameter = 0.40  # 40 cm
    section = oc.CircularSection(diameter=diameter)
    print(f"Section circulaire : D = {diameter*100:.0f} cm")
    print(f"Aire : {section.properties.area*1e4:.2f} cm2")
    print()
    
    # Materiaux
    concrete = oc.ConcreteEC2(fck=25)  # C25/30
    steel = oc.SteelEC2(fyk=500)  # B500B
    print(f"Beton : C25/30")
    print(f"  fck = {concrete.fck:.1f} MPa")
    print(f"  fcd = {concrete.fcd:.2f} MPa")
    print(f"  Ecm = {concrete.Ecm:.0f} MPa")
    print()
    print(f"Acier : B500B")
    print(f"  fyk = {steel.fyk:.1f} MPa")
    print(f"  fyd = {steel.fyd:.2f} MPa")
    print(f"  Es = {steel.Es:.0f} MPa")
    print()
    
    # Armatures - 8 barres Ø16 en peripherie
    rebars = oc.RebarGroup()
    rebars.add_circular_array(
        center_y=0.0,
        center_z=0.0,
        radius=diameter/2 - 0.04,  # enrobage 4 cm
        n=8,
        diameter=0.016
    )
    print(f"Armatures : 8 HA16 en peripherie")
    print(f"  As = {rebars.total_area*1e4:.2f} cm2")
    print(f"  Taux d'armature : {rebars.total_area/section.properties.area*100:.2f} %")
    print()
    
    # Sollicitations
    N = 800  # kN (compression)
    M = 50   # kN.m
    
    print(f"Sollicitations :")
    print(f"  N = {N:.0f} kN (compression)")
    print(f"  M = {M:.0f} kN.m")
    print()
    
    # Analyse
    print("Analyse en cours...")
    solver = oc.SectionSolver(section, concrete, steel, rebars, fiber_area=0.00005)
    print(f"  Maillage : {len(solver.fibers)} fibres de beton")
    print()
    
    result = solver.solve(N=N, My=0, Mz=M, tol=1e-4)
    
    print("RESULTATS :")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'} ({result.n_iter} iterations)")
    print(f"  Deformation axiale : {result.epsilon_0*1000:.3f} permil")
    print(f"  Courbure : {result.chi_z:.6e} rad/m")
    print(f"  Contrainte beton max : {result.sigma_c_max:.2f} MPa")
    print(f"  Contrainte acier max : {result.sigma_s_max:.2f} MPa")
    print()
    
    # Verifications EC2
    checks = oc.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
    print("VERIFICATIONS EC2 (ELU) :")
    print(f"  Beton : {checks['concrete_stress']['ratio']*100:.1f}% - {'OK' if checks['concrete_stress']['ok'] else 'NON OK'}")
    print(f"  Acier : {checks['steel_stress']['ratio']*100:.1f}% - {'OK' if checks['steel_stress']['ok'] else 'NON OK'}")
    print()
    
    print("=" * 70)


if __name__ == "__main__":
    main()

