
import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as anim

from typing import List
from particle import Particle


class System2d:
    def __init__(self, particles: List[Particle], dt, G=6.67430e-11):
        self.particles = particles
        self.dt = dt
        self.G = G

        self.elapsed = 0
        self.mscale = 1e-3
        self.rscale = 1e-11

        self.figure = plt.figure(figsize=(15, 15))  # Grösse Anzeige & Leerer Rahmen
        axes = plt.axes(xlim=(-2, 2), ylim=(-2, 2))  # Skalierung Rahmen
        axes.autoscale(False)  # ich will eine fixe Skalierung
        

        for part in particles:
            part.line = axes.plot([], [], "o")[0]  # EINE leere Linie zum Plotten der Partikel, wird nur einen Punkt enthalten


    def init_anmiation(self): 
        l = []
        for part in self.particles:  # für jede Partikel...
            part.line.set_data([], [])  # werde den Partikelpunkt auf der Linie wegwischen sozusagen
            l.append(part.line)  # und füge die nun leere Linie der Liste l hinzu
        return l  # und mein return ist die Liste von leeren Linien, also konkret das Wegwischen des Bildes

    def animate(self, step):
        self.step()
        l = []
        for part in self.particles:
            part.line.set_data(*(part.pos * self.rscale))
            part.line.set_markersize(np.cbrt(np.sqrt(part.mass)) * self.mscale)
            l.append(part.line)
        return l  # 

    def reset(self):
        self.elapsed = 0
        for p in self.particles:
            p.reset()

    def step(self):
        for part in self.particles:
            part.pos += part.velocity * self.dt

            a = 0
            for j in self.particles:
                if part == j:
                    continue
                r = j.pos - part.pos
                le = np.sum(r ** 2)
                a += self.G * j.mass / le * r / np.sqrt(le)

            part.velocity += a * self.dt

        self.elapsed += self.dt

    def render(self):
        for part in self.particles:
            plt.scatter(*(part.pos * self.rscale), s=np.sqrt(math.log(part.mass, 10)) * self.mscale)
        plt.show()

    def start(self, frames):
        a = anim.FuncAnimation(self.figure, self.animate, init_func=self.init_anmiation, frames=frames, interval=1)
        a.save('/tmp/basic_animation.mp4', fps=30)

        plt.show()
