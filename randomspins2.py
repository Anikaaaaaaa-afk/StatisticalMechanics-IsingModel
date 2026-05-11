import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 10  # Grid size
mu = 1  # Magnetic moment
B = 4.0  # Magnetic field strength
kT = 0.5  # Thermal energy
num_steps = 100  # Simulation steps

# Initialize spins randomly as +1 (up) or -1 (down)
spins = np.random.choice([-1, 1], size=(L, L))

# Magnetization: M = μ * Σ s_i
def magnetization(spins):
    return mu * np.sum(spins)

# Energy of the current state
def energy(spins):
    return -mu * B * np.sum(spins)

# Update spins using Metropolis-Hastings algorithm
def update_spins(spins, B, mu, kT):
    new_spins = spins.copy()
    i, j = np.random.randint(0, L, size=2)  # Pick a random spin
    
    # Propose flipping the spin
    new_spins[i, j] *= -1
    
    # Calculate energy change
    delta_U = -mu * B * (new_spins[i, j] - spins[i, j])
    
    # Flip if energy decreases or passes Boltzmann test
    if delta_U <= 0 or np.random.rand() < np.exp(-delta_U / kT):
        return new_spins
    else:
        return spins

# Visualization
fig, ax = plt.subplots()
X, Y = np.meshgrid(np.arange(L), np.arange(L))
# Plot spins as arrows: up (blue) or down (red)
quiver = ax.quiver(X, Y, np.zeros_like(spins), spins, color=['red' if s == -1 else 'blue' for s in spins.flat])

def animate(frame):
    global spins
    spins = update_spins(spins, B, mu, kT)
    # Update arrow colors and directions
    quiver.set_UVC(np.zeros_like(spins), spins)
    quiver.set_color(['red' if s == -1 else 'blue' for s in spins.flat])
    ax.set_title(f'Magnetization: {magnetization(spins):.1f}')
    return quiver,

ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=100, blit=False)
ani.save('boltzmann_spins.mp4', writer='ffmpeg', fps=10)
