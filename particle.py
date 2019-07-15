
import numpy as np

class Particle:
    def __init__(self, r, v, m,ra):
        self.pos = np.array(r, dtype=np.double)
        self.velocity = np.array(v, dtype=np.double)
        self.mass = m
        self.radius = ra

        self.line = None  # die "Spur" der Partikel, wird zwischen jeder Frame weggewischt und besteht in jeder Frame nur aus einem Punkt

        self.__orig_pos = self.pos
        self.__orig_velocity = self.velocity

    def reset(self):
        self.pos = self.__orig_pos
        self.velocity = self.__orig_velocity

    def __str__(self):
        return "{p: %s, v: %s}" % (str(self.pos), str(self.velocity))
