# Simulation Code Tests
*Created by Loick Marion*

This document outlines a series of tests designed to verify the accuracy and consistency of our simulation code.

## 1. Batch Test  
Ensures that splitting photon simulations into batches produces results identical to running the full simulation in one go. This verifies the correctness of batch processing and consistency in photon transport calculations.

## 2. Beam Test  
Evaluates the effectiveness of the 3D beam implementation, ensuring that the beam behaves as expected in simulation. This test confirms that the beam correctly follows its defined direction, divergence, and intensity profile.

## 3. Source-SiPM Distance Test  
Verifies that the measured distance between the source and SiPM in CAD is correctly translated into the simulation. This is achieved by analyzing absorption length variations and extracting the best-fit source-SiPM distance from the results.
