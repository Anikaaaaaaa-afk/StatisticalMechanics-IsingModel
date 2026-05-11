This repository contains all the code used to simulate the 1D Ising Model.

The "Stat Mech Analysis of the Ising Model" PDF provides detailed math on how the different thermodynamic quantities were derived from the Boltzmann distribution. 





# 1. Primary Visualization

The following code works for primary understanding of how the setup will work:

a. boltzmannpara.py - for visualization. It simulates magnetic spins on a 2D grid undergoing thermal fluctuations according to the Boltzmann distribution.  
                      Each spin starts with a random initial orientation between 0 and 2pi radians. The potential energy due to the spin's orientation is computed. It is minimized when the spins align with the magnetic field (cos theta = cos 0 = 1). Since there is a negative sign associated with the potential energy, the lowest energy state is when the potential is negative. An angle of 90 degrees would give an intermediate potential energy of 0 while an angle of 180 degrees would give +1.  
                      At each step, a small thermal fluctuation causes the spins to try and reorient themselves in a different angle theta. We compute a "threshold energy" from the Boltzmann distribution. If the energy of the spin with the new alignment is lesser than the energy of its old alignment, the new alignment is always accepter. If the energy of the new alignment is not lesser than the energy of its old alignment, the new spin is accepted with a probability exp(-ΔU/kT).   
                      The higher B is, the more the field favours spin alignment.  
                      The output file is a video animation - boltzmann_spins.mp4.   
  

  
  

# 2. Paramagnetism

The following code (and their outputs) account for the study of paramagnetism:

a. panalysis.py - We start with an L*L grid of spins but unlike the previous case, here they only flip between +1 and -1.  
                  Since the effect we care about is magnetization, intermediate orientations are of little importance; further, electrons only have two spin states.  
                  Magnetization is just how many spins are aligned along the field. Mathematically, it is the product of the magnetic moment of a spin times the probability of that spin existing. If we were to sum over all the individual magnetic momenta of the spins in the grid, we would experimentally be achieving the same effect.   
                  Similar to what was done in the case of visualization, at the start of each step, a random spin is flipped (multiplied by -1). The change in potential energy is computed. Here, the cos is absorbed into the orientation of the spins themselves. For cos theta = +1, the overall potential is negative. So when the spin is +1, the potential energy is lowered and the spin is aligned with the magnetic field.   
                  The same checks are run as before. If the new state of spins lowers the potential energy, the new spins are retained. If they increase the potential energy, the random probability of such a state existing is tested against the robability exp(-ΔU/kT).  
                  Since this process is run every step, the magnetization is instantaneously recorded as an array. We plot this against the theoretical line provided from the equation in the PDF. The theoretical value is just a number. Experimentally, we should see magnetization increase dramatically until it reaches around this point and then waver about it. When the strength of the magnetic field is lesser than the thermal kicks the spins receive, the fluctuations are more dramatic.   
                  There isn't any sense or way of studying the entropy of the system experimentally so we just use the theoeretically derived equation from the PDF.  
                  We study how entropy of the system changes with respect to different kT and B values. When kT is comparably higher than B, the system is more disordered because the effect of the magnetic field is negated by the thermal kicks the spins receive. Conversely, when the magnetic field is strong, spins are far more likely to align, reducing entropy. At the point of B = kT, there is a "crossover".   
                  We also study the probability of spins (+1 and -1 individually) to align with the magnetic field across increasing kT values. As higher kT values lead to higher disorder, regardless of the specific spin, spins are less likely to align.  
                  The output files are - magnetization_evolution.png for the constant theory line and magnetization fluctuating about the line as the steps progress.  
                                         paramagnet_entropy.png for the theoretical entropy of the system.  
                                         entropy_vs_B.png which shows how entropy changes as the strength of the magnetic field changes.  
                                         entropy_vs_kT.png which shows how entropy changes as the thermal noise in the system changes.  
                                         alignment_probability.png which shows how likely the spins are to align with the magnetic field as kT changes.  

b. parafluctuationstheory.py - Plots the theoretical equation for fluctuations as given in the PDF. Pretty straightforward.
                               Output file - paramagnetic_fluctuations.png.
                               Different from the other output file because of the extra "ic" after paramagnet.

c. parafluctuations.py - The physics is the same as in panalysis.py. 
                         From the PDF, the fluctuations are given by the variance. This code implements that using the simulation data. 
                         The instantaneous magnetization across time is computed for each kT value given by the temperature range array. And for each kT, the variance in magnetization is computed and stored to the fluctuations array.
                         The variance is plotted against kT. 
                         We should see qualitative agreement between the output of this code and parafluctuationstheory.py. 
                         Output file - paramagnet_fluctuations.png.





# 3. Ferromagnetism

TBD
                  
                  





