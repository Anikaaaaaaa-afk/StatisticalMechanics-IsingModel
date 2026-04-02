import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


L = 10  # LxL grid
mu = 1  # Magnetic moment magnitude
B = 4.0  # Applied magnetic field strength
kT = 0.5  # Thermal energy
num_steps = 100  # Number of simulation steps



#randomize angles
theta = np.random.uniform(0, 2*np.pi, (L, L))


#initial potential energy
U = -mu * B * np.cos(theta)



def update_spins(theta, B, mu, kT):
    
    new_theta = theta + np.random.uniform(-0.1, 0.1, theta.shape)  # Small random fluctuations
    U_old = -mu * B * np.cos(theta)
    U_new = -mu * B * np.cos(new_theta)
    
    # energy change
    delta_U = U_new - U_old
    
    
    #randomized Boltzmann equation
    accept_prob = np.exp(-delta_U / kT)
    random_vals = np.random.rand(*theta.shape)
    
  
    theta = np.where((delta_U <= 0) | (random_vals < accept_prob), new_theta, theta)
    
    return theta
    
    
    


fig, ax = plt.subplots()
X, Y = np.meshgrid(np.arange(L), np.arange(L))
quiver = ax.quiver(X, Y, np.cos(theta), np.sin(theta))




def animate(frame):
    global theta
    theta = update_spins(theta, B, mu, kT)
    quiver.set_UVC(np.cos(theta), np.sin(theta))
    return quiver,



ani = animation.FuncAnimation(fig, animate, frames=num_steps, interval=100, blit=False)
ani.save('boltzmann_spins.mp4', writer='ffmpeg', fps=10)
