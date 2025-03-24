#!/usr/bin/env python
import time
import csv
import numpy as np
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager

"""
Example showing how to run a simulation for different numbers of particles and save timing results to a CSV file.
"""

def run_simulation(num_particles):
    experiment_name = "Sebastian_08.01.2023(liquefaction)_correctedSiPM"
    e = [4, 6, 7, 8]  # Excludes short silicon outer
    e = [f"reflector{i}" for i in e]
    seed = np.random.randint(0, 10000)

    plots = [
    ]

    total_start = time.perf_counter()

    # Time geometry_manager
    start_gm = time.perf_counter()
    gm = geometry_manager(experiment_name=experiment_name, exclude=e)
    end_gm = time.perf_counter()

    # Time run_manager
    start_rm = time.perf_counter()
    rm = run_manager(
        geometry_manager=gm,
        experiment_name=experiment_name,
        random_seed=seed,
        num_particles=num_particles,
        plots=plots,
        batches=True
    )
    end_rm = time.perf_counter()

    total_end = time.perf_counter()

    return {
        "num_particles": num_particles,
        "geometry_manager_time": end_gm - start_gm,
        "run_manager_time": end_rm - start_rm,
        "total_time": total_end - total_start
    }

def main():
    particle_counts = [1_00_000] * 10 # Modify as needed
    results = []

    for n in particle_counts:
        print(f"Running simulation with {n} particles...")
        timing_data = run_simulation(n)
        results.append(timing_data)
        print(f"Completed {n} particles in {timing_data['total_time']:.2f} seconds.")

    # Save results to CSV
    csv_filename = "simulation_timing_results.csv"

    file_exists = False
    try:
        with open(csv_filename, "r") as f:
            file_exists = True  # Check if file exists and has data
    except FileNotFoundError:
        pass  # If file doesn't exist, create it later

    with open(csv_filename, "a", newline="") as csvfile:
        fieldnames = ["num_particles", "geometry_manager_time", "run_manager_time", "total_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:  # Only write headers if file is newly created
            writer.writeheader()

        writer.writerows(results)
    print(f"Results saved to {csv_filename}")

if __name__ == "__main__":
    main()
