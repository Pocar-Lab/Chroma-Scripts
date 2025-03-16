#!/usr/bin/env python
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
from PocarChroma.analysis_manager import analysis_manager
import time
from PocarChroma.document_manager import document_manager

"""
Example showing how to run a simulation with a script file rather than from the command line.

Here perhaps include description of what the simulation is testing for archival reasons.

Run this file from within the Chroma container with `python ./ExampleAnalysis.py`
"""

def main():
    experiment_name = "IncidentBlocker"
    # experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM" #define experiment
    LABEL = "Incident Hits Blocker" # label configuration or properties

    num_particles = 1_000_000
    seed = 5020
    plots = [
            
           
            "plot_angle_hist" , "plot_all_tracks", "plot_detected_tracks"
            
             ]

    # e = [1, 2, 3, 4, 5, 6, 7, 8] #exclude outer
    # e = [2, 3, 4, 5, 6, 7, 8, 9] #exclude outer

    # e = [9, 10, 11, 12, 13, 14, 15, 16] #exclude outer

    # e = [1, 3, 5, 7] #exclude outer

    # e = [f"reflector{i}" for i in e]
    e = ['reflectorholder1', 'reflectorholder2', 'reflector13', 'reflector14', 'reflector15','reflector16']
    # e = ["copper reflector"]
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Plots: {plots}")
    print(f"Exclusions: {e}")

    gm = geometry_manager(
        experiment_name=experiment_name, exclude=e
    )
    rm = run_manager(
        geometry_manager=gm,
        experiment_name=experiment_name,
        random_seed=seed,
        num_particles=num_particles,
        plots=plots,
        batches=True
    )
    print("Run manager complete")
    
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
    
    # dm = document_manager(rm.ana_man, LABEL)
    # dm.compile()
    #temporary new code:
    #print(rm.ana_man.pte)

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print(f"The simulation run time is: {e - s} s")
