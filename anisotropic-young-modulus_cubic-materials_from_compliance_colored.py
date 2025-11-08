# anisotropic-young-modulus_cubic-materials_from_compliance_colored.py
# -----------------------------------------
# Calculates and visualizes the directional Young's modulus E(n)
# for cubic crystals (given compliances S11, S12, S44)
# and color-codes the 3D surface according to the magnitude of E(n).
# Compatible with Matplotlib 3.7+
#
# Syntax: python anisotropic-young-modulus_cubic-materials_from_compliance_colored.py --S11 0.014928 --S12 -0.006259 --S44 0.013280 --material Cu
# Compliances in [GPa]^-1
#
# -----------------------------------------

import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib import cm


def directional_E_cubic_from_S(S11, S12, S44, samples=300):
    """
    Compute the directional Young's modulus E(n) for a cubic crystal.
    Formula:
        1/E(n) = S11 - 2*(S11 - S12 - 0.5*S44) * (n1^2*n2^2 + n2^2*n3^2 + n3^2*n1^2)
    """

    # Create uniform angular grids (θ: polar, φ: azimuthal)
    theta = np.linspace(0, np.pi, samples)
    phi = np.linspace(0, 2*np.pi, samples)
    T, P = np.meshgrid(theta, phi)

    # Unit vector components on the sphere
    ax = np.sin(T) * np.cos(P)  # x = n1
    ay = np.sin(T) * np.sin(P)  # y = n2
    az = np.cos(T)              # z = n3

    # Squared direction cosines
    n1_2, n2_2, n3_2 = ax**2, ay**2, az**2

    # Invariant term involving direction cosines
    I2 = n1_2 * n2_2 + n2_2 * n3_2 + n3_2 * n1_2

    # Compute 1/E(n)
    Einv = S11 - 2.0 * (S11 - S12 - 0.5 * S44) * I2
    Einv = np.maximum(Einv, 1e-16)  # avoid division by zero

    # Return E(n) in GPa
    E = 1.0 / Einv
    return E, ax, ay, az


def plot_young_surface_colored(E, ax, ay, az, title,
                               cmap_name='turbo',
                               outfile="young3D_colored.jpg"):
    """
    Plot a color-coded 3D surface of the Young's modulus. The color corresponds to the radial distance ( = magnitude of E).

    Parameters
    ----------
    E : 2D array (GPa)
        Young's modulus spatial distribution
    ax, ay, az : 2D arrays
        Direction cosines
    cmap_name : str
        Matplotlib colormap name (e.g., 'viridis', 'plasma', 'inferno', 'turbo')
    outfile : str
        Output image filename
    """

    # Prepare color normalization based on E values with Matplotlib 3.7+ style colormap access
    norm = plt.Normalize(vmin=E.min(), vmax=E.max())
    cmap = plt.colormaps[cmap_name]
    colors = cmap(norm(E))

    # Create 3D plot
    plt.figure(dpi=200)
    ax3 = plt.subplot(111, projection='3d')

    # Plot the colored surface
    surf = ax3.plot_surface(E * ax, E * ay, E * az,
                            facecolors=colors,
                            rstride=1, cstride=1,
                            linewidth=0, antialiased=False)

    # Add a colorbar for scale reference
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(E)
    cbar = plt.colorbar(mappable, ax=ax3, shrink=0.6, pad=0.1)
    cbar.set_label("Young's Modulus (GPa)", rotation=270, labelpad=15)

    # Axis labels and style
    ax3.set_title(title)
    try:
        ax3.set_box_aspect([1, 1, 1])
    except Exception:
        pass

    # Make axis tick labels smaller
    ax3.tick_params(axis='x', labelsize=10)
    ax3.tick_params(axis='y', labelsize=10)
    ax3.tick_params(axis='z', labelsize=10)

    # Lighten up the gridlines
    ax3.xaxis._axinfo["grid"]['linewidth'] = 0.3
    ax3.yaxis._axinfo["grid"]['linewidth'] = 0.3
    ax3.zaxis._axinfo["grid"]['linewidth'] = 0.3
    ax3.grid(True)

    # Save and show
    plt.savefig(outfile, bbox_inches='tight')
    plt.show()


def main():
    """
    Command-line interface. See syntax at top of code.
    """

    # Define command-line arguments
    p = argparse.ArgumentParser(description="3D anisotropic Young's modulus for cubic crystals (color-coded by E magnitude).")
    p.add_argument("--material", type=str, default="Element") # Used for title of graph
    p.add_argument("--S11", type=float, required=True, help="Compliance S11 in GPa^-1")
    p.add_argument("--S12", type=float, required=True, help="Compliance S12 in GPa^-1")
    p.add_argument("--S44", type=float, required=True, help="Compliance S44 in GPa^-1")
    p.add_argument("--samples", type=int, default=200, help="Angular grid resolution (default: 200)")
    p.add_argument("--cmap", type=str, default="turbo", help="Colormap name (default: turbo)")
    args = p.parse_args()
    
    graph_title=str(args.material)+" - Young's Modulus (GPa)"
    
    # Basic stability check
    if not (args.S11 > 0 and args.S44 > 0 and
            (args.S11 - args.S12) > 0 and
            (args.S11 + 2 * args.S12) > 0):
        print("Warning: Compliance values may violate cubic stability conditions.")
        print("Check that S11 > 0, S44 > 0, S11 - S12 > 0, and S11 + 2*S12 > 0")

    # Compute and plot
    E, ax, ay, az = directional_E_cubic_from_S(args.S11, args.S12, args.S44, samples=args.samples)
    plot_young_surface_colored(E, ax, ay, az, cmap_name=args.cmap, title=graph_title, outfile=graph_title)


if __name__ == "__main__":
    main()
