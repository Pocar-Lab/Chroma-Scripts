#The goal of this python file is to run simulations of the silicon reflector runs and subtract the histograms to confirm that the peaks cancel out.

#!/usr/bin/env python
from PocarChroma.geometry_manager import geometry_manager
from PocarChroma.run_manager import run_manager
import numpy as np






def main():
    experiment_names = ["8Silicon35_87","8Silicon35_87","8Silicon35_87","Sebastian_08.01.2023(liquefaction)_correctedSiPM","Sebastian_08.01.2023(liquefaction)_correctedSiPM","Sebastian_08.01.2023(liquefaction)_correctedSiPM"]
    labels = ["Tall8Reflector", "Tall4Reflector", "TallNoReflector", "Short8Reflector","Short4Reflector","ShortNoReflector"]
    e_all= [1, 2, 3, 4, 5, 6, 7, 8] #exclude all
    e_outer = [1, 3, 5, 7] #exclude outer
    e_all_sebastian = [f"reflector{i+1}" for i in e_all]
    e_outer_sebastian = [f"reflector{i}" for i in [4,6,7,8]]
    e_all = [f"reflector{i}" for i in e_all]
    e_outer = [f"reflector{i}" for i in e_outer]


    excludes = [None, e_outer, e_all, None, e_outer_sebastian, e_all_sebastian]
    i=5
    experiment_name = experiment_names[i]
    label = labels[i]
    e = excludes[i]
    num_particles = 100_000_000
    seed = 5020
    plots = ["plot_angle_hist"]
    

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
    hist = rm.ana_man.plot_angle_hist()

    import os
    csv_filename = f"{label}.csv"
    print(f"Saving to: {csv_filename}")
    np.savetxt('/workspace/si-index-of-refraction-sweep/Loick-Analysis-10-2/Subtracting Runs Concept/' + label + '.csv', hist.reshape(1, -1), delimiter=',', fmt='%d')
    print(f"File exists: {os.path.exists(csv_filename)}")

if __name__ == "__main__":
    main()
