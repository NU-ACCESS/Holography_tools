# Holography_tools
Holography scripts written in Python and designed to be used with Fiji

Propagator.py creates the wave propagation term. Place in './Fiji.app/jars/Lib' folder with centered FFT scripts. Use 'import Propadator' in python script.

Simulator.py generates a hologram from an image. To test use a_hair.tif.

Iter_Holo_2.py is the main iterative code. Phase and amplitude will be reconstructed from hologram. With example, ~50 iterations need for recovery.

This code is based on https://arxiv.org/pdf/physics/0610048.pdf. See original Matlab version here: https://www.mathworks.com/matlabcentral/fileexchange/64143-iterative-twin-image-free-reconstruction-of-in-line-hologram



