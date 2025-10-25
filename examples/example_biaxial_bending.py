"""
Exemple de flexion biaxiale selon Eurocode 2

Cas académique : Section rectangulaire avec flexion dans deux plans
Comparaison avec méthode des surfaces de résistance équivalentes

Référence : Mari & Scordelis (1984), Spacone et al. (1996)
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from opensection import RectangularSection, ConcreteEC2, SteelEC2, RebarGroup, SectionSolver


def biaxial_bending_study():
    """Étude de flexion biaxiale avec comparaison analytique"""

    print("Étude de flexion biaxiale")
    print("=" * 60)

    # Section rectangulaire 300×500mm
    b, h = 0.3, 0.5

    print("Paramètres géométriques :")
    print(f"  Section : {b*1000:.0f}×{h*1000:.0f} mm")

    # Matériaux
    concrete = ConcreteEC2(fck=25)  # C25/30
    steel = SteelEC2(fyk=500)       # B500B

    print("
Matériaux :")
    print(f"  Béton {concrete.fck} MPa (fcd = {concrete.fcd:.2f} MPa)")
    print(f"  Acier {steel.fyk} MPa (fyd = {steel.fyd:.2f} MPa)")

    # Section géométrique
    section = RectangularSection(width=b, height=h)

    # Armatures symétriques
    rebars = RebarGroup()
    cover = 0.035  # mm
    dia = 0.016    # Ø16mm

    # Armatures sur les 4 faces
    # Face inférieure (tendue en y)
    rebars.add_rebar(y=-h/2 + cover + dia/2, z=0.0, diameter=dia, n=3)
    # Face supérieure (comprimée en y)
    rebars.add_rebar(y=h/2 - cover - dia/2, z=0.0, diameter=dia, n=2)
    # Faces latérales (pour flexion en z)
    rebars.add_rebar(y=0.0, z=-b/2 + cover + dia/2, diameter=dia, n=2)
    rebars.add_rebar(y=0.0, z=b/2 - cover - dia/2, diameter=dia, n=2)

    print("
Armatures :")
    print(f"  Face Y- : 3Ø{dia*1000:.0f}mm")
    print(f"  Face Y+ : 2Ø{dia*1000:.0f}mm")
    print(f"  Faces Z± : 2×2 Ø{dia*1000:.0f}mm")
    print(f"  Total As = {rebars.total_area*1e4:.1f} cm²")

    # Création du solveur
    solver = SectionSolver(section, concrete, steel, rebars)

    print("
Analyse :")
    print(f"  Fibres béton : {len(solver.fibers)}")
    print(f"  Points d'armature : {len(solver.rebar_array)}")

    # Étude de la surface de résistance en flexion biaxiale
    print("
Construction de la surface de résistance biaxiale...")

    # Grille de moments (My, Mz)
    My_vals = np.linspace(-150, 150, 15)  # kN·m
    Mz_vals = np.linspace(-150, 150, 15)  # kN·m

    My_grid, Mz_grid = np.meshgrid(My_vals, Mz_vals)
    N_capacity = np.zeros_like(My_grid)

    # Pour chaque combinaison (My, Mz), trouver le N maximal
    for i in range(len(My_vals)):
        for j in range(len(Mz_vals)):
            My = My_vals[i]
            Mz = Mz_vals[j]

            # Recherche dichotomique du N maximal
            N_min, N_max = 0, 2000  # kN

            for _ in range(12):  # 12 itérations pour précision ~1kN
                N_test = (N_min + N_max) / 2
                result = solver.solve(N=N_test, My=My, Mz=Mz)

                if result.converged and result.sigma_c_max <= concrete.fcd * 1.01:
                    N_min = N_test
                else:
                    N_max = N_test

            N_capacity[j, i] = N_min  # Note: inversion pour meshgrid

    # Résistance en compression pure
    result_comp = solver.solve(N=2000, My=0, Mz=0)
    N_pure = result_comp.N if result_comp.converged else 0

    # Résistances uniaxiales
    result_My = solver.solve(N=0, My=150, Mz=0)
    My_max = result_My.My if result_My.converged else 0

    result_Mz = solver.solve(N=0, My=0, Mz=150)
    Mz_max = result_Mz.Mz if result_Mz.converged else 0

    print("
Résistances limites :")
    print(f"  Compression pure N_max = {N_pure:.0f} kN")
    print(f"  Flexion pure My_max = {My_max:.1f} kN·m")
    print(f"  Flexion pure Mz_max = {Mz_max:.1f} kN·m")

    return My_vals, Mz_vals, N_capacity, N_pure, My_max, Mz_max


def plot_interaction_surface(My_vals, Mz_vals, N_capacity, N_pure, My_max, Mz_max):
    """Tracé de la surface d'interaction tridimensionnelle"""

    fig = plt.figure(figsize=(14, 10))

    # Surface 3D
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')

    My_grid, Mz_grid = np.meshgrid(My_vals, Mz_vals)

    surf = ax1.plot_surface(My_grid, Mz_grid, N_capacity,
                           cmap='viridis', alpha=0.8, linewidth=0.5)

    ax1.set_xlabel('Moment My (kN·m)')
    ax1.set_ylabel('Moment Mz (kN·m)')
    ax1.set_zlabel('Effort axial N (kN)')
    ax1.set_title('Surface d\'interaction N-My-Mz')
    ax1.view_init(elev=20, azim=45)

    # Projection dans le plan N-M
    ax2 = fig.add_subplot(2, 2, 2)

    # Contours de niveau
    CS = ax2.contour(My_grid, Mz_grid, N_capacity, levels=15, cmap='viridis')
    ax2.clabel(CS, inline=True, fontsize=8)

    ax2.set_xlabel('Moment My (kN·m)')
    ax2.set_ylabel('Moment Mz (kN·m)')
    ax2.set_title('Contours N constant (vue du dessus)')
    ax2.grid(True, alpha=0.3)

    # Sections caractéristiques
    ax3 = fig.add_subplot(2, 2, 3)

    # Section N-My (Mz=0)
    mask_Mz0 = np.abs(Mz_vals) < 1e-6
    if np.any(mask_Mz0):
        idx_Mz0 = np.where(mask_Mz0)[0][0]
        ax3.plot(My_vals, N_capacity[idx_Mz0, :], 'b-', linewidth=3, label='Flexion My (Mz=0)')

    # Section N-Mz (My=0)
    mask_My0 = np.abs(My_vals) < 1e-6
    if np.any(mask_My0):
        idx_My0 = np.where(mask_My0)[0][0]
        ax3.plot(Mz_vals, N_capacity[:, idx_My0], 'r--', linewidth=3, label='Flexion Mz (My=0)')

    ax3.axhline(y=N_pure, color='k', linestyle=':', linewidth=2, label=f'Compression pure: {N_pure:.0f} kN')
    ax3.set_xlabel('Moment M (kN·m)')
    ax3.set_ylabel('Effort axial N (kN)')
    ax3.set_title('Sections caractéristiques')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Point de fonctionnement
    ax4 = fig.add_subplot(2, 2, 4)

    # Exemple de point de fonctionnement
    My_point = 80   # kN·m
    Mz_point = 60   # kN·m
    N_point = 800   # kN

    ax4.plot(My_vals, N_capacity[np.abs(Mz_vals - Mz_point).argmin(), :], 'b-', alpha=0.7)
    ax4.plot(Mz_vals, N_capacity[:, np.abs(My_vals - My_point).argmin()], 'r-', alpha=0.7)

    ax4.scatter([My_point], [N_point], color='red', s=100, zorder=5, label='Point de fonctionnement')
    ax4.axhline(y=N_point, color='red', linestyle='--', alpha=0.7)
    ax4.axvline(x=My_point, color='red', linestyle='--', alpha=0.7)

    ax4.set_xlabel('Moment My (kN·m)')
    ax4.set_ylabel('Effort axial N (kN)')
    ax4.set_title(f'Point de fonctionnement\nMy={My_point} kN·m, Mz={Mz_point} kN·m, N={N_point} kN')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('biaxial_interaction_surface.png', dpi=150, bbox_inches='tight')
    plt.show()


def analytical_comparison():
    """Comparaison avec approche analytique simplifiée"""

    print("\n" + "=" * 60)
    print("COMPARAISON AVEC APPROCHE ANALYTIQUE")
    print("=" * 60)

    # Section 300×500mm, béton C25/30
    b, h = 0.3, 0.5
    concrete = ConcreteEC2(fck=25)

    # Calcul analytique simplifié (EC2, méthode des surfaces équivalentes)
    # Pour section rectangulaire sans armatures comprimées

    # Résistance en compression pure
    N_pure_analytical = concrete.fcd * b * h * 1000  # kN

    # Résistance en flexion pure (hypothèse béton seul)
    # M_max = (1/6) * fcd * b * h²
    My_max_analytical = (1/6) * concrete.fcd * b * h**2

    print("Approche analytique simplifiée (EC2) :")
    print(f"  Compression pure N_max = {N_pure_analytical:.0f} kN")
    print(f"  Flexion pure My_max = {My_max_analytical:.1f} kN·m")

    # Calcul numérique pour comparaison
    section = RectangularSection(width=b, height=h)
    solver = SectionSolver(section, concrete, SteelEC2(fyk=500), RebarGroup())

    result_comp = solver.solve(N=2000, My=0, Mz=0)
    result_flex = solver.solve(N=0, My=My_max_analytical*1.1, Mz=0)

    print("
Résultats numériques :")
    print(f"  Compression pure N_max = {result_comp.N if result_comp.converged else 0:.0f} kN")
    print(f"  Flexion pure My_max = {result_flex.My if result_flex.converged else 0:.1f} kN·m")

    # Écart relatif
    error_N = abs(result_comp.N - N_pure_analytical) / N_pure_analytical * 100
    error_M = abs(result_flex.My - My_max_analytical) / My_max_analytical * 100

    print("
Écarts :")
    print(f"  Compression : {error_N:.2f}%")
    print(f"  Flexion : {error_M:.2f}%")

    return N_pure_analytical, My_max_analytical


if __name__ == "__main__":
    My_vals, Mz_vals, N_capacity, N_pure, My_max, Mz_max = biaxial_bending_study()
    plot_interaction_surface(My_vals, Mz_vals, N_capacity, N_pure, My_max, Mz_max)
    N_pure_ana, My_max_ana = analytical_comparison()

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    print("✓ Surface d'interaction biaxiale construite")
    print("✓ Comparaison avec approche analytique EC2")
    print("✓ Visualisation 3D de la capacité portante")
    print("✓ Point de fonctionnement analysé")
    print("\nRéférence : Mari & Scordelis (1984) - Fiber Analysis")
