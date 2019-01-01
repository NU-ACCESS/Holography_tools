from ij import IJ, ImagePlus, ImageStack
from ij.process import ImageProcessor, FloatProcessor
from edu.emory.mathcs.parallelfftj import DoubleTransformer
from edu.emory.mathcs.parallelfftj import FourierDomainOriginType
from edu.emory.mathcs.parallelfftj import SpectrumType
import math, cmath
import Propagator
import fft

# Input parameters
N = 500     # number of pixels
L = 532*0.000000001      # wavelength in nm
w = 0.002  # width field of view 
z = 0.05  # z step in meter

imp = IJ.getImage()

#synthetic amplitude and phase
am = [math.exp(-1.6*val) for val in imp.getProcessor().getPixels()] 
ph = [-3*val for val in imp.getProcessor().getPixels()]

t = [x*cmath.exp(-1j*y) for x, y in zip(am, ph)] 

real = ImagePlus("real", FloatProcessor(N,N,[val.real for val in t]))
imaginary = ImagePlus("IMAGINARY", FloatProcessor(N,N,[val.imag for val in t]))


fft_1 = fft.fft(real,imaginary,N,N)

#projection to detector plane
z = Propagator.Zone(L, N, z, w)
real2 = [(x * y).real for x , y in zip(fft_1, [val.conjugate() for val in z])]
imag2 = [(x * y).imag for x , y in zip(fft_1, [val.conjugate() for val in z])]
R2 = ImagePlus("real", FloatProcessor(N, N, real2, None))
I2 = ImagePlus("imaginary", FloatProcessor(N, N, imag2, None))

ifft_1 = fft.ifft(R2,I2,N,N)

#amplitude at detector plane
Amplitude = ImagePlus("Amplitude_det", FloatProcessor(N, N, [abs(x) for x in ifft_1], None)).show()

