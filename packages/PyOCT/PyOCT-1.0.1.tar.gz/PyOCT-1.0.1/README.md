# PyOCT: Imaging Reconstruction of Spectral-Domain Optical Coherence Tomography
PyOCT is developed to conduct normal spectral-domain optical coherence tomography (SD-OCT) imaging reconstruction with main steps as:
1. Reading Data
2. Background Subtraction 
3. Spectral Resampling 
3. Comutational Aberration Correction (Alpha-correction)
4. Camera Dispersion Correction (Beta-correction with camera calibration factors) 
5. Inverse Fourier Transform 
6. Obtain OCT Image

The algorithms was developed initially in Prof. Steven G. Adie research lab at Cornell University using MATLAB. The reconstruction speed has been improved with matrix-operation. Compared with MATLAB, Python language have a much better performance in loading data from binary files tested only in our lab computer. 