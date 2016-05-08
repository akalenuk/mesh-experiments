import time
import obj_io
import least_squares
import numpy
from oneliners import *

EPS = 2.0
NORM_DOT = 0.9
INPUT = 'big_ellipsoid.obj'
OUTPUT = 'ffout.obj'

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
							if abs(d) > EPS:
								fits_in_plane = False
					if fits_in_plane:
						plane_indexes += [j]
						plane_map[j].add(plane_no)
						if len(plane_map[j]) == 1:
							new_fire += [j]
		
		fire = [i for i in new_fire]
	return sorted(plane_indexes)


if __name__ == "__main__":
	f = open(INPUT, 'r')
	input_obj = f.read()
	f.close()

	print 'Max deviation:', EPS
	print 'Min dot of normals', NORM_DOT
	print 'Input model:', INPUT

	vertexes = obj_io.vertexes(input_obj)
	
	triangles = obj_io.triangles(input_obj)
	triangles = [[ti-1 for ti in tis] for tis in triangles]

	normals = obj_io.normals(input_obj)
	triangle_normals = obj_io.triangle_normals(input_obj)
	triangle_normals = [[ti-1 for ti in tis] for tis in triangle_normals]

	vertexes_to_triangles = {vi : [] for vi in range(len(vertexes))}
	for ti in range(len(triangles)):
		vertexes_to_triangles[triangles[ti][0]] += [ti]
		vertexes_to_triangles[triangles[ti][1]] += [ti]
		vertexes_to_triangles[triangles[ti][2]] += [ti]

	print '  Vertexes:', len(vertexes)
	print '  Triangles:', len(triangles)

	neighbours = [set() for v in vertexes]
	for (t1, t2, t3) in triangles:
		neighbours[t1].add(t2)
		neighbours[t1].add(t3)
		neighbours[t2].add(t1)
		neighbours[t2].add(t3)
		neighbours[t3].add(t1)
		neighbours[t3].add(t2)

	# make plane map - vertex_index to list of planes it belongs to	
	print 'Making plane map...',
	timestamp = time.clock()
	vertex_to_planes = [set() for every in vertexes]
	planes = []
	for i in range(len(vertexes)):
		if len(vertex_to_planes[i]) == 0:
			planes += [find_plane(i, len(planes), vertexes, neighbours, vertex_to_planes)]
			print "plane ", len(planes), "starts at", i, "and has", len(planes[-1]), "vertixes"

		if i % 1000 == 0 and i != 0:
			print 1000,
	print len(triangles) % 1000 
	print 'Plane marking time - ', time.clock() - timestamp
	timestamp = time.clock()

	# reverse plane_map
	planes_to_vertexes = {}
	for (vertex_index, set_of_planes) in zip(range(len(vertex_to_planes)), vertex_to_planes):
		tuple_of_planes = tuple(set(set_of_planes))
		if tuple_of_planes in planes_to_vertexes:
			planes_to_vertexes[tuple_of_planes] += [vertex_index]
		else:
			planes_to_vertexes[tuple_of_planes] = [vertex_index]

	# contour retrival
	# step 1 - get contour points: points of 3+ planes intersection
	planes_to_contour_point = {}
	for (planes, vertex_indexes) in planes_to_vertexes.iteritems():
		if len(planes) > 2:
			contour_point = centroid_of([vertexes[vi] for vi in vertex_indexes])
			planes_to_contour_point[planes] = contour_point
			for vi in vertex_indexes:
				vertexes[vi] = [xi for xi in contour_point]

	# step 2 - merge edge and plane points (where 2 planes intersect, or all points are on plane) to contour points
	for (planes, vertex_indexes) in planes_to_vertexes.iteritems():
		if len(planes) < 3:
			potential_vertexes = []
			for (cp_planes, vertex) in planes_to_contour_point.iteritems():
				if len(planes) == 1 and planes[0] in cp_planes:
					potential_vertexes += [vertex]
				elif len(planes) == 2 and planes[0] in cp_planes and planes[1] in cp_planes:
					potential_vertexes += [vertex]
				potential_vertexes += [vertex]

			# it's importrant that this points be merged with nearest contour point
			for vi in vertex_indexes:
				nearest_contour_vertex = min(potential_vertexes, key = lambda pv: distance_between(vertexes[vi], pv))
				vertexes[vi] = [xi for xi in nearest_contour_vertex]

	print 'Classification and post-processing time - ', time.clock() - timestamp
			
	print 'Output model:', OUTPUT
	print '  Contour points:', len(planes_to_contour_point)

	f = open(OUTPUT, 'w')
	f.write(obj_io.str_from_vertexes(vertexes))
	f.write('\n')
	f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in triangles]))
	f.close()

