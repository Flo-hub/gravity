
import math
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as anim

from typing import List
from particle import Particle


class System2d:
    def __init__(self, particles: List[Particle], dt, G=6.67430e-11):
        self.particles = particles  # Liste der Körper im System
        self.dt = dt  # Zeitschritt
        self.G = G  # Gravitationskonstante

        self.elapsed = 0  # die Uhr wird bei jedem Zeitschritt ticken
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
            part.line.set_data(*(part.pos * self.rscale))  # positionieren die Partikel und skaliere damit sie man im fixierten Rahmen sehen kann
            part.line.set_markersize(np.cbrt(np.sqrt(part.mass)) * self.mscale)  #damit die Skalierung der Planetengrösse klappt ist hier die Masse proportional zum Radius hoch 6 statt hoch 3
            l.append(part.line)
        return l  

    def reset(self):
        self.elapsed = 0
        for p in self.particles:
            p.reset()

    def step(self):
        for part in self.particles:
            part.pos += part.velocity * self.dt  # die Position wird aktualisiert

            a = 0  # nun wird die Geschwindigkeit nach ein Paar Fallunterscheidungen aktualisiert:
            for j in self.particles:
                if part == j or j.mass == 0:  # eine Partikel interagiert nicht mit sich selbst, auch nicht mit (durch Kollision) verschwundenen Partikeln
                    continue
                r = j.pos - part.pos
                le = np.sum(r ** 2)
                if np.sqrt(le) <= part.radius + j.radius:  # falls sie sich berühren kollidieren die Körper
                    part.mass = (part.mass * part.velocity + j.mass * j.velocity) / (part.mass + j.mass)  # kollidierende schwere Körper bleiben meistens aneinander heften mit Impulserhaltung
                    part.pos =  0,5 * (part.pos + j.pos)  # wir setzen grob den Schwerpunkt in der Mitte... 
                    j.mass = 0   #...und lassen den Körper j verschwinden, d.h. es kann nicht mehr interagieren und ist auf der Animation nicht mehr zu sehen, vgl l.42 
                    continue
                a += self.G * j.mass / le * r / np.sqrt(le)  # wir berechnen Schritt für Schritt die resultierende Beschleunigung...

            part.velocity += a * self.dt  #...und aktualisieren die Geschwindigkeit

        self.elapsed += self.dt  # die Uhr tickt
        for part in self.particles:
            if part.mass == 0: 
                self.particles.remove(part)  # verschwundene Körper verschwinden nun auch aus der Liste

    def render(self):
        for part in self.particles:
            plt.scatter(*(part.pos * self.rscale), s=np.sqrt(math.log(part.mass, 10)) * self.mscale)
        plt.show()

    def start(self, frames):
        a = anim.FuncAnimation(self.figure, self.animate, init_func=self.init_anmiation, frames=frames*365, interval=1)
        a.save('/tmp/basic_animation.mp4', fps=30)

        plt.show()
