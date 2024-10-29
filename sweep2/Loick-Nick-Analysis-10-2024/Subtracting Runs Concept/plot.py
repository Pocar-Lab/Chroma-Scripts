import numpy as np
import matplotlib.pyplot as plt

tall8reflector = np.loadtxt('Tall8Reflector.csv',delimiter=',')
tall4reflector = np.loadtxt('Tall4Reflector.csv',delimiter=',')
tallnoreflector = np.loadtxt('TallNoReflector.csv',delimiter=',')

short8reflector = np.loadtxt('Short8Reflector.csv',delimiter=',')
short4reflector = np.loadtxt('Short4Reflector.csv',delimiter=',')
shortnoreflector = np.loadtxt('ShortNoReflector.csv',delimiter=',')

tall_4_only = tall4reflector-tallnoreflector
tall_8_only = tall8reflector - tall4reflector

short_4_only = short4reflector-shortnoreflector
short_8_only = short8reflector-short4reflector
x_values = np.arange(0, len(tall_4_only) * 0.5, 0.5)

all_arrays = [
    tall8reflector,
    tall4reflector,
    tallnoreflector,
    short8reflector,
    short4reflector,
    shortnoreflector,
    tall_4_only,
    tall_8_only,
    short_4_only,
    short_8_only
]

titles = [
    'Tall 8 Reflector Data',
    'Tall 4 Reflector Data',
    'Tall No Reflector Data',
    'Short 8 Reflector Data',
    'Short 4 Reflector Data',
    'Short No Reflector Data',
    'Difference: Tall 4 Reflector - Tall No Reflector',
    'Difference: Tall 8 Reflector - Tall 4 Reflector',
    'Difference: Short 4 Reflector - Short No Reflector',
    'Difference: Short 8 Reflector - Short 4 Reflector'
]

for i in range(10):
    plt.bar(x_values, all_arrays[i], width=0.5, align='edge')
    plt.title(titles[i])
    plt.savefig(f"{titles[i]}.png", dpi=300)
    plt.close()
