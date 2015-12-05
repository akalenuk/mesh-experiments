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

	plane_map = [set() for v in vertexes] # not a map

	print "vertexes", len(vertexes)
	print "triangles", len(triangles)
	print "first point neighbours", neighbours[0]
	planes = []
	for i in range(len(vertexes)):
		if len(plane_map[i]) == 0:
			planes += [find_plane(i, len(planes), vertexes, neighbours, plane_map)]
			print "plane ", len(planes), "starts at", i, "and has", len(planes[-1]), "vertixes"

	planes_to_vertexes = {}
	for (vertex_index, set_of_planes) in zip(range(len(plane_map)), plane_map):
		list_of_planes = list(set_of_planes)
		str_of_planes = ' '.join([str(p) for p in list_of_planes])
		if str_of_planes in planes_to_vertexes:
			planes_to_vertexes[str_of_planes] += [vertex_index]
		else:
			planes_to_vertexes[str_of_planes] = [vertex_index]

	for (_, vertex_indexes)	in planes_to_vertexes.iteritems():
		div = 1. / len(vertex_indexes)
		centroid = [0., 0., 0.]
		for vi in vertex_indexes:
			centroid = [c+v for (c, v) in zip(centroid, vertexes[vi])]
		centroid = [c * div for c in centroid]
		for vi in vertex_indexes:
			vertexes[vi] = [c for c in centroid]
			
	f = open('ffout.obj', 'w')
	f.write(obj_io.str_from_vertexes(vertexes))
	f.write('\n')
	f.write(obj_io.str_from_faces(triangles))
	f.close()
# reverse plane_map, replace every point in group with group centroid
# wouldn't work very well for non-convex plane patches, but who's perfect
