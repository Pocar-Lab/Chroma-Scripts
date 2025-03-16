import os 
import csv
import numpy as np
import pandas as pd
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
import time
from PocarChroma.document_manager import document_manager
def overwrite_scattering_length(filepath, new_value):
    df = pd.read_csv(filepath)
    df['scattering_length'] = new_value
    df.to_csv(filepath, index = False)
    
def appending_to_csv(scattering_length, PTE):
    df = pd.DataFrame({'scattering_length': [scattering_length], 'PTE_value': [PTE]})
    if not os.path.exists('Project1_data_no_copper_reflection.csv'):
        df.to_csv('Project1_data_no_copper_reflection.csv', mode = 'a', header = True, index = False )
    else:
        df.to_csv('Project1_data_no_copper_reflection.csv', mode = 'a', header = False, index = False )
        
def main():
    experiment_name = "copper_reflector_2023.08.06"
    filepath = f'/workspace/data_files/data/{experiment_name}/bulk_materials_{experiment_name}.csv'
    e = ['copper reflector','copper plate 1', 'copper plate 2']
    num_particles = 10_000_000
    seed = 5020
    plots = [] 
    for i in np.arange(100,402,2):
        overwrite_scattering_length(filepath, i)
        
        gm = geometry_manager(
        experiment_name=experiment_name, exclude=e)
        
        rm = run_manager(
        geometry_manager=gm,
        experiment_name=experiment_name,
        random_seed=seed,
        num_particles=num_particles,
        plots = plots,
        batches=True)
        PTE = rm.ana_man.photon_transmission_efficiency
        appending_to_csv(i, PTE)
if __name__ == '__main__':
    main()

        
