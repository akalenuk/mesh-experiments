import numpy as np
from scipy.optimize import leastsq
from oneliners import *

def distances(X, p):
    plane_xyz = p[0:3]
    distance = (plane_xyz*X).sum(axis=1) + p[3]
    return distance / np.linalg.norm(plane_xyz)


def fit_plane(points, initial_plane = [1.]*4):
	def residuals(params, signal, X):
	    return distances(X, params)
	numbers = leastsq(residuals, initial_plane, args=(None, points), maxfev=100)[0]
	return normalized(numbers[:3]) + [numbers[3]/length_of(numbers[:3])]
	

def plane_from_3_points(points):
	v = [vector(points[0], points[1]), vector(points[0], points[2])]
	cross = [v[0][1]*v[1][2] - v[0][2]*v[1][1],
		 v[0][2]*v[1][0] - v[0][0]*v[1][2],
		 v[0][0]*v[1][1] - v[0][1]*v[1][0]]
	plane_d = dot_of(cross, points[0]) / length_of(cross)
	plane_n = normalized(cross)
	return (plane_n, plane_d)


if __name__ == "__main__":
	# coordinates (XYZ) of C1, C2, C4 and C5
	XYZ = np.array([
		[1., 0., 0.],
		[0., 1., 0.],
		[0., 0., 1.],
		[1., 0., 0.]
	])
		

	# Inital guess of the plane
	p0 = [0.506645455682, -0.185724560275, -1.43998120646, 1.37626378129]
	p = fit_plane(XYZ, p0)
	sd = distances(np.array([[0., 0., 0.], [1., 1., 1.]]), p)

	print "Solution: ", p
	print "Distances from [0, 0, 0], [1, 1, 1]: ", sd
	
	(plane_n, plane_d) = plane_from_3_points([XYZ[0], XYZ[1], XYZ[2]])
	print 'Simmetrical plane:', plane_n, plane_d

