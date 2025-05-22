#!/usr/bin/env python
from PocarChroma.geometry_manager import GeometryManager
from PocarChroma.run_manager import RunManager
from PocarChroma.material_manager import MaterialManager
from PocarChroma.surface_manager import SurfaceManager
from PocarChroma.analysis_manager import AnalysisManager
# from PocarChroma.document_manager import document_manager

import time
import numpy as np
import csv

"""
Example showing how to run a simulation with a script file rather than from the command line.

Here perhaps include description of what the simulation is testing for archival reasons.

Run this file from within the Chroma container with `python ./ExampleAnalysis.py`
"""

def sweep(value):
    
    experiment_name = "corrected_copper"
    num_particles = 1_000_000
    seed = np.random.randint(0,10000)
    plots = []

    # e = ["reflectorholder1","reflectorholder2"]

    mm = MaterialManager(experiment_name=experiment_name)
    mm.material_props["copper"]["eta"] = value
    mm.material_props["copper"]["k"] = 0.5


    sm = SurfaceManager(material_manager = mm, experiment_name = experiment_name)
    # sm.overwrite_property("Cu-Xe", "reflect_specular", value)
    # sm.overwrite_property("Cu-Xe", "reflect_diffuse", 1-value)
    gm = GeometryManager(experiment_name=experiment_name,surf_manager = sm)
    rm = RunManager(geometry_manager=gm,random_seed=seed, num_particles=num_particles, batch_size = 2_500_000)
    
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
    return am.photon_transport_efficiency


if __name__ == "__main__":
    
    ptes = []
    
    Scattering = np.linspace(1.2, 1.2, 1)
    
    for i in range(len(Scattering)):
        pte = sweep(Scattering[i])  # Get PTE value for the current Xe_value
        
        with open('ptes_data_copper_refl.csv', 'a', newline='') as file:  # Open file in append mode
            writer = csv.writer(file)
            
            # Write header only if the file is empty
            if file.tell() == 0:  # Check if file is empty
                writer.writerow(['n value (k = 0.5)', 'PTE'])  # Write header
                
            writer.writerow([Scattering[i], pte])  # Write the current data row

    
    
