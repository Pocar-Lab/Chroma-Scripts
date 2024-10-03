#!/usr/bin/env python
#this was very much copied from Lucs sweep file
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
from PocarChroma.surface_manager import surface_manager
from PocarChroma.material_manager import material_manager
import time
import numpy as np
from pprint import pprint
"""
Example showing how to run a simulation with a script file rather than from the command line.

Here perhaps include description of what the simulation is testing for archival reasons.

Run this file from within the Chroma container with `python ./ExampleAnalysis.py`
"""


from functools import partial
from tqdm import tqdm
from tqdm.contrib import itertools

from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout(): #custom context to not print things
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout



def run_simulation(n_si, k_si,experiment_name, e):
    """
    Run  8 reflector simulation, return results
    """
    num_particles = 2_000_000
    seed = 1130
    visualize = False
    plots = []
    mm = material_manager(experiment_name) 
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = surface_manager(mm, experiment_name) 
    gm = geometry_manager(
        experiment_name=experiment_name,
        surf_manager=sm,
        exclude = e
    )
    fail_counter = 0
    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = run_manager(
                geometry_manager=gm,
                experiment_name=experiment_name,
                random_seed=seed,
                num_particles=num_particles,
                plots=plots,
            )
        except Exception as e:
            fail_counter += 1
            print("meow")
            if fail_counter == 3:
                print("failed 3 times")
                print(e)
                raise e
                exit()
            continue
        break

    pte = rm.ana_man.photon_transmission_efficiency

    return pte, rm.ana_man.pte_st_dev
#     e_outer_sebastian = [f"reflector{i}" for i in [4,6,7,8]]

def run_tall_batch(n_si, k_si):
    experiment_name = '8Silicon35_87' 
    pte_8, pte_err_8 = run_simulation(n_si, k_si, experiment_name, None)
    e_outer= [f"reflector{i}" for i in [1,3,5,7]]
    pte_4, pte_err_4 = run_simulation(n_si,k_si, experiment_name, e = e_outer)
  
    return pte_8, pte_err_8, pte_4, pte_err_4

def run_short_batch(n_si, k_si):
    experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM"
    pte_8, pte_err_8 = run_simulation(n_si, k_si, experiment_name, None)
    e_outer= [f"reflector{i}" for i in [4,6,7,8]]
    pte_4, pte_err_4 = run_simulation(n_si,k_si, experiment_name, e = e_outer)
  
    return pte_8, pte_err_8, pte_4, pte_err_4

def main():
    import csv

    # CSV filename
    csv_filename = f"tall_silicon_complex_sweep.csv"

    # Open the CSV file in append mode and write the header once
    with open(csv_filename, 'a+', newline='') as csvfile:
        fieldnames = ['k_si', 'n_si', 'pte_8', 'pte_8_error', 'pte_4', 'pte_4_error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is empty
        csvfile.seek(0)
        if csvfile.read(1) == "":
            writer.writeheader()

    for k_si, n_si in itertools.product(np.linspace(.74, .96, 12), np.linspace(1.71, 2.08, 18)):
            with suppress_stdout(): #suppress output to not clog up the log
                pte_8, pte_err_8, pte_4, pte_err_4 = run_tall_batch(n_si, k_si) #run 8 reflector

                #compile results and info
                result = { 
                    'k_si': k_si,
                    'n_si': n_si,
                    'pte_8': pte_8,
                    'pte_8_error': pte_err_8,
                    "pte_4": pte_4,
                    "pte_4_error": pte_err_4
                }

            with open(csv_filename, 'a+', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(result)



if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print(f"The simulation run time is: {e - s} s")
