# chat_gpt_examples

Like everyone else in the world, I've been looking at how ChatGPT can both simplify my coding life and help me communicate coding concepts more qickly to my colleagues.

# N-Agent "follow the leader" control law.
As ChatGPT helped to summarize, the **nbody_example.py** Python program simulates N-body dynamics using the pairwise virtual force laws based on velocity dampening, transverse velocity dampening, and a directed version of Hooke's law. The lead agent (N'th agent) is prescribed a path, and the other agents follow along using a virtual force law between each successive pair of agents.  Note that the force law is forward looking in the sense that the connectivity graph does not have loops.  It is well known that such loops lead to feedback oscillations.

Take a look at the comments in the [here](nbody_example.py) **nbody_example.py** file to see the string of prompts that lead to this function.

The main function of the example program uses the three force calculation functions to simulate the positions and velocities of a set of particles. The program initializes the positions and velocities of 10 particles and runs the simulation for a given number of time steps, updating the positions and velocities at each step based on the forces acting on the particles. 

The program uses the NumPy library to perform vectorized calculations, which allows for faster and more efficient computation. The code is structured using function definitions and clear documentation to improve readability and maintainability. The program also includes an if statement to allow it to be imported as a module or run as a standalone script.

![One agent leading nine others](./follow_the_leader.gif)

# Using Proportional Navigation for <br> N-Agent "follow the leader" control law.
This is the same as before, except that a virtual force is created to position each agent into a specified relative position behind the agent they are following.  If an agent with coordinates x (agent_x) is following an agent with coordiantes y and velocity vy, then the virtual position that agent_x attemps to achieve at that moment is y - D * vy/norm(vy).  The parameter D is the intended follow distance.

![One agent leading nine others](./pronav_follow_the_leader.gif)
