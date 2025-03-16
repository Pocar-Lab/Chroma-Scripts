import numpy as np

standard_wavelengths = np.arange(60, 1000, 5).astype(np.float32)
num_wavelengths = len(standard_wavelengths)
num_angles = 10

data = np.zeros((num_angles, num_wavelengths))
for i in range(num_angles):
    for j in range(num_wavelengths):
        data[i][j] = i/num_angles + j/(10 * num_wavelengths)

np.savetxt("data.csv", data, delimiter=",")
