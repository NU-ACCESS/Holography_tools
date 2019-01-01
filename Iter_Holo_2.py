from ij import IJ, ImagePlus, ImageStack
from ij.process import ImageProcessor, FloatProcessor
import math, cmath
import Propagator
import fft

# Input parameters
N = 500     # number of pixels
L = 532*0.000000001   # wavelength in nm
w = 0.002 # width of field in meters
z = 0.05 # object-to-detector distance in meter

imp = IJ.getImage()
z = Propagator.Zone(L, N, z, w) #wave propagation term

#iterative reconstruction
for j in range(0, 50):
	if j == 0:
		#creating initial complex-valued field distribution in the detector plane
		imp_init = ImagePlus("real", FloatProcessor(N, N, [0 for i in range(N*N)])) 
		fft_1 = fft.fft(imp,imp_init,N,N)
	else:
		#reconstruction of transmission function 
		imp2 = ImagePlus("phase", FloatProcessor(N, N, [cmath.phase(x) for x in fft_4], None))
		m = [val for val in imp.getProcessor().getPixels()]
		sin = [math.sin(val) for val in imp2.getProcessor().getPixels()]
		cos = [math.cos(val) for val in imp2.getProcessor().getPixels()]
		imp_r = ImagePlus("", FloatProcessor(N,N,[x*y for x, y in zip(m, cos)]))
		imp_i = ImagePlus("", FloatProcessor(N,N,[x*y for x, y in zip(m, sin)]))
		fft_1 = fft.fft(imp_r, imp_i,N,N)
		
	#multiply image by fresnel kernel: propagate to object plane
	real = [(x * y).real for x , y in zip(fft_1, z)]
	imag = [(x * y).imag for x , y in zip(fft_1, z)]
	R = ImagePlus("", FloatProcessor(N, N, real, None))
	I = ImagePlus("", FloatProcessor(N, N, imag, None))
		
	fft_2 = fft.ifft(R, I,N,N)

	phase = [cmath.phase(x) for x in fft_2] #phase
	m = [abs(x) for x in fft_2]

	#filter in object domain, no non negative absorbances
	fil = [-1* math.log(val) for val in [abs(x) for x in fft_2]]
	ind = [i for i,x in enumerate(fil) if x < 0]
		
	for i in ind:
		phase[i] = 0
		fil[i] = 0

	m = [math.exp(-1*val) for val in fil] #amplitude after filtering
	sin = [math.sin(val) for val in phase]
	cos = [math.cos(val) for val in phase]

	imp_r = ImagePlus("", FloatProcessor(N,N,[x*y for x, y in zip(m, cos)]))
	imp_i = ImagePlus("", FloatProcessor(N,N,[x*y for x, y in zip(m, sin)]))

	imp5 = ImagePlus("amplitude", FloatProcessor(N, N, [math.exp(-val) for val in m], None))
	imp6 = ImagePlus("phase", FloatProcessor(N, N, phase, None))

	#calculating complex-valued wavefront in the detector plane 
	fft_3 = fft.fft(imp_r, imp_i,N,N)
	real2 = [(x * y).real for x , y in zip(fft_3, [val.conjugate() for val in z])]
	imag2 = [(x * y).imag for x , y in zip(fft_3, [val.conjugate() for val in z])]
	R2 = ImagePlus("real", FloatProcessor(N, N, real2, None))
	I2 = ImagePlus("imaginary", FloatProcessor(N, N, imag2, None))

	fft_4 = fft.ifft(R2, I2,N,N)
	
	print ("iteration %d") %j

imp5.show()
imp6.show()