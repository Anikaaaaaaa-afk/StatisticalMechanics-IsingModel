import numpy as np
import matplotlib.pyplot as plt

# Parameters (identical structure to ferromagnetism code)
L = 15                # Grid size
mu = 1.0              # Magnetic moment
B = 0.3               # External field
num_steps = 100000    # Total Monte Carlo steps
N = L * L             # Total spins

# Initialize spins randomly
spins = np.random.choice([-1, 1], size=(L, L))

# Magnetization function (same as before)
def magnetization(spins):
    return mu * np.sum(spins)

# Energy function (simplified: no spin-spin interaction, only B-field)
def energy(spins):
    return -mu * B * np.sum(spins)

# Spin update rule (Metropolis, same structure as ferro but no J)
def update_spins(spins, B, mu, kT):
    new_spins = spins.copy()
    i, j = np.random.randint(0, L, size=2)
    new_spins[i, j] *= -1  # Propose flip
    
    delta_U = -mu * B * (new_spins[i, j] - spins[i, j])  # Energy change
    
    # Metropolis acceptance
    if delta_U <= 0 or np.random.rand() < np.exp(-delta_U / kT):
        return new_spins
    else:
        return spins

kT_values = np.linspace(0.1, 5.0, 100)  # Temperature range
fluctuations = []

for kT in kT_values:
    spins = np.random.choice([-1, 1], size=(L, L))  # Reset spins
    mag_history = []
    
    # Equilibration phase (discard first half)
    for _ in range(num_steps // 2):
        spins = update_spins(spins, B, mu, kT)
    
    # Measurement phase (record second half)
    for _ in range(num_steps // 2):
        spins = update_spins(spins, B, mu, kT)
        mag_history.append(magnetization(spins))
    
    fluctuations.append(np.std(mag_history))  # Standard deviation = fluctuations

# Plotting (same style as ferro)
plt.figure(figsize=(10, 6))
plt.plot(kT_values, fluctuations, 'ro-', linewidth=2, label='Simulation')
plt.xlabel('Temperature (kT)', fontsize=14)
plt.ylabel('Magnetization Fluctuations (σ)', fontsize=14)
plt.title(f'Paramagnet: Fluctuations vs Temperature (B={B})', fontsize=16)
plt.grid(True, alpha=0.3)

# Theoretical curve (for paramagnet)
#theory_fluct = N * (mu**2) / (np.cosh(mu * B / kT_values)**2)  # Exact solution
#plt.plot(kT_values, theory_fluct, 'k--', label='Theory: $Nμ^2 \mathrm{sech}^2(μB/kT)$')
#plt.legend(fontsize=12)
plt.savefig('paramagnet_fluctuations.png', dpi=300)
