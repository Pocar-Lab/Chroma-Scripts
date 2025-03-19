#!/usr/bin/env python
import time
import csv
import numpy as np
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
from PocarChroma.analysis_manager import analysis_manager

"""
Example showing how to run a simulation for different numbers of particles and save timing results to a CSV file.
"""

def run_simulation(num_particles):
    experiment_name = "8Silicon35_87"
    seed = np.random.randint(0, 10000)
    plots = []

    # Time geometry_manager
    e = None
    gm = geometry_manager(experiment_name=experiment_name, exclude=e)

    # Time run_manager
    rm = run_manager(
        geometry_manager=gm,
        experiment_name=experiment_name,
        random_seed=seed,
        num_particles=num_particles,
        plots=plots,
        batches=True
    )

    # Time Analysis Manager
    photons, photon_tracks, particle_histories = rm.get_simulation_results()

    am = analysis_manager(
        gm,
        experiment_name,
        plots,
        photons,
        photon_tracks,
        seed,
        particle_histories,
        save=False,
        show=True,
    )

    timing_data = {
        "num_particles": num_particles,
        **rm.times
    }
    return timing_data

def main():
    particle_counts = [10_000_000] * 10  # Modify as needed
    results = []

    for n in particle_counts:
        print(f"Running simulation with {n} particles...")
        timing_data = run_simulation(n)
        results.append(timing_data)
        print(f"Completed {n} particles.")

    # Save results to CSV
    csv_filename = "run_batches_timing_results.csv"

    # Determine field names dynamically from results
    all_fieldnames = set()
    for result in results:
        all_fieldnames.update(result.keys())

    fieldnames = sorted(all_fieldnames)  # Sort for consistency

    file_exists = False
    try:
        with open(csv_filename, "r") as f:
            file_exists = True  # Check if file exists
    except FileNotFoundError:
        pass  # If file doesn't exist, create it later

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:  # Write header if new file
            writer.writeheader()

        writer.writerows(results)
    
    print(f"Results saved to {csv_filename}")

if __name__ == "__main__":
    main()
