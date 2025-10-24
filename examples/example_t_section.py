"""
Exemple : Poutre en T en béton armé
"""
import opensection as ps


def main():
    print("=" * 70)
    print("EXEMPLE : POUTRE EN T EN BETON ARME")
    print("=" * 70)
    print()
    
    # Geometrie
    flange_width = 0.80  # 80 cm (table de compression)
    flange_thickness = 0.12  # 12 cm
    web_width = 0.25  # 25 cm (ame)
    web_height = 0.48  # 48 cm
    
    section = oc.TSection(
        flange_width=flange_width,
        flange_thickness=flange_thickness,
        web_width=web_width,
        web_height=web_height
    )
    
    props = section.properties
    print(f"Section en T :")
    print(f"  Table : {flange_width*100:.0f} x {flange_thickness*100:.0f} cm")
    print(f"  Ame : {web_width*100:.0f} x {web_height*100:.0f} cm")
    print(f"  Aire totale : {props.area*1e4:.1f} cm2")
    print(f"  Centroide : y={props.centroid[0]*100:.2f} cm, z={props.centroid[1]*100:.2f} cm")
    print()
    
    # Materiaux
    concrete = oc.ConcreteEC2(fck=30)
    steel = oc.SteelEC2(fyk=500)
    print(f"Materiaux :")
    print(f"  Beton C30/37 : fcd = {concrete.fcd:.2f} MPa")
    print(f"  Acier B500B : fyd = {steel.fyd:.2f} MPa")
    print()
    
    # Armatures tendues (en bas)
    rebars = oc.RebarGroup()
    rebars.add_linear_array(
        y1=-web_width/2 + 0.04,
        z1=-web_height + 0.04,
        y2=web_width/2 - 0.04,
        z2=-web_height + 0.04,
        n=5,
        diameter=0.025
    )
    
    # Armatures comprimees (en haut)
    rebars.add_linear_array(
        y1=-web_width/2 + 0.04,
        z1=flange_thickness - 0.04,
        y2=web_width/2 - 0.04,
        z2=flange_thickness - 0.04,
        n=3,
        diameter=0.016
    )
    
    print(f"Armatures :")
    print(f"  Tendues : 5 HA25 (en bas)")
    print(f"  Comprimees : 3 HA16 (en haut)")
    print(f"  As total = {rebars.total_area*1e4:.2f} cm2")
    print()
    
    # Sollicitations (flexion simple)
    N = 0    # Pas d'effort normal
    M = 250  # kN.m
    
    print(f"Sollicitations :")
    print(f"  N = {N:.0f} kN")
    print(f"  M = {M:.0f} kN.m")
    print()
    
    # Analyse
    print("Analyse en cours...")
    solver = oc.SectionSolver(section, concrete, steel, rebars)
    print(f"  Maillage : {len(solver.fibers)} fibres de beton")
    print()
    
    result = solver.solve(N=N, My=0, Mz=M)
    
    print("RESULTATS :")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'} ({result.n_iter} iterations)")
    print(f"  Deformation axiale : {result.epsilon_0*1000:.3f} permil")
    print(f"  Courbure : {result.chi_z:.6e} rad/m")
    print(f"  Contrainte beton max : {result.sigma_c_max:.2f} MPa")
    print(f"  Contrainte acier max : {result.sigma_s_max:.2f} MPa")
    
    if result.converged:
        depth = result.neutral_axis_depth
        print(f"  Profondeur axe neutre : {depth*100:.2f} cm")
    
    print()
    
    # Verifications
    checks = oc.EC2Verification.check_ULS(result, concrete.fcd, steel.fyd)
    print("VERIFICATIONS EC2 :")
    print(f"  Beton : {checks['concrete_stress']['ratio']*100:.1f}% - {'OK' if checks['concrete_stress']['ok'] else 'NON OK'}")
    print(f"  Acier : {checks['steel_stress']['ratio']*100:.1f}% - {'OK' if checks['steel_stress']['ok'] else 'NON OK'}")
    print()
    
    print("=" * 70)


if __name__ == "__main__":
    main()

