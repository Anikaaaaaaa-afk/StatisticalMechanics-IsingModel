import numpy as np
import matplotlib.pyplot as plt

# System parameters
N = 15 * 15  # Number of spins (L=15 grid)
mu = 1.0     # Magnetic moment
B = 0.3      # External field strength

# Temperature range
kT_values = np.linspace(0.1, 5.0, 100)

# Theoretical fluctuations
fluctuations = N * (mu**2) / (np.cosh(mu * B / kT_values))**2

# Plot
plt.figure(figsize=(10, 6))
plt.plot(kT_values, fluctuations, 'b-', linewidth=3, label=f'Theory: $Nμ^2 \mathrm{{sech}}^2(μB/kT)$ (B={B})')
plt.xlabel('Temperature (kT)', fontsize=14)
plt.ylabel('Magnetization Fluctuations $⟨M^2⟩ - ⟨M⟩^2$', fontsize=14)
plt.title('Paramagnetic Fluctuations', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Highlight critical region
peak_kT = mu * B / 0.66  # Approximate peak location (sech² peaks near μB/kT ≈ 0.66)
plt.axvline(x=peak_kT, color='r', linestyle='--', label=f'Peak at kT ≈ {peak_kT:.2f}')
plt.legend(fontsize=12)
plt.savefig('paramagnetic_fluctuations_theory.png', dpi=300, bbox_inches='tight')
