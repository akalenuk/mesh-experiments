import obj_io
import least_squares
import numpy

eps = 1.0

# plane_map - index to list of planes indexed vectors belong to
# fill_map - index to boolean if all point neighbours found their plane
# plane_no - number of plane, basically the count
def find_plane(start_i, plane_no, vertexes, neighbours, plane_map):
	plane_indexes = [start_i]
	plane_map[start_i].add(plane_no)
	plane = [1., 0., 0., 0.]
	fire = [start_i]

	while len(fire) > 0:
		new_fire = []
		for i in fire:
			for j in neighbours[i]:
				if not plane_no in plane_map[j]:
					fits_in_plane = True
					if len(plane_indexes) >= 3:
						pts = numpy.array([vertexes[pi] for pi in plane_indexes] + [vertexes[j]])
						plane = least_squares.fit_plane(pts)
						distances = least_squares.distances(pts, plane)
						for d in distances:
							if abs(d) > eps:
								fits_in_plane = False
					if fits_in_plane:
						plane_indexes += [j]
						plane_map[j].add(plane_no)
						if len(plane_map[j]) == 1:
							new_fire += [j]
		
		fire = [i for i in new_fire]
	return sorted(plane_indexes)
	
	

if __name__ == "__main__":
	f = open('ellipsoid.obj', 'r')
	input_obj = f.read()
	f.close()

	vertexes = obj_io.vertexes(input_obj)
	
	triangles = obj_io.triangles(input_obj)
	triangles = [[ti-1 for ti in tis] for tis in triangles]

	neighbours = [set() for v in vertexes]
	for (t1, t2, t3) in triangles:
		neighbours[t1].add(t2)
		neighbours[t1].add(t3)
		neighbours[t2].add(t1)
		neighbours[t2].add(t3)
		neighbours[t3].add(t1)
		neighbours[t3].add(t2)

	plane_map = [set() for v in vertexes]

	print "vertexes", len(vertexes)
	print "triangles", len(triangles)
	print "first point neighbours", neighbours[0]
	planes = []
	for i in range(len(vertexes)):
		if len(plane_map[i]) == 0:
			planes += [find_plane(i, len(planes), vertexes, neighbours, plane_map)]
			print "plane ", len(planes), "starts at", i, "and has", len(planes[-1]), "vertixes"

	hist = {}
	for s in plane_map:
		x = len(s)
		if x in hist:
			hist[x] += 1
		else:
			hixt[x] = 1
			
# reverse plane_map, replace every point in group with group centroid
# wouldn't work very well for non-convex plane patches, but who's perfect
