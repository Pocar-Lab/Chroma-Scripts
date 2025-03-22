# Title: Subtracting Runs Concept  

**Dates**: March 17 2025 - 
**Researchers**: Loick Marion, Nick Yazbek

---

## Purpose  
We have determined (leave space) that there is too much correlation between the 8 and 4 reflector runs. One potential solution is to subtract the differences between the 8 and 4 reflector runs, as well as the 4 and 0 reflector runs. In theory, this would isolate the peaks that are unique to each run, making the runs more distinct. We attempted a similar Analysis over the summer, but the uncertainty on the experimental alpha ratios was too high to be able to make conclusions. Now with a significantly lwoer alpha ratio uncertainty due to an improved fit  by using a linear term times an exponential term, we feel that we have a chance to get some meaningful results. 

---

## Method  
We run 2d parameter sweeps over n (real part of refractive index) and specular ratio of silicon reflectors using the julia QCTI library for the silicon runs (8 short, 4 short, 4 tall). We vary the specular ratio between 0 and 1 because that is its entire domain and n from 0.2 to 1.2 as we feel that would allow us to test a sufficient range of reflectances (about 0.2 - 0.8 for photons around 40 degrees). We set k = 0.5 as that number, as demonstrated from previous sweeps that Luc did as well as the Fresnel Equations, allows for large variance in reflectance with similar variance in n, requiring less time computationally.

Once we have the PTE sweeps for the 8 refelctor and 4 reflector runs run, we subtract the 4 reflector pte ratio from the 8 reflector pte ratio, hopign to isolate the effects of the outer 4 reflectors.

Similarly, we subtract 1 (PTE no relfector / pte no refelctor) frm the tall 4 reflector ratio to try and isolte the effects of the 4 refelctor peak.

We then analyze these for correlation as well as fit them to a score function to determine which values of n and sr mak the sweeps best match experimetnal data.
---

## Results  

---

## Future Work  

