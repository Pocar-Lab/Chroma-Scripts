#!/usr/bin/env python
from PocarChroma.geometry_manager import GeometryManager
from PocarChroma.run_manager import RunManager
from PocarChroma.material_manager import MaterialManager
from PocarChroma.surface_manager import SurfaceManager
from PocarChroma.analysis_manager import AnalysisManager
# from PocarChroma.document_manager import document_manager

import time
import numpy as np

"""
Example showing how to run a simulation with a script file rather than from the command line.

Here perhaps include description of what the simulation is testing for archival reasons.

Run this file from within the Chroma container with `python ./ExampleAnalysis.py`
"""

def main():
    experiment_name = "8Silicon35_87"
    # experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM" #define experiment
    LABEL = "SHORT-INNER-SPECULAR-REFLECTOR" # label configuration or properties

    num_particles = 2_000_000
    seed = np.random.randint(0,10000)
    plots = [
            # "plot_all_tracks" ,
            # "plot_detected_tracks" ,
            # "plot_undetected_tracks" ,
            # "plot_reflected_tracks" ,
            # "plot_filtered_scattered_tracks" ,
            # "plot_detected_reflected_tracks" ,
            # "plot_specular_reflected_tracks" ,
            # "plot_diffuse_reflected_tracks" ,
            # "plot_refl_multiplicity" ,
            # "photon_shooting_angle" ,
            # "photon_incident_angle_emission_angle_correlation" ,
            # "plot_angle_hist" ,
            # "plot_refl_angle" ,
            # "plot_position_hist" ,
             ]

    # e = [1, 2, 3, 4, 5, 6, 7, 8] #exclude outer
    # e = [2, 3, 4, 5, 6, 7, 8, 9] #exclude outer
    # e = [4,6,7,8] # excludes short silicon outer
    # e = [9, 10, 11, 12, 13, 14, 15, 16] #exclude outer

    e = [1, 3, 5, 7] #exclude outer

    e = [f"reflector{i}" for i in e]
    # e = None
    # e = ["copper reflector"]
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Plots: {plots}")
    print(f"Exclusions: {e}")

    gm = GeometryManager(
        experiment_name=experiment_name, exclude=e
    )
    rm = RunManager(
        geometry_manager=gm,
        random_seed=seed,
        num_particles=num_particles,
    )
    print("Run manager complete")
    
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
    # dm = document_manager(am, LABEL)
    # dm.compile()

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print(f"The simulation run time is: {e - s} s")
    
    
