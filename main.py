

import numpy as np

from particle import Particle
from system import System2d

def main():
    p = []
    p.append(Particle((0, 0), (0, 0), 2e30))  # sun
    p.append(Particle((-5.8e10, 0), (0, -47873), 3.3e23))  # mercury
    p.append(Particle((1.5e11, 0), (0, 30000), 6e24))  # earth

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