#!/usr/bin/env python
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager, primary_generator
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


import multiprocessing
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


class LEDGenerator(primary_generator):
    def __init__(self, num_particles, center_pos=[0, 0, 0], r=0, source_type="isotropic", beam_theta=0, beam_phi=0):
        super().__init__(num_particles, center_pos, r, source_type, beam_theta, beam_phi)
        self.wavelengths = np.ones(self.num_particles) * 310.0



def run_half_reflectors(n_si, k_si, spec_r, run_id):
    """
    Run  8 reflector simulation, return results
    """
    experiment_name = "8HalfReflectors28_56"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Run ID: {run_id}")
    print(f"Visualize: {visualize}")
    print(f"Plots: {plots}")
    print(f"k_si={k_si}, n_si={n_si}")
    ptes = []
    ptes_err = []
    mm = material_manager(experiment_name) 
    #mm.add_attributes(mm.materials["liquid xenon"], refractive_index=n_xe)
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        # run_id=run_id, 
        # visualize=visualize,
        surf_manager=sm
    )
    fail_counter = 0

    pg = LEDGenerator(num_particles, center_pos=gm.get_solid_center(name="source"))

    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = run_manager(
                geometry_manager=gm,
                experiment_name=experiment_name,
                random_seed=seed,
                num_particles=num_particles,
                # run_id=run_id,
                plots=plots,
                pg=pg
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

def run_LED_reflector(n_si, k_si, spec_r, run_id):
    """
    Run 4 reflector config with LED wavelength
    """
    experiment_name = "TiltedReflectors"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    # exclusion = [1, 3, 5, 7]
    exclusion = []
    excluded = [f"reflector{i}" for i in exclusion]
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Run ID: {run_id}")
    print(f"Visualize: {visualize}")
    print(f"Plots: {plots}")
    print(f"k_si={k_si}, n_si={n_si}")
    print(f"excluded: {excluded}")
    ptes = []
    ptes_err = []
    mm = material_manager(experiment_name) 
    #mm.add_attributes(mm.materials["liquid xenon"], refractive_index=n_xe)
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        surf_manager=sm,
        # exclude=excluded
    )
    fail_counter = 0

    # pg = LEDGenerator(num_particles, center_pos=gm.get_solid_center(name="source"))

    
    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = run_manager(
                geometry_manager=gm,
                experiment_name=experiment_name,
                random_seed=seed,
                num_particles=num_particles,
                plots=plots,
                # pg=pg
            )
        except Exception as e:
            fail_counter += 1
            if fail_counter == 3:
                print("failed 3 timess")
                print(e)
                raise e
                exit()
            continue
        break

    pte = rm.ana_man.photon_transmission_efficiency

    return pte, rm.ana_man.pte_st_dev


def run_8_reflector(n_si, k_si, spec_r, run_id):
    """
    Run  8 reflector simulation, return results
    """
    experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Run ID: {run_id}")
    print(f"Visualize: {visualize}")
    print(f"Plots: {plots}")
    print(f"k_si={k_si}, n_si={n_si}")
    ptes = []
    ptes_err = []
    mm = material_manager(experiment_name) 
    #mm.add_attributes(mm.materials["liquid xenon"], refractive_index=n_xe)
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        # run_id=run_id, 
        # visualize=visualize,
        surf_manager=sm
    )
    fail_counter = 0
    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = run_manager(
                geometry_manager=gm,
                experiment_name=experiment_name,
                random_seed=seed,
                num_particles=num_particles,
                # run_id=run_id,
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

def run_4_reflector(n_si, k_si, spec_r, run_id):
    """
    Run 4 reflector config
    """
    experiment_name = "8refelctortall"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    exclusion = [1, 3, 5, 7]
    excluded = [f"reflector{i}" for i in exclusion]
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Run ID: {run_id}")
    print(f"Visualize: {visualize}")
    print(f"Plots: {plots}")
    print(f"k_si={k_si}, n_si={n_si}")
    print(f"excluded: {excluded}")
    ptes = []
    ptes_err = []
    mm = material_manager(experiment_name) 
    #mm.add_attributes(mm.materials["liquid xenon"], refractive_index=n_xe)
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        surf_manager=sm,
        exclude=excluded
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
            if fail_counter == 3:
                print("failed 3 timess")
                print(e)
                raise e
                exit()
            continue
        break

    pte = rm.ana_man.photon_transmission_efficiency

    return pte, rm.ana_man.pte_st_dev


def run_blocked_half_reflectors(n_si, k_si, spec_r, run_id):
    """
    Run  8 reflector simulation, return results
    """
    experiment_name = "8HalfReflectors28_56"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    print(f"Experiment Name: {experiment_name}")
    print(f"Number of particles: {num_particles}")
    print(f"Random seed: {seed}")
    print(f"Run ID: {run_id}")
    print(f"Visualize: {visualize}")
    print(f"Plots: {plots}")
    print(f"k_si={k_si}, n_si={n_si}")
    ptes = []
    ptes_err = []
    mm = material_manager(experiment_name) 
    #mm.add_attributes(mm.materials["liquid xenon"], refractive_index=n_xe)
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    mm.material_props["liquid xenon"]["scattering_length"] = 300
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        # run_id=run_id, 
        # visualize=visualize,
        surf_manager=sm
    )
    fail_counter = 0

    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = run_manager(
                geometry_manager=gm,
                experiment_name=experiment_name,
                random_seed=seed,
                num_particles=num_particles,
                # run_id=run_id,
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


def run_blocked_4_reflectors(n_si, k_si, spec_r, run_id):
    """
    Run  blocked 4 reflector simulation, return results
    """
    experiment_name = "IncidentBlocker"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    ptes = []
    ptes_err = []
    mm = material_manager(experiment_name) 
    #mm.add_attributes(mm.materials["liquid xenon"], refractive_index=n_xe)
    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    # mm.material_props["liquid xenon"]["scattering_length"] = 300
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        # run_id=run_id, 
        # visualize=visualize,
        surf_manager=sm
    )
    fail_counter = 0

    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = run_manager(
                geometry_manager=gm,
                experiment_name=experiment_name,
                random_seed=seed,
                num_particles=num_particles,
                # run_id=run_id,
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

def main():
    results = []
    run_id = 1
    # for k_si, n_si in itertools.product(np.linspace(.5, 2.5, 100), np.linspace(.5, 1.5, 55)):

    #iterate over all combinations of chosen values of k_si, n_si
    n_si = 0.5
    for k_si, spec_r in itertools.product(np.linspace(.5, 1.4, 5), np.linspace(0, 1, 5)):
            with suppress_stdout(): #suppress output to not clog up the log
                # pte_8, pte_err_8 = run_8_reflector(n_si, k_si,spec_r, run_id) #run 8 reflector
                pte_half, pte_err_half = run_blocked_half_reflectors(n_si, k_si,spec_r, run_id) #run 8 reflector

                # pte_4, pte_err_4 = run_4_reflector(n_si, k_si, run_id) #run 4 reflector

                #compile results and info
                results.append({ 
                    'run_id' : run_id,
                    'k_si': k_si,
                    'n_si': n_si,
                    "spec_r": spec_r,
                    # 'pte_8': pte_8,
                    # 'pte_8_error': pte_err_8,
                    # "pte_4": pte_4,
                    # "pte_4_error": pte_err_4
                    'pte_half': pte_half,
                    'pte_half_err': pte_err_half,
                })
                run_id += 1

    # Write results to CSV
    csv_filename = f"testsweep.csv"
    import csv
    with open(csv_filename, 'w+', newline='') as csvfile:
        fieldnames = results[0].keys() # ['run_id'n_xe', 'n_si', 'pte', 'pte_error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Results have been written to {csv_filename}")



def run_4_short_reflector(k_si, spec_r):
    """
    Run 4 reflector config
    """
    experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM"
    num_particles = 1_000_000
    seed = 1042
    visualize = False
    plots = []
    exclusion = [4,6,7,8]
    excluded = [f"reflector{i}" for i in exclusion]
    

    mm = material_manager(experiment_name) 
    mm.material_props["silicon"]["k"] = k_si
    
    sm = surface_manager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = geometry_manager(
        experiment_name=experiment_name,
        surf_manager=sm,
        exclude=excluded
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
            if fail_counter == 3:
                print("failed 3 timess")
                print(e)
                raise e
                exit()
            continue
        break

    pte = rm.ana_man.photon_transmission_efficiency

    return pte

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print(f"The simulation run time is: {e - s} s")
