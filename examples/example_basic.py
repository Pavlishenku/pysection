"""
Exemple basique d'utilisation d'SectionPy
"""
import numpy as np
from sectionpy import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup, SectionSolver


def main():
    print("SectionPy - Exemple de calcul de section")
    print("=" * 60)
    
    # Définir la géométrie
    section = RectangularSection(width=0.3, height=0.5)
    print(f"\nSection: {section.width}m x {section.height}m")
    
    # Matériaux
    concrete = ConcreteEC2(fck=30)
    steel = SteelEC2(fyk=500)
    print(f"Béton: C30/37 (fcd = {concrete.fcd:.2f} MPa)")
    print(f"Acier: B500B (fyd = {steel.fyd:.2f} MPa)")
    
    # Armatures (y: vertical, z: horizontal)
    rebars = RebarGroup()
    rebars.add_rebar(y=0.20, z=0.0, diameter=0.020, n=3)  # 3HA20 haut
    rebars.add_rebar(y=-0.20, z=0.0, diameter=0.016, n=2)   # 2HA16 bas
    print(f"\nArmatures: {rebars.n_rebars} barres, As = {rebars.total_area*1e4:.2f} cm²")
    
    # Créer le solveur
    solver = SectionSolver(section, concrete, steel, rebars)
    print(f"Fibres béton: {len(solver.fibers)}")
    
    # Résoudre pour N et M
    N = 500  # kN
    M = 100  # kN·m
    
    print(f"\nSollicitations: N = {N} kN, M = {M} kN·m")
    print("\nRésolution...")
    
    result = solver.solve(N=N, My=0, Mz=M, tol=1e-3, max_iter=100)
    
    print(f"\nRÉSULTATS:")
    print(f"  Convergence: {'OUI' if result.converged else 'NON'}")
    print(f"  Itérations: {result.n_iter}")
    print(f"  e0 = {result.epsilon_0*1000:.3f} ‰")
    print(f"  ?_z = {result.chi_z:.6e} rad/m")
    print(f"  s_c,max = {result.sigma_c_max:.2f} MPa")
    print(f"  s_s,max = {result.sigma_s_max:.2f} MPa")
    print(f"  Profondeur AN = {result.neutral_axis_depth:.3f} m")
    
    # Vérifications EC2
    from sectionpy.eurocodes import EC2Verification
    
    checks_uls = EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
    
    print(f"\nVÉRIFICATIONS ELU:")
    print(f"  Béton: {checks_uls['concrete_stress']['ratio']:.2%} - {'OK' if checks_uls['concrete_stress']['ok'] else 'NOK'}")
    print(f"  Acier: {checks_uls['steel_stress']['ratio']:.2%} - {'OK' if checks_uls['steel_stress']['ok'] else 'NOK'}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
