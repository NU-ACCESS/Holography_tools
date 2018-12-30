# L1 = wavelength 450nm * 0.000000001 (for conversion to meters)
# N = number of pixels in width and height
# z distance in meters of sample from sensor
# width of field of view, no magnification factor in meters

def Zone(L1, N, z, w):
	import cmath
#The so called propagator. Fresnel equation stored as complex values.
	#p = []
	#for i in range(N):
	#	for j in range(N):
	#		u = (L1 * (i - N/2 - 1)/w)
	#		v = (L1 * (j - N/2 - 1)/w)
	#		if (u**2 + v**2) <= 1:
  	#			f = cmath.exp(-2*cmath.pi*1j*z*cmath.sqrt(1 - u**2 - v**2)/L1)
 	#		p.append(f)
 	
 	# Above code is the original for loop-- very readable. More effecient list comprehension is below.
 	p = [0 if (L1 * (i - N/2 - 1)/w)**2 + (L1 * (j - N/2 - 1)/w)**2 > 1 else cmath.exp(-2*cmath.pi*1j*z*cmath.sqrt(1 - (L1 * (i - N/2 - 1)/w)**2 - (L1 * (j - N/2 - 1)/w)**2)/L1) for i in range (N) for j in range (N)]
	return(p)