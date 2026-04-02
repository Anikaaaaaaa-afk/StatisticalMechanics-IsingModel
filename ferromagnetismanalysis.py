import numpy as np
import matplotlib.pyplot as plt

# CODE FOR FLUCTUATIONS

L = 15  # grid
J = 0.2  # coupling constant
mu = 1.0  # magnetic moment
B = 0.3 
num_steps = 100000 
N = L * L

spins = np.random.choice([-1, 1], size=(L, L))

def magnetization(spins):
    return mu * np.sum(spins)

def local_energy(spins, i, j):
    s = spins[i, j]
    neighbors = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i, (j+1)%L] + spins[i, (j-1)%L]
    return (-J * s * neighbors) - (mu * B * s)
    
def update_spins(spins, J, mu, B, kT):
    new_spins = spins.copy()
    i, j = np.random.randint(0, L, size=2)
    current_energy = local_energy(new_spins, i, j)
    proposed_energy = local_energy(new_spins, i, j) * -1
    delta_E = proposed_energy - current_energy
    if delta_E <= 0 or np.random.rand() < np.exp(-delta_E / kT):
        new_spins[i, j] *= -1
    return new_spins

# Original simulation for magnetization evolution
kT = 0.5
magnetization_history = []
for step in range(num_steps):
    spins = update_spins(spins, J, mu, B, kT)
    magnetization_history.append(magnetization(spins))

plt.figure(figsize=(10, 6))
plt.plot(range(num_steps), magnetization_history, 'b-', linewidth=2)
plt.xlabel('Monte Carlo Step', fontsize=14)
plt.ylabel('Magnetization', fontsize=14)
plt.title(f'Magnetization Evolution (B = {B}, J = {J}, kT = {kT})', fontsize=16)
plt.grid(True, alpha=0.3)

saturation_magnetization = N * mu
plt.axhline(y=saturation_magnetization, color='g', linestyle=':',label=f'Saturation: {saturation_magnetization}')
plt.legend(fontsize=12)
plt.savefig('magnetization_evolution.png', dpi=300)

# New code for fluctuations vs kT
kT_values = np.linspace(0.1, 3.0, 20)  # Range of temperatures to study
fluctuations = []

for kT in kT_values:
    # Reset spins for each temperature
    spins = np.random.choice([-1, 1], size=(L, L))
    mag_history = []
    
    # Equilibration phase
    for _ in range(num_steps//2):
        spins = update_spins(spins, J, mu, B, kT)
    
    # Measurement phase
    for _ in range(num_steps//2):
        spins = update_spins(spins, J, mu, B, kT)
        mag_history.append(magnetization(spins))
    
    # Calculate standard deviation of magnetization
    fluctuations.append(np.std(mag_history))

# Plot fluctuations vs kT
plt.figure(figsize=(10, 6))
plt.plot(kT_values, fluctuations, 'ro-', linewidth=2)
plt.xlabel('Temperature (kT)', fontsize=14)
plt.ylabel('Magnetization Fluctuations (σ)', fontsize=14)
plt.title('Magnetization Fluctuations vs Temperature', fontsize=16)
plt.grid(True, alpha=0.3)
plt.savefig('fluctuations_vs_kT.png', dpi=300)
