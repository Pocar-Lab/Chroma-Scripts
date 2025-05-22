from PocarChroma.geometry_manager import GeometryManager
from PocarChroma.run_manager import RunManager, PrimaryGenerator
from PocarChroma.surface_manager import SurfaceManager
from PocarChroma.material_manager import MaterialManager
from PocarChroma.analysis_manager import AnalysisManager
from descent import numerical_gradient, gradient_descent
import numpy as np

import sys
import io
from contextlib import redirect_stdout

noreflector_pte_4 = 0.00129
noreflector_pte_8 = 0.0013598

A_alpha_4 = 1.8
A_alpha_8 = 2.56


lit_value = (1.902, 0.8398)

def score_pte_4(pte):
    return  (A_alpha_4 - pte / noreflector_pte_4) ** 2

def score_pte_8(pte):
    return  (A_alpha_8 - pte / noreflector_pte_8) ** 2


def run_4_tall_reflector(n_si, k_si):
    experiment_name = "8Silicon35_87"
    num_particles = 2_000_000
    seed = 1042
    plots = []
    exclusion = [1,3,5,7]
    excluded = [f"reflector{i}" for i in exclusion]
    spec_r = 0.7

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
    
def run_8_short_reflector(n_si, sr):
    experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM"
    num_particles = 2_000_000
    seed = 1042
    plots = []
    exclusion = []
    excluded = [f"reflector{i}" for i in exclusion]
    spec_r = sr
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
    am = None
    with io.StringIO() as buf, redirect_stdout(buf):
        am = AnalysisManager(
            gm,
            experiment_name,
            plots,
            photons,
            photon_tracks,
            seed,
            particle_histories,
            save=False,
            show=False,
            print=False,
        )
    pte = am.photon_transport_efficiency

    return pte

def score_4_from_indices(input_tuple):
    n_si, k_si = input_tuple
    pte = run_4_tall_reflector(n_si, k_si)
    return score_pte_4(pte)

def score_8_from_indices(input_tuple):
    n_si, sr = input_tuple
    pte = run_8_short_reflector(n_si, sr)
    return score_pte_8(pte)

initial_point = np.array([1.0,0.2])
points = gradient_descent(score_8_from_indices, initial_point, learning_rate=0.08, tol = 0.005, step_size = 0.02)

np.savetxt("output_8_short.csv", points, delimiter=",", fmt="%.5f")  # '%.5f' controls decimal precision
