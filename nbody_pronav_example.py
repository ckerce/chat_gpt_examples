import numpy as np
import pdb
from matplotlib import pyplot as plt

def transverse_velocity_dampening(x, y, vx, gamma_t):
    """
    Calculates the transverse velocity dampening force vector between 
    particles i (at position x) and j (at position y).

    Arguments:
    x -- a numpy array representing the position of particle i 
    y -- a numpy array representing the position of particle j
    vx -- a numpy array representing the velocity of particle i
    gamma_t -- a scalar value representing the dampening coefficient

    Returns:
    A numpy array representing the transverse velocity dampening force vector between particles i and j.
    """
    r = y - x
    r_norm = np.linalg.norm(r)
    if r_norm == 0:
        return np.zeros_like(vx)
    v_parallel = np.dot(vx, r / r_norm) * r / r_norm
    return -gamma_t * (vx - v_parallel)

def velocity_dampening(vx, gamma):
    """
    Calculates the velocity dampening force vector for particle i.

    Arguments:
    vx -- a numpy array representing the velocity of particle i
    gamma -- a scalar value representing the dampening coefficient

    Returns:
    A numpy array representing the velocity dampening force vector for particle i.
    """
    return -gamma * vx


def proportional_navigation(x, y, v, alpha, beta):
    """
    Calculates the proportional navigation force vector for particle i (at position x).

    Arguments:
    x -- a numpy array representing the position of particle i 
    y -- a numpy array representing the position of particle j 
    v -- a numpy array representing the velocity of particle i
    alpha -- a scalar value representing the proportionality constant
    beta -- a scalar value representing the relative weight of the navigation versus the pure pursuit

    Returns:
    A numpy array representing the proportional navigation force vector for particle i.
    """
    r = y - x
    r_norm = np.linalg.norm(r)
    if r_norm == 0:
        return np.zeros_like(v)
    v_hat = v / (1e-8 + np.linalg.norm(v))
    r_hat = r / r_norm
    s = np.cross(v_hat, r_hat)
    return alpha * np.linalg.norm(v) * s + beta * r_hat

def desired_position(x,v,D):
    """
    Calculates the desired position for particle i.

    Arguments:
    x -- a numpy array representing the position of particle i
    v -- a numpy array representing the velocity of particle i
    D -- a scalar value representing the desired separation distance between particles i and j

    Returns:
    A numpy array representing the desired position for particle i.
    """

    v_norm =  np.linalg.norm(v)
    if v_norm > 0:
       v_hat = v / np.linalg.norm(v)
    else:
       v_hat = np.zeros_like(v)
    return x - D * v_hat

def make_movie():
    """
    Creates a sequence of plots for a particle simulation and saves them as jpg files.
    """

    count = 0
    for k in range(0,5001,25):
        plt.figure()
        plt.plot(X[k,:,0], X[k,:,1],'-+')
        plt.ylim(-1.1,1.1)
        plt.xlim(-1, 60)
        plt.grid()
        plt.savefig('plt'+str(count).zfill(4)+'.jpg')
        count+=1
        plt.close()


#if __name__ == '__main__':
# Section: Parameters
N = 10
alpha = 2.
beta = 4.
D = 1.
gamma = 2.5
gamma_t = 5.

# Section: Inter-agent coupling mask
epsilon = np.zeros((N,N))
epsilon[:-1, 1:] = np.identity(N - 1)
np.fill_diagonal(epsilon, 0)

# Section: Agent initial positions and velocities
x = np.zeros((N, 2))
v = np.zeros((N, 2))

x[:,0] = np.linspace(0,N-1,N)
x[:,1] = np.sin( np.linspace(0,2*np.pi, N))
v[-1:,0] = 1

X = [x.copy()]
V = [v.copy()]

# Section: Simulation
T = 50
dt = 0.01
timesteps = int(T / dt)
for step in range(timesteps):
    # Calculate pairwise forces using proportional navigation as the control law
    F = np.zeros_like(x)
    for i in range(N):
        for j in range(i, N):
            if epsilon[i, j]:
                x_desired = desired_position(x[j], v[j], D)
                F[i] += proportional_navigation(x[i], x_desired, v[i], alpha, beta)
                F[i] += transverse_velocity_dampening(x[i], x[j], v[i], gamma_t)
    for i in range(N-1):
        F[i] += velocity_dampening(v[i], gamma)

    # Update positions and velocities
    x += v * dt + 0.5 * F * dt**2
    v += 0.5 * F * dt
    X.append(x.copy())
    V.append(v.copy())

X = np.array(X)
V = np.array(V)

# Section: Plot outputs
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

