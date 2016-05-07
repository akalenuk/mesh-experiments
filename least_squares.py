import numpy as np
from scipy.optimize import leastsq

def distances(X, p):
    plane_xyz = p[0:3]
    distance = (plane_xyz*X).sum(axis=1) + p[3]
    return distance / np.linalg.norm(plane_xyz)

def fit_plane(points, initial_plane = [1.]*4):
	def residuals(params, signal, X):
	    return distances(X, params)

	return leastsq(residuals, initial_plane, args=(None, points))[0]
	

if __name__ == "__main__":
	# coordinates (XYZ) of C1, C2, C4 and C5
	XYZ = np.array([
		[0., 0., 0.],
		[1., 0., 0.],
		[1., 1., 0.],
		[0., 1., 0.]])
		

	# Inital guess of the plane
	p0 = [0.506645455682, -0.185724560275, -1.43998120646, 1.37626378129]
	p = fit_plane(XYZ, p0)
	sd = distances(np.array([[0., 0., 2.], [1., 1., 3.]]), p)

	print "Solution: ", p
	print "Distances from [0, 0, 2], [1, 1, 3]: ", sd 
