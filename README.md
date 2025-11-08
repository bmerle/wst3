# Anisotropic Young’s Modulus for Cubic Crystals (Color-Mapped 3D Surface)

Compute and visualize the directional Young’s modulus E(n) for cubic crystals from their elastic compliances (S11, S12, S44).
The script draws a 3D surface where the radius equals E(n) in a given direction and colors the surface by the magnitude of E.

##  Features

- Computes E(n) for cubic symmetry using compliances.
- Produces a smooth, color-coded 3D surface (radius = E, color = E).
- Customizable angular resolution and colormap.
- Basic stability checks for the supplied compliance values.

## Formula

For cubic crystals, the directional Young’s modulus is given by:

1/E(n) = S11 - 2 * (S11 - S12 - 0.5*S44) * (n1^2 n2^2 + n2^2 n3^2 + n3^2 n1^2)

The script evaluates this on a uniform grid over the unit sphere and returns E in GPa provided you are providing S_ij in GPa^-1.

## Requirements

- Python 3.9+
- NumPy
- Matplotlib 3.7+

## Usage (CLI)

Run the script with your compliances (in GPa^-1):
python anisotropic-young-modulus_cubic-materials_from_compliance_colored.py --S11 0.014928 --S12 -0.006259 --S44 0.013280 --material Cu

### Arguments

| Argument | Type | Required | Description |
|-----------|------|-----------|--------------|
| `--S11` | float | ✓ | Compliance S11 in GPa^-1 |
| `--S12` | float | ✓ | Compliance S12 in GPa^-1 |
| `--S44` | float | ✓ | Compliance S44 in GPa^-1 |
| `--material` | str | ✗ | Material name (used in plot title & filename) |
| `--samples` | int | ✗ | Angular grid resolution (default: 200) |
| `--cmap` | str | ✗ | Colormap name (default: turbo) |

Output image will be saved as: {material} - Young's Modulus (GPa).png

## Tips

- Input S_ij in GPa^-1 → Output E in GPa
- Increase `--samples` for smoother surfaces (higher runtime)

## Binder

### Repository

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bmerle/wst3/main)

### Jupyter Notebook

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bmerle/wst3/main?filepath=run_young_modulus.ipynb)
