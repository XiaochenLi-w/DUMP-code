import numpy as np

# n = 70187
# k = 900
n = 494352
k = 2000

epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

delta = 1.0e-6

mse = np.zeros(len(epsilon), dtype=float)

for i in range(len(epsilon)):
    mse[i] = 32 / (epsilon[i]**2 * n**2)

print(mse)