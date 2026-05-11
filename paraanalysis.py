import numpy as np
import matplotlib.pyplot as plt

# Parameters
L = 15  # Grid size
mu = 1.0  # Magnetic moment
B = 0.3  # External magnetic field
num_steps = 10000  # Number of Monte Carlo steps
N = L * L  # Total number of spins

# Initialize spins randomly (+1 or -1)
spins = np.random.choice([-1, 1], size=(L, L))

# Functions
def magnetization(spins):
    return mu * np.sum(spins)

def update_spins(spins, B, mu, kT):
    new_spins = spins.copy()
    i, j = np.random.randint(0, L, size=2)
    new_spins[i, j] *= -1
    delta_U = -mu * B * (new_spins[i, j] - spins[i, j])
    if delta_U <= 0 or np.random.rand() < np.exp(-delta_U / kT):
        return new_spins
    else:
        return spins

# Magnetization evolution for a fixed kT
kT_fixed = 0.5
magnetization_history = []
for step in range(num_steps):
    spins = update_spins(spins, B, mu, kT_fixed)
    magnetization_history.append(magnetization(spins))

# Theoretical magnetization
theory_M = N * mu * np.tanh(mu * B / kT_fixed)

# Plot magnetization evolution
plt.figure(figsize=(10, 6))
plt.plot(range(num_steps), magnetization_history, 'b-', linewidth=2)
plt.axhline(y=theory_M, color='r', linestyle='--', label=f'Theoretical: {theory_M:.1f}')
plt.xlabel('Monte Carlo Step', fontsize=14)
plt.ylabel('Magnetization', fontsize=14)
plt.title(f'Magnetization Evolution (Paramagnet: B = {B}, kT = {kT_fixed})', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('magnetization_evolution.png', dpi=300, bbox_inches='tight')

# Sweep over temperature values
kT_values = np.linspace(0.1, 5.0, 50)
# Theoretical entropy per spin fixed B
entropy_values = np.log(2 * np.cosh(mu * B / kT_values)) - (mu * B / kT_values) * np.tanh(mu * B / kT_values)

plt.figure(figsize=(10, 6))
plt.plot(kT_values, entropy_values, 'm-', linewidth=2)
plt.xlabel("kT", fontsize=14)
plt.ylabel("Entropy S (per spin)", fontsize=14)
plt.title("Theoretical Entropy of a Paramagnet", fontsize=16)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('paramagnet_entropy.png', dpi=300, bbox_inches='tight')

# Entropy per spin formula for paramagnetism fixed kT
kT = 0.5  # Fixed temperature

# Varying B from 0 to 5
B_values = np.linspace(0, 5, 200)
entropy_values = np.log(2 * np.cosh(mu * B_values / kT)) - (mu * B_values / kT) * np.tanh(mu * B_values / kT)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(B_values, entropy_values, 'orange', linewidth=2)
plt.xlabel("Magnetic Field B", fontsize=14)
plt.ylabel("Entropy S (per spin)", fontsize=14)
plt.title(f"Entropy vs Magnetic Field (kT = {kT})", fontsize=16)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('entropy_vs_B.png', dpi=300, bbox_inches='tight')

# Plotting probability of alignment
P_up = np.exp(mu * B / kT_values) / (2 * np.cosh(mu * B / kT_values))
P_down = np.exp(-mu * B / kT_values) / (2 * np.cosh(mu * B / kT_values))

plt.figure(figsize=(10, 6))
plt.plot(kT_values, P_up, label="P(up)", color='green')
plt.plot(kT_values, P_down, label="P(down)", color='orange')
plt.xlabel("kT", fontsize=14)
plt.ylabel("Probability", fontsize=14)
plt.title("Probability of Spin Alignment vs Temperature", fontsize=16)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('alignment_probability.png', dpi=300, bbox_inches='tight')



