# Chat GPT Examples

Like everyone else in the world, I've been looking at how ChatGPT can both simplify my coding life and help me communicate coding concepts more qickly to my colleagues.  I'll post examples here as they seem relevant to communicating a point.

# N-Agent "follow the leader" control law.
The [nbody_example.py](nbody_example.py) Python program simulates N-body dynamics using a pairwise virtual force law based on velocity dampening, transverse velocity dampening, and a directed version of Hooke's law. This control law is designed to simulate a group of agents, where the lead agent (Nth agent) follows a prescribed path, and the other agents follow along using a virtual force law between each successive pair of agents.

The interaction dynamics of the agents are described by a virtualized Newton's laws of motion, which relate the control acting on an object to its acceleration. In this case, we implement this concept using a virtual force to simulate the interaction between the agents. The virtual force acting on an agent is determined by the relative positions and velocities of the agents.

The virtual force law is forward-looking in the sense that the connectivity graph does not have loops. This is because loops can lead to feedback oscillations. To prevent this, we use a directed virtual Hooke's law.

The main function of the example program uses the three force calculation functions to simulate the positions and velocities of a set of particles. The program initializes the positions and velocities of 10 particles and runs the simulation for a given number of time steps, updating the positions and velocities at each step based on the forces acting on the particles.

The program uses the NumPy library to perform vectorized calculations, which allows for faster and more efficient computation. The code is structured using function definitions and clear documentation to improve readability and maintainability. The program also includes an if statement to allow it to be imported as a module or run as a standalone script.
![One agent leading nine others](./follow_the_leader.gif)

# Proportional Navigation for the <br> N-Agent "follow the leader" control law.
In the [nbody_pronav_example.py](nbody_pronav_example.py) program, we modify the virtual force law used in the previous example to use **proportional navigation**. Proportional navigation is a guidance law commonly used in missile intercept systems. The guidance law is based on the principle of parallel navigation, which states that an interceptor must fly a path that is parallel to the path of the target, but with a time delay.

In our case, we use proportional navigation to position each agent into a specified relative position behind the agent they are following. If an agent with coordinates **x** is following an agent with coordinates **y** and velocity **vy**, then the virtual position that agent **x** attempts to achieve at that moment is **y - D * vy/norm(vy)**, where **D** is the intended follow distance.

The main function of the example program is similar to the previous example, but incorporating the proportional navigation virtual force law in place of the virtualized Hooke's Law. The program initializes the positions and velocities of 10 particles and runs the simulation for a given number of time steps, updating the positions and velocities at each step based on the forces acting on the particles.

![One agent leading nine others](./pronav_follow_the_leader.gif)
