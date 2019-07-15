

import numpy as np

from particle import Particle
from system import System2d

def main():
    p = []
    p.append(Particle((0, 0), (0, 0), 2e30))  # sun
    p.append(Particle((-5.8e10, 0), (0, -47873), 3.3e23, 2.44e6))  # mercury
    p.append(Particle((0,-1.1e11), (35021,0), 4.87e24, 6.10e6))  # venus
    p.append(Particle((1.5e11, 0), (0, 30000), 5.97e24, 6.38e6))  # earth
    p.append(Particle((3.48e8+1.5e11,0), (0,31000), 7.35e22, 3.48e6))  #moon
    p.append(Particle((0,2.3e11), (-24131,0), 0.64e24, 3.40e6))  # mars

    system = System2d(p, 3600 * 24)
    # system.render()
    # for i in range(10000):
    #     system.step()
    #     # system.render()
    #     # print(np.linalg.norm(system.particles[0].pos - system.particles[1].pos))
    # system.render()

    system.start(365)





if __name__ == "__main__":
    main()
