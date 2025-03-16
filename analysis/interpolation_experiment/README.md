# Julia QTCI Sweep Experiment  
*Date Started: September 3, 2024*  
*Date Finished: September 15, 2024*  
*Researcher: Luc Barrett*

## Purpose  
Running 2D sweeps by testing every single combination of parameters is very slow and effectively impossible for dimensions higher than 2. The goal of this analysis is to determine if Julia's QCTI library can help us run these parameter sweeps in less time, improving computational efficiency.

## Method  
A Python function was defined to take the sweep parameters as input and output the PTE. This function was then used as input for Julia’s QCTI library to optimize the parameter sweeps and speed up the process. Each individual simulation was done with 1 million photons.

## Results  
A 1000 by 1000 parameter space was interpolated in only about 12000 simulations, making this much faster than sweeping every single value.
## Future Work  
I reccomend to use this library for all future sweeps.