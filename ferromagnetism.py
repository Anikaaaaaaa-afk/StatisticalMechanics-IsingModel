import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
L = 15  # Grid size
J = 0.2  # Ferromagnetic coupling constant
mu = 1.0  # Magnetic moment
B = 0.8  # External magnetic field strength
kT = 0.5  # Thermal energy
num_steps = 1000  # Max simulation steps

# Initialize spin grid randomly
spins = np.random.choice([-1, 1], size=(L, L))

# Magnetization function
def magnetization(spins):
    return mu * np.sum(spins)

# Local energy for spin at (i, j)
def local_energy(spins, i, j):
    s = spins[i, j]
    neighbors = (
        spins[(i + 1) % L, j]
        + spins[(i - 1) % L, j]
        + spins[i, (j + 1) % L]
        + spins[i, (j - 1) % L]
    )
    return -J * s * neighbors - mu * B * s

# Metropolis update
def update_spins(spins, J, mu, B, kT):
    new_spins = spins.copy()
    i, j = np.random.randint(0, L, size=2)

    current_energy = local_energy(new_spins, i, j)
    proposed_energy = -current_energy  # Flipping spin reverses energy

    delta_E = proposed_energy - current_energy

    # Boltzmann condition
    if delta_E <= 0 or np.random.rand() < np.exp(-delta_E / kT):
        new_spins[i, j] *= -1

    return new_spins

# Set up plot
fig, ax = plt.subplots()
X, Y = np.meshgrid(np.arange(L), np.arange(L))
quiver = ax.quiver(
    X,
    Y,
    np.zeros_like(spins),
    spins,
    color=["red" if s == -1 else "blue" for s in spins.flat],
    pivot="middle",
)

# Animation function
def animate(frame):
    global spins, ani

    if magnetization(spins) < 151:
        spins = update_spins(spins, J, mu, B, kT)
        quiver.set_UVC(np.zeros_like(spins), spins)
        quiver.set_color(["red" if s == -1 else "blue" for s in spins.flat])
        ax.set_title(f"Magnetization: {magnetization(spins):.1f}\nB={B:.2f}, kT={kT:.2f}")
    else:
        ani.event_source.stop()

    return quiver,

# Create animation
ani = animation.FuncAnimation(
    fig, animate, frames=num_steps, interval=50, blit=False
)

# Save animation
ani.save("ferro.mp4", writer="ffmpeg", fps=20)

# Optional: Show plot during execution
# plt.show()

