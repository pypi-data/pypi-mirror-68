# Quasi-discrete Hankel transform.

An approximately unitary discrete Hankel transform useful for numerical wave propagation with cylindrical symmetry.
 
Described in:

Yu, L.; Huang, M.; Chen, M.; Chen, W.; Huang, W. & Zhu, Z., 
[Quasi-discrete Hankel transform](https://www.osapublishing.org/ol/abstract.cfm?uri=ol-23-6-409),
Opt. Lett., OSA, 1998, 23, 409-411.

The only difference from Yu et al is that instead of r<sub>1</sub> and r<sub>2</sub> we use
r and k, where k=2*pi*r_2 i.e. here we use angular frequency. Instances of class QDHT are
parameterized by single parameter N, the number of 
sampling points. 

For all functions, R is the aperture radius and dim is dimension along which
r or k runs i.e. along which transforms are performed.
