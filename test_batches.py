#this is a copy of the current version of main.py from the nEXO-Chroma repo
#it is here to test havin analysis scripts as a separate folder

#!/usr/bin/env python

import sys, getopt
import numpy as np

from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
from PocarChroma.material_manager import material_manager
from PocarChroma.surface_manager import surface_manager

import time

def main():


    experiment_name = "8Silicon35_87"

    num_particles = 8_000_000
    seed = 12345
    mm = material_manager(experiment_name=experiment_name)
    sm = surface_manager(material_manager = mm, experiment_name = experiment_name)
    gm = geometry_manager(experiment_name=experiment_name,surf_manager = sm)
    rm = run_manager(geometry_manager=gm, experiment_name=experiment_name, random_seed=seed, num_particles=num_particles,plots=[], batches = True)

    large_det = np.sum(rm.ana_man.tallies["SURFACE_DETECT"])

    small_det = []

    for i in range(int(num_particles/2_000_000)):
        seed = 12345 + i
        num_particles = 2_000_000
        mm = material_manager(experiment_name=experiment_name)
        sm = surface_manager(material_manager = mm, experiment_name = experiment_name)
        gm = geometry_manager(experiment_name=experiment_name,surf_manager = sm)
        rm = run_manager(geometry_manager=gm, experiment_name=experiment_name, random_seed=seed, num_particles=num_particles,plots=[])

        small_det.append(np.sum(rm.ana_man.tallies["SURFACE_DETECT"]))
    
    print(large_det)
    print(small_det)
    print(np.sum(small_det))


if __name__ == '__main__':
	main()
