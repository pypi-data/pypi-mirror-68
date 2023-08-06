========
Usage
========

To use Recfast++ for Python in a project::

	from recfast4py import recfast
	
	Yp = 0.24
	T0 = 2.725
	
	Om = 0.26
	Ob = 0.044
	OL = 0.0
	Ok = 0.0
	h100 = 0.71
	Nnu = 3.04
	F = 1.14
	fDM = 0.0
	
	zarr, Xe_H, Xe_He, Xe ,TM = recfast.Xe_frac(Yp,T0,Om, Ob, OL,Ok, h100, Nnu, F, fDM)
	
	import matplotlib.pyplot as pl
	pl.plot(Xe)
	pl.plot(Xe_H)
	pl.plot(Xe_He)
	
	pl.show()
