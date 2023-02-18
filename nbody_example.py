'''
The following was the initial ChatGPT prompt I used to generate the following code.  
It was actually a mess, and chatGPT changed streams mid-composition:

PROMPT_1: Generate a stubbed out python program using numpy. Include function 
definitions, but not the internal code that implements the functions.  
Instead just return 0.  The program should include a full main call 
using the "if _name_ == _main_" construction, and the main program 
should be complete.  The purpose of this program is to simulates N-body 
dynamics using the following pairwise force laws for pairwise spring, 
transverse velocity dampening, and velocity dampening:
fpw(x,y) = espilon_x_y * b * (norm(x-y) - D) * (y-x)/norm(x-y).  
ftv(x,y,vx) = - gamma_t * ( vx - dot(vx, (y-x)/norm(y-x))*(y-x)/norm(y-x) )
fvd(vx) = - gamma * vx
The variables x, y, and vx are vectors.  The variables gamma, gamma_t, b 
and D are scalars that are the same for all pairs of particles. The variable 
epsilon_x_y is a scalar variable that masks whether or not x should be 
influenced through a force from y.  The variables x and y represent the 
positions of particles, and the variable vx represents the velocity of 
the particle with position x.  
For coding conventions, make sure to use function definitions where it 
makes reading the code most efficient.  Also make sure to include a main 
function.  Document the code clearly and thoroughly.

PROMPT_2:Can you create the code for the fpw function so that it is 
compabible with simulate_n_body_dynamics?

PROMPT_3:Can you create the code for the ftv function so that it is 
compabible with simulate_n_body_dynamics?

PROMPT_4:Can you create the code for the fvd function so that it is 
compabible with simulate_n_body_dynamics?

PROMPT_5:Can you create the "if __name__ == '__main__':" code so that 
it runs the simulation of positions and velocities?  Use all the functions 
defined above, do not re-create them unless needed.  The position of each 
particle should be two dimensional, as should the velocity.  There 
should be 10 particles. 

NOTE:  Everything was going great until PROMPT_5, and then it changed 
it's style completely.  

The code worked, except that the intended asymmetric relationship of 
epsilon_x_y was not respected, as it included the y_x force, as well.

NOTE:  I put in most of the plotting commands, although it did put in one useless one.
'''


import numpy as np
from matplotlib import pyplot as plt


def fpw(x, y, epsilon_x_y, b, D):
    """
    Pairwise force law for pairwise spring.

    Parameters:
        x (numpy.ndarray): position vector of particle 1.
        y (numpy.ndarray): position vector of particle 2.
        epsilon_x_y (float): scalar variable that masks whether or not x should be influenced through a force from y.
        b (float): scalar that is the same for all pairs of particles.
        D (float): scalar that is the same for all pairs of particles.

    Returns:
        numpy.ndarray: force vector that particle 1 exerts on particle 2.
    """
    r = y - x
    r_norm = np.linalg.norm(r)
    if r_norm == 0:
        return np.zeros_like(x)
    return epsilon_x_y * b * (r_norm - D) * r / r_norm

def ftv(x, y, vx, gamma_t):
    """
    Pairwise force law for transverse velocity dampening.

    Parameters:
        x (numpy.ndarray): position vector of particle 1.
        y (numpy.ndarray): position vector of particle 2.
        vx (numpy.ndarray): velocity vector of particle 1.
        gamma_t (float): scalar that is the same for all pairs of particles.

    Returns:
        numpy.ndarray: force vector that particle 1 exerts on particle 2.
    """
    r = y - x
    r_norm = np.linalg.norm(r)
    if r_norm == 0:
        return np.zeros_like(vx)
    v_parallel = np.dot(vx, r / r_norm) * r / r_norm
    return -gamma_t * (vx - v_parallel)

def fvd(vx, gamma):
    """
    Pairwise force law for velocity dampening.

    Parameters:
        vx (numpy.ndarray): velocity vector of particle 1.
        gamma (float): scalar that is the same for all particles.

    Returns:
        numpy.ndarray: force vector that particle 1 exerts on particle 2.
    """
    return -gamma * vx


#if __name__ == '__main__':
# Parameters
N = 10
gamma = 3.
gamma_t = 0.1
b = 1
D = 1 
#epsilon = np.random.choice([0, 1], size=(N, N))
epsilon = np.zeros((N,N))
epsilon[:-1, 1:] = np.identity(N - 1)
np.fill_diagonal(epsilon, 0)

# Initial positions and velocities
#np.random.seed(0)
x = np.zeros((N, 2))
vx = np.zeros((N, 2))

x[:,0] = np.linspace(0,N-1,N)
x[:,1] = np.sin( np.linspace(0,2*np.pi, N))
vx[-1:,0] = 1

X = [x.copy()]
V = [vx.copy()]

# Simulation
T = 50
dt = 0.01
timesteps = int(T / dt)
for step in range(timesteps):
    # Calculate pairwise forces
    F = np.zeros_like(x)
    for i in range(N):
        for j in range(i, N):
            if epsilon[i, j]:
                F[i] += fpw(x[i], x[j], epsilon[i,j], b, D) + ftv(x[i], x[j], vx[i], gamma_t)
                #F[j] += fpw(x[j], x[i], epsilon[i,j], b, D) - ftv(x[i], x[j], vx[j], gamma_t)
    for i in range(N-1):
        F[i] += fvd(vx[i], gamma)

    # Update positions and velocities
    x += vx * dt + 0.5 * F * dt**2
    vx += 0.5 * F * dt
    X.append(x.copy())
    V.append(vx.copy())

X = np.array(X)
V = np.array(V)
# Plot final positions
plt.ion()
plt.title('Initial Agent Positions')
plt.scatter(X[0,:,0], X[0,:,1])
plt.grid()

plt.figure()
plt.title('Final Agent Positions')
plt.scatter(x[:, 0], x[:, 1])
plt.grid()


plt.figure()
plt.title('History of Agent Positions (with y-offset to show trends)')
for k in range(0,5001,100):
    plt.plot(X[k,:,0], X[k,:,1] + k)
    for idx in range(N):
        plt.plot( X[k,idx,0], X[k,idx,1] + k,'b+')
plt.grid()
