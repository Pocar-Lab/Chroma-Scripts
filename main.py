#this is a copy of the current version of main.py from the nEXO-Chroma repo
#it is here to test havin analysis scripts as a separate folder

#!/usr/bin/env python
import pandas as pd
import sys, getopt
import numpy as np

from PocarChroma.geometry_manager import GeometryManager
from PocarChroma.run_manager import RunManager
from PocarChroma.material_manager import MaterialManager
from PocarChroma.surface_manager import SurfaceManager
from PocarChroma.analysis_manager import AnalysisManager

import time

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

    mm = MaterialManager(experiment_name=experiment_name)
    sm = SurfaceManager(material_manager = mm, experiment_name = experiment_name)
    gm = GeometryManager(experiment_name=experiment_name,surf_manager = sm)
    rm = RunManager(geometry_manager=gm,random_seed=seed, num_particles=num_particles, batch_size = 5_000_000)
    photons, photon_tracks, particle_histories = rm.get_simulation_results()
    am = AnalysisManager(
                gm,
                experiment_name,
                plots,
                photons,
                photon_tracks,
                seed,
                particle_histories,
                save = False,
                show = False,
                print = True,
            )    
    
    def save_to_csv(photons, photon_tracks, particle_histories, experiment_name):
        photons_df = pd.DataFrame(photons)
        photon_tracks_df = pd.DataFrame(photon_tracks)
        particle_histories_df = pd.DataFrame(particle_histories)
        
        photons_df.to_csv(f"{experiment_name}_photons.csv", index=False)
        photon_tracks_df.to_csv(f"{experiment_name}_photon_tracks.csv", index=False)
        particle_histories_df.to_csv(f"{experiment_name}_particle_histories.csv", index=False)
        
    # save_to_csv(photons, photon_tracks, particle_histories, experiment_name)

    return am.get_end_time()



if __name__ == '__main__':
	s = time.time()
	e = main()
	print(f'The simulation run time is: {e - s} s')