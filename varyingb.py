import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # For progress bars

# System parameters
L = 25  # Lattice size (L x L)
mu = 1   # Magnetic moment
J = 0.2  # Coupling constant (set to 0 for paramagnetism)
N = L * L
num_steps = 40000
equilibration_steps = 10000
endp = 5  # Maximum value for B or kT
graphlim = (endp + 0.1)

# Simulation settings
oscillating = True   # Toggle for oscillating magnetic field
omega = 0.001        # Frequency of oscillation
n_points = 20        # Number of points in each range

# Create ranges with discrete points
B_values = np.linspace(0, endp, n_points)
kT_values = np.linspace(0.1, endp, n_points)

# Fixed values for each plot
fixed_kT = 0.3
fixed_B = 0.9

# Theory functions
def theoretical_magnetization(B, kT):
    """Calculate theoretical magnetization for given B and kT."""
    return mu * np.tanh((2 * J * mu + mu * B) / kT)

def simulate_ising(B, kT, J, oscillating=False, omega=0.001):
    """
    Simulate 2D Ising model with Metropolis algorithm.
    Returns dictionary with mean, std, and stderr of magnetization.
    """
    spins = np.random.choice([-1, 1], size=(L, L))
    mag_history = []
    
    for step in range(num_steps):
        # Random site selection
        i, j = np.random.randint(0, L, size=2)
        s = spins[i, j]
        
        # Apply oscillating field if enabled
        current_B = B * np.sin(omega * step) if oscillating else B
        
        # Calculate energy difference
        neighbors = (spins[(i+1)%L, j] + spins[(i-1)%L, j] + 
                     spins[i, (j+1)%L] + spins[i, (j-1)%L])
        delta_E = 2 * J * s * neighbors + 2 * mu * current_B * s
        
        # Metropolis condition
        if delta_E <= 0 or np.random.rand() < np.exp(-delta_E / kT):
            spins[i, j] *= -1
        
        # Record after equilibration
        if step >= equilibration_steps:
            mag_history.append(mu * np.sum(spins) / N)
    
    return {
        'mean': np.mean(mag_history),
        'std': np.std(mag_history),
        'stderr': np.std(mag_history) / np.sqrt(len(mag_history))
    }

# Initialize figure with better layout
plt.figure(figsize=(18, 7))
plt.suptitle(f"2D Ising Model Simulation (L={L}, J={J}, μ={mu})", fontsize=16, y=1.02)

# Left plot: M vs B (fixed kT)
ax1 = plt.subplot(1, 2, 1)

# Theory curve (higher resolution)
B_theory = np.linspace(0, endp, 1000)
M_theory = theoretical_magnetization(B_theory, fixed_kT)
plt.plot(B_theory, M_theory, 'r-', label='Theoretical', linewidth=2.5, alpha=0.8)

# Simulation data with progress bar
print("Simulating M vs B (fixed kT)...")
sim_data = [simulate_ising(b, fixed_kT, J, oscillating, omega) for b in tqdm(B_values)]
means = [d['mean'] for d in sim_data]
stds = [d['std'] for d in sim_data]

# Plotting with improved styling
plt.errorbar(B_values, means, yerr=stds, fmt='o', color='royalblue', 
             capsize=4, capthick=1.5, elinewidth=1.5, label='Simulation ± SD')
plt.plot(B_values, means, '--', color='royalblue', alpha=0.5, linewidth=1)

plt.xlabel('Magnetic Field (B)', fontsize=12)
plt.ylabel('Magnetization per spin', fontsize=12)
plt.title(f'Magnetization vs Field (kT = {fixed_kT})', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=11, framealpha=1)
plt.xlim(-0.1, graphlim)

# Right plot: M vs kT (fixed B)
ax2 = plt.subplot(1, 2, 2)

# Theory curve
kT_theory = np.linspace(0.1, endp, 1000)
M_theory_kT = theoretical_magnetization(fixed_B, kT_theory)
plt.plot(kT_theory, M_theory_kT, 'r-', label='Theoretical', linewidth=2.5, alpha=0.8)

# Simulation data with progress bar
print("\nSimulating M vs kT (fixed B)...")
sim_data_kT = [simulate_ising(fixed_B, kt, J, oscillating, omega) for kt in tqdm(kT_values)]
means_kT = [d['mean'] for d in sim_data_kT]
stds_kT = [d['std'] for d in sim_data_kT]

# Plotting with improved styling
plt.errorbar(kT_values, means_kT, yerr=stds_kT, fmt='o', color='forestgreen', 
             capsize=4, capthick=1.5, elinewidth=1.5, label='Simulation ± SD')
plt.plot(kT_values, means_kT, '--', color='forestgreen', alpha=0.5, linewidth=1)

plt.xlabel('Temperature (kT)', fontsize=12)
plt.ylabel('Magnetization per spin', fontsize=12)
plt.title(f'Magnetization vs Temperature (B = {fixed_B})', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=11, framealpha=1)
plt.xlim(0, graphlim)

# Final adjustments
plt.tight_layout()
plt.savefig('ising_varying_B_kT.png', dpi=300, bbox_inches='tight')
