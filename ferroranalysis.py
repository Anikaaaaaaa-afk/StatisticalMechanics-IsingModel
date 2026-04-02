import numpy as np
import matplotlib.pyplot as plt





# System parameters
L = 25
mu = 1
J = 0.2 # set this to 0 for paramagnetism
N = L * L
num_steps = 40000
equilibration_steps = 10000
endp = 5 #the maximum number you want B or kT to be, the higher this is, the more data we get to analyse
graphlim = (endp + 0.1) #cuts the graph off exactly 0.1 after the last number we calculate shit for





# Ranges with discrete points - change the number of steps
B_values = np.linspace(0, endp, 20)
kT_values = np.linspace(0.1, endp, 20)

# Fixed values
fixed_kT = 0.3
fixed_B = 0.9





# theory functions
def theoretical_magnetization(B, kT):
    return mu * np.tanh((2*J*mu + mu*B)/kT)

# error analysis
def simulate_with_J(B, kT, J):
    spins = np.random.choice([-1, 1], size=(L, L))
    mag_history = []

    for _ in range(num_steps):
        i, j = np.random.randint(0, L, size=2)
        s = spins[i, j]
        neighbors = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i, (j+1)%L] + spins[i, (j-1)%L]
        delta_E = 2 * J * s * neighbors + 2 * mu * B * s

        if delta_E <= 0 or np.random.rand() < np.exp(-delta_E / kT):
            spins[i, j] *= -1

        if _ >= equilibration_steps:
            # Normalized magnetization per spin
            mag_history.append(mu * np.sum(spins) / N)

    return {
        'mean': np.mean(mag_history),
        'std': np.std(mag_history),
        'stderr': np.std(mag_history) / np.sqrt(len(mag_history))
    }








# initialize figure
plt.figure(figsize=(16, 6))





# left: M vs B (fixed kT)
plt.subplot(1, 2, 1)

# theory
B_theory = np.linspace(0, endp, 10000)
M_theory = [theoretical_magnetization(b, fixed_kT) for b in B_theory]
plt.plot(B_theory, M_theory, 'r-', label='Theory', linewidth=3)

# sim
sim_data = [simulate_with_J(b, fixed_kT, J) for b in B_values]
means = [d['mean'] for d in sim_data]
stds = [d['std'] for d in sim_data]
stderrs = [d['stderr'] for d in sim_data]

# error bars and standard error markers
plt.errorbar(B_values, means, yerr=stds, fmt='bo', capsize=5, label='Mean ± Std Dev')
plt.plot(B_values, means, 'b--', linewidth=1, alpha=0.5)
plt.scatter(B_values, means, s=100, c='white', edgecolor='blue', linewidths=2, label='Standard Error', zorder=3)

plt.xlabel('Magnetic Field (B)', fontsize=14)
plt.ylabel('Magnetization per spin', fontsize=14)
plt.title(f'M vs B (kT = {fixed_kT})', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.xlim(-0.1, graphlim)





# right: M vs kT (fixed B)
plt.subplot(1, 2, 2)

kT_theory = np.linspace(0.1, endp, 10000)
M_theory_kT = [theoretical_magnetization(fixed_B, kt) for kt in kT_theory]
plt.plot(kT_theory, M_theory_kT, 'r-', label='Theory', linewidth=3)

sim_data_kT = [simulate_with_J(fixed_B, kt, J) for kt in kT_values]
means_kT = [d['mean'] for d in sim_data_kT]
stds_kT = [d['std'] for d in sim_data_kT]
stderrs_kT = [d['stderr'] for d in sim_data_kT]

plt.errorbar(kT_values, means_kT, yerr=stds_kT, fmt='go', capsize=5, label='Mean ± Std Dev')
plt.plot(kT_values, means_kT, 'g--', linewidth=1, alpha=0.5)
plt.scatter(kT_values, means_kT, s=100, c='white', edgecolor='green', linewidths=2, label='Standard Error', zorder=3)

plt.xlabel('Temperature (kT)', fontsize=14)
plt.ylabel('Magnetization per spin', fontsize=14)
plt.title(f'M vs kT (B = {fixed_B})', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.xlim(0, graphlim)





#closing
plt.tight_layout()
plt.savefig('M_vs_B_M_vs_kT.png', dpi=300, bbox_inches='tight')
