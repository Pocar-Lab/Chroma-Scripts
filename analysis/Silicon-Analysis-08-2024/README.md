# 2D Sweep over Real and Complex Indices of Refraction  
*Date Started: July 31, 2024*  
*Date Finished: August 2, 2024*  
*Researcher: Luc Barrett*

## Purpose  
The purpose of this sweep is to find the indices of refraction of Silicon that best match our data. We hope to determine a best-fit line of solutions for both the 8-reflector and 4-reflector runs, and find their intersection to identify the indices of refraction that yield the best match with our experimental data.

## Method  
A total of 11,000 simulations were run—5,500 for the 8-short and 4-tall reflector configurations. A 2D sweep was performed by varying both the real (n) and complex (k) indices of refraction. The ratio of PTEs for the 8-reflector/no reflector and 4-reflector/no reflector were taken and compared to the respective alpha ratios. The optimal results were plotted using a score function, which was the square of the difference between the PTE and alpha ratios.

## Results  
The results of the 4-reflector and 8-reflector sweeps were too correlated to use both for a unique solution. Additionally, it was determined that the PTE solution bands follow lines of constant reflectance, leading us to believe that the PTE is more influenced by reflectance than by the individual real and complex indices of refraction.

## Future Work  
We need a method to break the correlation between different runs. Since this correlation is inherent from the geometry of the cell, we should test whether other cell configurations could be useful. Additionally, it seems that varying both the specular ratio and reflectance would be more effective than varying n and k, as reflectance appears to be the primary driver of PTE.
