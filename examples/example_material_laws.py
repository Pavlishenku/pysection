"""
Exemple : Visualisation des lois de comportement des materiaux
"""
import numpy as np
import pysection as ps

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("matplotlib non disponible - graphiques desactives")


def plot_concrete_law():
    """Trace la loi sigma-epsilon du beton"""
    if not HAS_MATPLOTLIB:
        return
    
    print("Trace de la loi beton EC2...")
    
    # Creer plusieurs betons
    c25 = oc.ConcreteEC2(fck=25)
    c30 = oc.ConcreteEC2(fck=30)
    c50 = oc.ConcreteEC2(fck=50)
    
    # Plage de deformations
    epsilon = np.linspace(0, 0.0045, 200)
    
    # Calculer les contraintes
    sigma_c25 = c25.stress_vectorized(epsilon)
    sigma_c30 = c30.stress_vectorized(epsilon)
    sigma_c50 = c50.stress_vectorized(epsilon)
    
    # Tracer
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon*1000, sigma_c25, 'b-', label='C25/30', linewidth=2)
    plt.plot(epsilon*1000, sigma_c30, 'g-', label='C30/37', linewidth=2)
    plt.plot(epsilon*1000, sigma_c50, 'r-', label='C50/60', linewidth=2)
    
    plt.xlabel('Deformation [permil]')
    plt.ylabel('Contrainte [MPa]')
    plt.title('Loi de comportement du beton (EC2)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('concrete_law.png', dpi=150)
    print("  -> Graphique sauvegarde : concrete_law.png")
    plt.close()


def plot_steel_law():
    """Trace la loi sigma-epsilon de l'acier"""
    if not HAS_MATPLOTLIB:
        return
    
    print("Trace de la loi acier EC2...")
    
    # Creer acier avec et sans ecrouissage
    steel_plastic = oc.SteelEC2(fyk=500, include_hardening=False)
    steel_hardening = oc.SteelEC2(fyk=500, include_hardening=True, k=0.01)
    
    # Plage de deformations (tension et compression)
    epsilon = np.linspace(-0.02, 0.02, 400)
    
    # Calculer les contraintes
    sigma_plastic = steel_hardening.stress_vectorized(epsilon)
    sigma_hardening = steel_hardening.stress_vectorized(epsilon)
    
    # Tracer
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon*1000, sigma_plastic, 'b-', label='Elasto-plastique', linewidth=2)
    plt.plot(epsilon*1000, sigma_hardening, 'r--', label='Avec ecrouissage', linewidth=2)
    
    plt.axhline(y=steel_plastic.fyd, color='gray', linestyle=':', alpha=0.5)
    plt.axhline(y=-steel_plastic.fyd, color='gray', linestyle=':', alpha=0.5)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.xlabel('Deformation [permil]')
    plt.ylabel('Contrainte [MPa]')
    plt.title('Loi de comportement de l\'acier d\'armature (EC2)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('steel_law.png', dpi=150)
    print("  -> Graphique sauvegarde : steel_law.png")
    plt.close()


def print_material_properties():
    """Affiche les proprietes des materiaux"""
    print("=" * 70)
    print("PROPRIETES DES MATERIAUX")
    print("=" * 70)
    print()
    
    # Betons
    print("BETONS EC2 :")
    print()
    for fck in [20, 25, 30, 35, 40, 45, 50, 60]:
        c = oc.ConcreteEC2(fck=fck)
        print(f"  C{fck}/{{fck+8 if fck<=50 else fck+10}} :")
        print(f"    fck = {c.fck:.1f} MPa")
        print(f"    fcd = {c.fcd:.2f} MPa")
        print(f"    Ecm = {c.Ecm:.0f} MPa")
        print(f"    epsilon_c2 = {c.epsilon_c2*1000:.2f} permil")
        print(f"    epsilon_cu2 = {c.epsilon_cu2*1000:.2f} permil")
        print()
    
    # Aciers
    print("ACIERS EC2 :")
    print()
    for fyk in [400, 500]:
        s = oc.SteelEC2(fyk=fyk)
        print(f"  B{fyk}B :")
        print(f"    fyk = {s.fyk:.1f} MPa")
        print(f"    fyd = {s.fyd:.2f} MPa")
        print(f"    Es = {s.Es:.0f} MPa")
        print(f"    epsilon_yk = {s.epsilon_yk*1000:.3f} permil")
        print(f"    epsilon_ud = {s.epsilon_ud*1000:.1f} permil")
        print()


def main():
    print("=" * 70)
    print("EXEMPLE : LOIS DE COMPORTEMENT DES MATERIAUX")
    print("=" * 70)
    print()
    
    print_material_properties()
    
    if HAS_MATPLOTLIB:
        plot_concrete_law()
        plot_steel_law()
        print()
        print("Graphiques sauvegardes !")
    else:
        print("Installez matplotlib pour visualiser les lois :")
        print("  pip install matplotlib")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

