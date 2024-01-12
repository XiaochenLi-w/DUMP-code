import numpy as np

# n = 70187
# k = 900
n = 494352
k = 2000

epsilon = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

delta = 1.0e-8

mse = np.zeros(len(epsilon), dtype=float)

tau = np.log(n)

for i in range(len(epsilon)):
    rho = np.log( 2 / delta) / epsilon[i]**2
    #mse[i] = np.log( 1 / delta) / (epsilon[i]**2 * n**2)
    temp = np.power(2, -tau)
    mse[i] = temp / (n * (1 - temp)) + n * rho * temp / (n**2 * (1 - temp))

print(mse)