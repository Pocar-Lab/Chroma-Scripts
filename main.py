#this is a copy of the current version of main.py from the nEXO-Chroma repo
#it is here to test havin analysis scripts as a separate folder

#!/usr/bin/env python
import pandas as pd
import sys, getopt
import numpy as np

from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
from PocarChroma.material_manager import material_manager
from PocarChroma.surface_manager import surface_manager
from PocarChroma.analysis_manager import analysis_manager

import time
def overwrite_scattering_length(filepath = 'Chroma-Scripts/data_files/bulk_materials_starter.csv', new_value = 100):
    df = pd.read_csv(filepath)
    df['scattering_length'] = new_value
    df.to_csv(filepath, index = False)

def usage():
    print ("=====================================================================")
    print ("  The minimum paramaters the simulation needs are:")
    print ("    (1) '-e' <Str>              name of experiment to be simulated.")
    print ("  Additional options can be chosen:")
    print ("  	(2) '-n' <#>	            number of photons to be simulated.") 
    print ("  	(3) '-s' <#>                choose the seed number")
    print ("    (4) '-p' <Str1,Str2,...>    choose which plots to run")
    print ("=====================================================================")

def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, "n:s:r:e:p:")
    except getopt.GetoptError as err:
        print(f"Error: {err}")
        usage()
        sys.exit()

    experiment_name = None
    num_particles = 1_000_000
    seed = np.random.randint(0,1000000)
    plots = []

    for opt, arg in opts:
        if opt == '-e':
            experiment_name = str(arg)
        elif opt == '-n':
            num_particles = int(arg)
        elif opt == '-s':
            seed = int(arg)
        elif opt == '-p':
            plots = [i.strip() for i in arg.split(',')]


    if not experiment_name:
        print("Please Input an Experiment Name")
        usage()
        sys.exit()

    print(f"{'Experiment Name:':<25} {experiment_name:>27}")
    print(f"{'Number of Particles:':<25} {num_particles:>27}")
    print(f"{'Seed:':<25} {seed:>27}")

    if len(plots) > 0:
        print(f"{'Plots:':<25} {', '.join(plots):>27}")
    else:
        print(f"{'Plots:':<25} {'None':>27}")

    mm = material_manager(experiment_name=experiment_name)
    sm = surface_manager(material_manager = mm, experiment_name = experiment_name)
    gm = geometry_manager(experiment_name=experiment_name,surf_manager = sm)
    rm = run_manager(geometry_manager=gm, experiment_name=experiment_name, random_seed=seed, num_particles=num_particles,plots=plots)
    photons, photon_tracks, particle_histories = rm.get_simulation_results()
    am = analysis_manager(
                gm,
                experiment_name,
                plots,
                photons,
                photon_tracks,
                seed,
                particle_histories,
                save = False,
                show = True,
            )    
    return am.get_end_time()



if __name__ == '__main__':
	s = time.time()
	e = main()
	print(f'The simulation run time is: {e - s} s')