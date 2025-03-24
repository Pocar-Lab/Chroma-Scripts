#!/usr/bin/env python
from PocarChroma.geometry_manager import GeometryManager
from PocarChroma.run_manager import RunManager, PrimaryGenerator
from PocarChroma.surface_manager import SurfaceManager
from PocarChroma.material_manager import MaterialManager
from PocarChroma.analysis_manager import AnalysisManager

import time
import numpy as np
from pprint import pprint
import multiprocessing
from functools import partial
from tqdm import tqdm
from tqdm.contrib import itertools

from contextlib import contextmanager
import sys, os

def run_8_short_reflector(n_si, spec_r):
    experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM"
    num_particles = 2_000_000
    seed = 1042
    plots = []
    exclusion = []
    excluded = [f"reflector{i}" for i in exclusion]
    k_si = 0.5
    
    ptes = []
    ptes_err = []
    mm = MaterialManager(experiment_name) 

    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = SurfaceManager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = GeometryManager(
        experiment_name=experiment_name,
        surf_manager=sm,
        exclude=excluded
    )
    fail_counter = 0
    
    rm = None
    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = RunManager(
                geometry_manager=gm,
                random_seed=seed,
                num_particles=num_particles,
            )
        except Exception as e:
            fail_counter += 1
            if fail_counter == 3:
                print("failed 3 times")
                print(e)
                raise e
                exit()
            continue
        break

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
                print = False,
            )    
    pte = am.photon_transport_efficiency
    
def run_4_tall_reflector(n_si, spec_r):
    experiment_name = "8Silicon35_87"
    num_particles = 2_000_000
    seed = 1042
    plots = []
    exclusion = [1,3,5,7]
    excluded = [f"reflector{i}" for i in exclusion]
    k_si = 0.5

    mm = MaterialManager(experiment_name) 

    mm.add_attributes(mm.materials["silicon"], refractive_index=n_si)
    mm.material_props["silicon"]["eta"] = n_si
    mm.material_props["silicon"]["k"] = k_si
    sm = SurfaceManager(mm, experiment_name) 
    sm.overwrite_property("silicon-Xe", "reflect_specular", spec_r)
    sm.overwrite_property("silicon-Xe", "reflect_diffuse", 1-spec_r)

    gm = GeometryManager(
        experiment_name=experiment_name,
        surf_manager=sm,
        exclude=excluded
    )
    fail_counter = 0
    
    rm = None
    while fail_counter < 3: #handle rare CUDA error
        try:
            rm = RunManager(
                geometry_manager=gm,
                random_seed=seed,
                num_particles=num_particles,
            )
        except Exception as e:
            fail_counter += 1
            if fail_counter == 3:
                print("failed 3 times")
                print(e)
                raise e
                exit()
            continue
        break

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
                print = False,
            )    
    pte = am.photon_transport_efficiency

    return pte