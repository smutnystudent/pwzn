#Marta Kajkowska
import argparse
import numpy as np
from PIL import Image
from rich.progress import track

parser = argparse.ArgumentParser()
parser.add_argument('size', help="rozmiar siatki", type=int)
parser.add_argument('J', help="całka wymiany", type=float)
parser.add_argument('beta', help="1/kT", type=float)
parser.add_argument('B', help="wartość pola", type=float)
parser.add_argument('steps', help="liczba kroków symulacji", type=int)
parser.add_argument('-sd', '--spin_density', help="początkowa gęstość spinów", type=float, default=0.5)
parser.add_argument('-f', '--file', help="nazwa pliku", default="step")
args = parser.parse_args()

class simulation:
    def __init__(self, size, J, beta, B, steps, spin_density, file):
        self.size = size
        self.J = J
        self.beta = beta
        self.B = B
        self.steps = steps
        self.spin_density = spin_density
        self.file = file
        self.spins = -np.ones((size, size))
        for i in range(int(self.spin_density*(self.size**2))):
            c = 0
            while c == 0:
                x = np.random.randint(self.size)
                y = np.random.randint(self.size)
                if self.spins[(x, y)] == -1:
                    self.spins[(x, y)] = 1
                    c = 666
        for step in track(range(self.steps)):
            for i in range(self.size**2):
                x = np.random.randint(self.size)
                y = np.random.randint(self.size)
                dE = 2 * self.B * self.spins[(x, y)]
                if x > 0:
                    dE += 2 * self.J * self.spins[(x, y)] * self.spins[(x-1, y)]
                if y > 0:
                    dE += 2 * self.J * self.spins[(x, y)] * self.spins[(x, y-1)]
                if x < self.size - 1:
                    dE += 2 * self.J * self.spins[(x, y)] * self.spins[(x+1, y)]
                if y < self.size - 1:
                    dE += 2 * self.J * self.spins[(x, y)] * self.spins[(x, y+1)]
                if dE < 0 or np.random.rand() < np.exp(-dE*self.beta):
                    self.spins[(x, y)] *= -1
            image = np.zeros((self.size, self.size))
            for i in range(self.size):
                for j in range(self.size):
                    if self.spins[(i, j)] == -1:
                        image[(i, j)] = 0
                    else:
                        image[(i, j)] = 255
            img = Image.fromarray(image)
            img = img.convert('RGB')
            img.save(self.file+str(step)+".jpg")
sim = simulation(args.size, args.J, args.beta, args.B, args.steps, args.spin_density, args.file)

