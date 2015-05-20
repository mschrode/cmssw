--- APEFromMisalignment_7_4_1 branch ---

Implements a simple procedure to approximate Alignment Parameter Errors (APEs):

1) Start with an MC sample. Here, the true geometry IDEAL of the tracker that has been assumed at generation (of the hits) is known.

2) A random mis-alignment is applied on top of the IDEAL geometry: the position of each module is shifted by a random number sampled from a Gaussian of width sigma. This will lead to a mis-aligned tracker geometry MISALIGN.

3) The idea is that MISALIGN corresponds to a geometry obtained with the alignment fit, where the module positions are determined only up to a given uncertainty sigma, which stems from the (statistical) uncertainty (APE) of the alignment procedure. Thererore, one needs to find that sigma that matches the alignment uncertainty in reality. A quantity which is sensitive to the APE and which can be measured also in data is the DRnR (distribution of RMS of normalized residuals).

--> That sigma for which the DRnR of MISALIGN has the same mean as in the data is taken as average APE.

To account for the expected different alignment precision in different subdetectors, e.g. due to different illumination of the modules, the procedure is performed individually per subdetector, e.g. we have IDEAL plus MISALIGN(BPIX) and compare the DRnR of the BPIX modules to the data. Finally, a mis-aligned geometry is produced where each subdetector has that MISALIGN that matches the data, and the DRnR are again verified to match the data (to ensure that correlations between the subdetectors do not affect the result). The corresponding sigmas are then used as APEs. (Further validation are performed to ensure that the track-reconstruction performance is acceptable.)

Caveats of this method: The same APEs are used for all modules in one subdetector. Particularly for cosmics-only alignment, the modules are expected to be very inhomogeniously illuminated in phi, however.
