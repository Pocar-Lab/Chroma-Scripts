# Source Size Impact on PTE  
*Date Started: August 11, 2024*  
*Date Finished: September 17, 2024*  
*Researcher: Luc Barrett*

## Purpose  
We assume that the source is a point source in Chroma. In actuality, our source is not a point source. This study aims to investigate if modifying the source to a disk of different radii (approaching a point source at \(r = 0\)) has a significant impact on PTE.

## Method  
A new instance of the photon generator class was defined to accurately generate photons for a disk source. Several simulations were run with different source sizes, and the resulting PTE values were recorded.

## Results  
Adjusting the source size has a noticeable impact on PTE. Based on the results, I would recommend switching to using a disk source as it is likely to improve the accuracy of the model.

## Future Work  
It would be prudent to carry out some silicon reflectance analysis with both a point source and a disk source of varying sizes to quantitatively discern if this change makes a significant difference in PTE.
