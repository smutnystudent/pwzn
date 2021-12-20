from numba import jit
import argparse
import numpy as np
from PIL import Image
from rich.progress import track
import matplotlib.pyplot as plt
from time import time


parser = argparse.ArgumentParser()
parser.add_argument('size', help="rozmiar siatki", type=int)
parser.add_argument('J', help="całka wymiany", type=float)
parser.add_argument('beta', help="1/kT", type=float)
parser.add_argument('B', help="wartość pola", type=float)
parser.add_argument('steps', help="liczba kroków symulacji", type=int)
parser.add_argument('-sd', '--spin_density', help="początkowa gęstość spinów", type=float, default=0.5)
parser.add_argument('-f', '--file', help="nazwa pliku", default="step")
parser.add_argument('-m', '--file2', help="nazwa pliku 2", default="magnetyzacja")
args = parser.parse_args()

@jit(nopython = True)
def function(size, spin_density, steps, spins, J, beta, B):
    m = -(size ** 2)
    steps1 = np.zeros(steps + 1)
    mag = np.zeros(steps + 1)
    for i in range(int(spin_density * (size ** 2))):
        c = 0
        while c == 0:
            x = np.random.randint(size)
            y = np.random.randint(size)
            if spins[(x, y)] == -1:
                spins[(x, y)] = 1
                m += 2 * spins[(x, y)]
                c = 666
    steps1[0] = 0
    mag[0] = m
    for step in range(steps):
        for i in range(size ** 2):
            x = np.random.randint(size)
            y = np.random.randint(size)
            dE = 2 * B * spins[(x, y)]
            if x > 0:
                dE += 2 * J * spins[(x, y)] * spins[(x - 1, y)]
            if y > 0:
                dE += 2 * J * spins[(x, y)] * spins[(x, y - 1)]
            if x < size - 1:
                dE += 2 * J * spins[(x, y)] * spins[(x + 1, y)]
            if y < size - 1:
                dE += 2 * J * spins[(x, y)] * spins[(x, y + 1)]
            if dE < 0 or np.random.rand() < np.exp(-dE * beta):
                spins[(x, y)] *= -1
                m += 2 * spins[(x, y)]
        steps1[step + 1] = step
        mag[step + 1] = m

def function2(size, spin_density, steps, spins, J, beta, B):
    m = -(size ** 2)
    steps1 = np.zeros(steps + 1)
    mag = np.zeros(steps + 1)
    for i in range(int(spin_density * (size**2))):
        c = 0
        while c == 0:
            x = np.random.randint(size)
            y = np.random.randint(size)
            if spins[(x, y)] == -1:
                spins[(x, y)] = 1
                m += 2 * spins[(x, y)]
                c = 666
    steps1[0] = 0
    mag[0] = m
    for step in range(steps):
        for i in range(size ** 2):
            x = np.random.randint(size)
            y = np.random.randint(size)
            dE = 2 * B * spins[(x, y)]
            if x > 0:
                dE += 2 * J * spins[(x, y)] * spins[(x - 1, y)]
            if y > 0:
                dE += 2 * J * spins[(x, y)] * spins[(x, y - 1)]
            if x < size - 1:
                dE += 2 * J * spins[(x, y)] * spins[(x + 1, y)]
            if y < size - 1:
                dE += 2 * J * spins[(x, y)] * spins[(x, y + 1)]
            if dE < 0 or np.random.rand() < np.exp(-dE * beta):
                spins[(x, y)] *= -1
                m += 2 * spins[(x, y)]
        steps1[step + 1] = step
        mag[step + 1] = m

class simulation:
    def __init__(self, size, J, beta, B, steps, spin_density, file, file2):
        self.size = size
        self.J = J
        self.beta = beta
        self.B = B
        self.steps = steps
        self.spin_density = spin_density
        self.file = file
        self.spins = -np.ones((size, size))
        self.file2 = file2
        t1 = time()
        function(self.size, self.spin_density, self.steps, self.spins, self.J, self.beta, self.B)
        t2 = time()
        print("z numbą: ", t2-t1, "s")
        self.spins = -np.ones((size, size))
        t1 = time()
        function2(self.size, self.spin_density, self.steps, self.spins, self.J, self.beta, self.B)
        t2 = time()
        print("bez numby: ", t2-t1, "s")

sim = simulation(args.size, args.J, args.beta, args.B, args.steps, args.spin_density, args.file, args.file2)


