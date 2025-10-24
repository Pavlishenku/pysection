"""
Exemple d'utilisation de la base de validation analytique
Compare le solver numérique avec des solutions analytiques EC2
"""

from pysection import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup, SectionSolver
from pysection.validation.analytical_cases import ValidationDatabase
import numpy as np


def validate_solver_against_analytical():
    """
    Compare le solver numérique avec solutions analytiques
    """
    print("=" * 70)
    print("VALIDATION DU SOLVER SectionPy")
    print("Comparaison avec solutions analytiques Eurocode 2")
    print("=" * 70)
    print()
    
    # Charger la base de validation
    db = ValidationDatabase()
    
    print(f"Base de validation : {len(db.list_cases())} cas de test")
    print()
    
    results = {}
    
    # CAS 1 : COMPRESSION PURE
    print("-" * 70)
    print("CAS 1 : COMPRESSION CENTRÉE")
    print("-" * 70)
    
    case = db.get_case("rect_compression")
    geom = case["geometry"]
    reinf = case["reinforcement"]
    mat = case["materials"]
    sol_analytical = case["solution"]
    
    # Créer la section
    section = RectangularSection(width=geom["width"], height=geom["height"])
    concrete = ConcreteEC2(fck=mat["fck"])
    steel = SteelEC2(fyk=mat["fyk"])
    rebars = RebarGroup()
    
    # Armatures réparties
    As_per_bar = reinf["As_total"] / 4
    diameter = np.sqrt(4 * As_per_bar / np.pi)
    rebars.add_rebar(y=0.20, z=0.12, diameter=diameter, n=1)
    rebars.add_rebar(y=0.20, z=-0.12, diameter=diameter, n=1)
    rebars.add_rebar(y=-0.20, z=0.12, diameter=diameter, n=1)
    rebars.add_rebar(y=-0.20, z=-0.12, diameter=diameter, n=1)
    
    print(f"Section : {geom['width']*100}x{geom['height']*100} cm")
    print(f"Armatures : {reinf['As_total']*1e4:.1f} cm² (réparties)")
    print(f"Béton : C{int(mat['fck'])}/37")
    print()
    
    # Résoudre
    solver = SectionSolver(section, concrete, steel, rebars)
    result = solver.solve(N=sol_analytical.N, My=0, Mz=0, tol=1e-2, max_iter=100)
    
    print("Solution analytique EC2:")
    print(f"  N = {sol_analytical.N:.2f} kN")
    print(f"  epsilon_0 = {sol_analytical.epsilon_0*1000:.3f} ‰")
    print(f"  sigma_c = {sol_analytical.sigma_c_max:.2f} MPa")
    print()
    
    print("Solution numérique (SectionPy):")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'}")
    if result.converged:
        print(f"  Iterations : {result.n_iter}")
        print(f"  N = {result.N:.2f} kN")
        print(f"  epsilon_0 = {result.epsilon_0*1000:.3f} ‰")
        print(f"  sigma_c_max = {result.sigma_c_max:.2f} MPa")
        
        error_N = abs(result.N - sol_analytical.N) / abs(sol_analytical.N) * 100
        error_eps = abs(result.epsilon_0 - sol_analytical.epsilon_0) / abs(sol_analytical.epsilon_0) * 100 if sol_analytical.epsilon_0 != 0 else 0
        
        print()
        print(f"Écarts:")
        print(f"  N : {error_N:.2f}% {'[OK]' if error_N < case['tolerance']*100 else '[FAIL]'}")
        print(f"  epsilon_0 : {error_eps:.2f}%")
        
        results["compression"] = {
            "converged": True,
            "error_N": error_N,
            "ok": error_N < case['tolerance']*100
        }
    else:
        results["compression"] = {"converged": False, "ok": False}
    
    print()
    
    # CAS 2 : RÉGIME ÉLASTIQUE
    print("-" * 70)
    print("CAS 2 : RÉGIME ÉLASTIQUE (FAIBLES CHARGES)")
    print("-" * 70)
    
    case = db.get_case("rect_elastic")
    geom = case["geometry"]
    reinf = case["reinforcement"]
    mat = case["materials"]
    loads = case["loads"]
    sol_analytical = case["solution"]
    
    # Créer la section
    section = RectangularSection(width=geom["width"], height=geom["height"])
    concrete = ConcreteEC2(fck=mat["fck"])
    steel = SteelEC2(fyk=mat["fyk"])
    rebars = RebarGroup()
    
    # Armatures tendues
    d = geom["d"]
    y_tension = -(geom["height"]/2 - (geom["height"] - d))
    n_bars = int(reinf["As_tension"] / (np.pi * 0.016**2 / 4)) + 1
    rebars.add_rebar(y=y_tension, z=0.0, diameter=0.016, n=n_bars)
    
    print(f"Section : {geom['width']*100}x{geom['height']*100} cm")
    print(f"Charges : N = {loads['N']} kN, M = {loads['M']} kN·m")
    print()
    
    # Résoudre
    solver = SectionSolver(section, concrete, steel, rebars)
    result = solver.solve(N=loads["N"], My=0, Mz=loads["M"], tol=1e-2, max_iter=100)
    
    print("Solution analytique (Navier-Bernoulli):")
    print(f"  N = {sol_analytical.N:.2f} kN")
    print(f"  M = {sol_analytical.M:.2f} kN·m")
    print(f"  sigma_c_max = {sol_analytical.sigma_c_max:.2f} MPa")
    print()
    
    print("Solution numérique (SectionPy):")
    print(f"  Convergence : {'OUI' if result.converged else 'NON'}")
    if result.converged:
        print(f"  Iterations : {result.n_iter}")
        print(f"  N = {result.N:.2f} kN")
        print(f"  M_z = {result.Mz:.2f} kN·m")
        print(f"  sigma_c_max = {result.sigma_c_max:.2f} MPa")
        
        error_N = abs(result.N - loads["N"]) / abs(loads["N"]) * 100
        error_M = abs(result.Mz - loads["M"]) / abs(loads["M"]) * 100
        
        print()
        print(f"Écarts:")
        print(f"  N : {error_N:.2f}% {'[OK]' if error_N < case['tolerance']*100 else '[FAIL]'}")
        print(f"  M : {error_M:.2f}% {'[OK]' if error_M < case['tolerance']*100 else '[FAIL]'}")
        
        results["elastic"] = {
            "converged": True,
            "error_N": error_N,
            "error_M": error_M,
            "ok": error_N < case['tolerance']*100 and error_M < case['tolerance']*100
        }
    else:
        results["elastic"] = {"converged": False, "ok": False}
    
    print()
    
    # RÉSUMÉ
    print("=" * 70)
    print("RÉSUMÉ DE LA VALIDATION")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r.get("ok", False))
    
    for case_name, res in results.items():
        status = "[OK]" if res.get("ok", False) else "[FAIL]" if res.get("converged", False) else "[NO CONV]"
        print(f"  {case_name:20s} : {status}")
    
    print()
    print(f"Résultat : {passed}/{total} cas validés")
    
    if passed == total:
        print("\n[SUCCESS] Tous les cas de validation passent !")
        print("Le solver numérique reproduit correctement les solutions analytiques.")
    else:
        print(f"\n[INFO] {total-passed} cas à améliorer")
    
    print("=" * 70)


if __name__ == "__main__":
    validate_solver_against_analytical()

