from mesh_generation_surface_grid_and_crawl import *
import numpy as np
from math import sqrt

ps = [	[-0.5, -0.5, -0.5], 
		[1., 0., 0.],
		[0., 1., 0.],
		[0., 0., 1.]]

x1 = ps[0][0]; y1 = ps[0][1]; z1 = ps[0][2]
x2 = ps[1][0]; y2 = ps[1][1]; z2 = ps[1][2]
x3 = ps[2][0]; y3 = ps[2][1]; z3 = ps[2][2]
x4 = ps[3][0]; y4 = ps[3][1]; z4 = ps[3][2]

# zero distances
#d2 = (x2 + I*xi2 - x1)**2 + (y2 + I*yi2 - y1)**2 + (z2 - z1)**2
#d3 = (x3 - x1)**2 + (y3 + I*yi3 - y1)**2 + (z3 + I*zi3 - z1)**2
#d4 = (x4 + I*xi4 - x1)**2 + (y4 - y1)**2 + (z4 + I*zi4 - z1)**2

# when solved give us this:
xi2 =  -sqrt((x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2 + z1**2 - 2*z1*z2 + z2**2)/(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2))*(y1 - y2)
yi2 =  sqrt((x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2 + z1**2 - 2*z1*z2 + z2**2)/(x1**2 - 2*x1*x2 + x2**2 + y1**2 - 2*y1*y2 + y2**2))*(x1 - x2)
yi3 =  -sqrt((x1**2 - 2*x1*x3 + x3**2 + y1**2 - 2*y1*y3 + y3**2 + z1**2 - 2*z1*z3 + z3**2)/(y1**2 - 2*y1*y3 + y3**2 + z1**2 - 2*z1*z3 + z3**2))*(z1 - z3)
zi3 =  sqrt((x1**2 - 2*x1*x3 + x3**2 + y1**2 - 2*y1*y3 + y3**2 + z1**2 - 2*z1*z3 + z3**2)/(y1**2 - 2*y1*y3 + y3**2 + z1**2 - 2*z1*z3 + z3**2))*(y1 - y3)
zi4 =  sqrt((x1**2 - 2*x1*x4 + x4**2 + y1**2 - 2*y1*y4 + y4**2 + z1**2 - 2*z1*z4 + z4**2)/(x1**2 - 2*x1*x4 + x4**2 + z1**2 - 2*z1*z4 + z4**2))*(x1 - x4)
xi4 =  -sqrt((x1**2 - 2*x1*x4 + x4**2 + y1**2 - 2*y1*y4 + y4**2 + z1**2 - 2*z1*z4 + z4**2)/(x1**2 - 2*x1*x4 + x4**2 + z1**2 - 2*z1*z4 + z4**2))*(z1 - z4)

# full plane eqaution
#A = [
#	[x1, - xi1,  y1, -yi1, z1, -zi1],
#	[x2, - xi2,  y2, -yi2, z2, -zi2],
#	[x3, - xi3,  y3, -yi3, z3, -zi3],
#	[xi1,  x1,  yi1, y1, zi1, z1],
#	[xi2,  x2,  yi2, y2, zi2, z2],
#	[xi3,  x3,  yi3, y3, zi3, z3]
#	]
#B = [
#	[-1],
#	[-1],
#	[-1],
#	[0],
#	[0],
#	[0]
#	]

# first plane
A = [
	[x1, 0,  y1, 0, z1, 0],
	[x2, - xi2,  y2, -yi2, z2, 0],
	[x3, 0,  y3, -yi3, z3, -zi3],
	[0,  x1,  0, y1, 0, z1],
	[xi2,  x2,  yi2, y2, 0, z2],
	[0,  x3,  yi3, y3, zi3, z3]
	]
B = [
	[-1],
	[-1],
	[-1],
	[0],
	[0],
	[0]
	]
	
(a1, ai1, b1, bi1, c1, ci1) = plane1 = np.linalg.solve(A, B)
#print(a1, ai1, b1, bi1, c1, ci1)


# second plane 
A = [
	[x1,0,  y1,0, z1,0],
	[x3, 0,  y3, -yi3, z3, -zi3],
	[x4, - xi4,  y4, 0, z4, -zi4],
	[0,  x1,  0, y1, 0, z1],
	[0,  x3,  yi3, y3, zi3, z3],
	[xi4,  x4,  0, y4, zi4, z4]
	]
B = [
	[-1],
	[-1],
	[-1],
	[0],
	[0],
	[0]
	]

(a1, ai1, b1, bi1, c1, ci1) = plane2 = np.linalg.solve(A, B)
#print(a1, ai1, b1, bi1, c1, ci1)


# third plane 
A = [
	[x1, 0,  y1, 0, z1, 0],
	[x4, - xi4,  y4, 0, z4, -zi4],
	[x2, - xi2,  y2, -yi2, z2, 0],
	[0,  x1,  0, y1, 0, z1],
	[xi4,  x4,  0, y4, zi4, z4],
	[xi2,  x2,  yi2, y2, 0, z2],
	]
B = [
	[-1],
	[-1],
	[-1],
	[0],
	[0],
	[0]
	]
	
(a1, ai1, b1, bi1, c1, ci1) = plane3 = np.linalg.solve(A, B)
#print(a1, ai1, b1, bi1, c1, ci1)

# fouth plane
A = [
	[x4, - xi4,  y4, 0, z4, -zi4],
	[x3, 0,  y3, -yi3, z3, -zi3],
	[x2, - xi2,  y2, -yi2, z2, 0],
	[xi4,  x4,  0, y4, zi4, z4],
	[0,  x3,  yi3, y3, zi3, z3],
	[xi2,  x2,  yi2, y2, 0, z2]
	]
B = [
	[-1],
	[-1],
	[-1],
	[0],
	[0],
	[0]
	]
	
(a1, ai1, b1, bi1, c1, ci1) = plane4 = np.linalg.solve(A, B)
#print(a1, ai1, b1, bi1, c1, ci1)

def plane_in(x, xi, y, yi, z, zi, plane):
	return x*plane[0][0] + xi*plane[1][0] + y*plane[2][0] + yi*plane[3][0] + z*plane[4][0] + zi*plane[5][0] + 1


def SDF(xyz):
	x = xyz[0]
	xi = 1
	y = xyz[1]
	yi = 1
	z = xyz[2]
	zi = 1
	return (plane_in(x, xi, y, yi, z, zi, plane1)-0.1)  \
	     * (plane_in(x, xi, y, yi, z, zi, plane2)-0.1) \
	     * (plane_in(x, xi, y, yi, z, zi, plane3)-0.1) \
	     * (plane_in(x, xi, y, yi, z, zi, plane4)-0.1)


OUTPUT = '_isotropic_tetrahedron_surface.obj'
(vs, ts) = triangulate([-1.1, -1.1, -1.1], [+1.1, +1.1, +1.1], 0.05, SDF)

vsi = len(vs)
vs += [ps[0], ps[1], ps[2], ps[3]]
ts += [[vsi, vsi+1, vsi+2], [vsi, vsi+2, vsi+3], [vsi, vsi+3, vsi+1], [vsi+3, vsi+2, vsi+1]]

print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

f = open(OUTPUT, 'w')
f.write(obj_io.str_from_vertexes(vs))
f.write('\n')
f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
f.close()
