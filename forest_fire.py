import obj_io
import least_squares
import numpy
import oneliners

EPS = 5.0
NORM_DOT = 0.9

def ignite(triangle_i, plane_id, plane, plane_map):
	global triangle_to_planes

	# burnout check
	if len(triangle_to_planes[triangle_i]) != 0:
		return

	# normal check
	plane_normal = oneliners.normalize(plane[:3])
	for n in [normals[triangle_normals[triangle_i][j]] for j in range(3)]:
		if abs(oneliners.dot(n, plane_normal)) < NORM_DOT:
			return

	#distance check
	pts = [vertexes[tri] for tri in triangles[triangle_i]]
	distances = least_squares.distances(pts, plane)
	for d in distances:
		if abs(d) > EPS:
			return

	# mark plane_map
	for vi in triangles[triangle_i]:
		plane_map[vi] = list(set(plane_map[vi] + [plane_id]))
	triangle_to_planes[triangle_i] += [plane_id]

	# ignite neighbours
	for new_triangle_i in range(len(triangles)):
		for i in triangles[new_triangle_i]:
			if i in triangles[triangle_i]:
				ignite(new_triangle_i, plane_id, plane, plane_map)
				break;


if __name__ == "__main__":
	f = open('ellipsoid.obj', 'r')
	input_obj = f.read()
	f.close()

	vertexes = obj_io.vertexes(input_obj)
	
	triangles = obj_io.triangles(input_obj)
	triangles = [[ti-1 for ti in tis] for tis in triangles]

	normals = obj_io.normals(input_obj)
	triangle_normals = obj_io.triangle_normals(input_obj)
	triangle_normals = [[ti-1 for ti in tis] for tis in triangle_normals]

	# make plane_map - vertex_index to list of planes it belongs to	
	plane_map = [[] for every in vertexes]
	triangle_to_planes = [[] for every in triangles]
	for i in range(len(triangles)):
		tris = triangles[i]
 		pts = numpy.array([vertexes[pi] for pi in tris] + [vertexes[pi] for pi in tris])
		plane = least_squares.fit_plane(pts)
		ignite(i, i, plane, plane_map)

	# reverse plane_map, replace every point in group with group centroid
	# wouldn't work very well for non-convex plane patches, but who's perfect
	planes_to_vertexes = {}
	for (vertex_index, set_of_planes) in zip(range(len(plane_map)), plane_map):
		list_of_planes = list(set(set_of_planes))
		str_of_planes = ' '.join([str(p) for p in list_of_planes])
		if str_of_planes in planes_to_vertexes:
			planes_to_vertexes[str_of_planes] += [vertex_index]
		else:
			planes_to_vertexes[str_of_planes] = [vertex_index]

	for (a, b) in planes_to_vertexes.iteritems():
		print a, b

	for (planes, vertex_indexes) in planes_to_vertexes.iteritems():
		if len(planes) == 0:	# debug case, generally there shouldn't be any unplaned vertexes
			continue
		centroid = [0., 0., 0.]	
		div = 1. / len(vertex_indexes)
		for vi in vertex_indexes:
			centroid = [c+v for (c, v) in zip(centroid, vertexes[vi])]
		centroid = [c * div for c in centroid]
	
		for vi in vertex_indexes:
			vertexes[vi] = [c for c in centroid]
			
	f = open('ffout.obj', 'w')
	f.write(obj_io.str_from_vertexes(vertexes))
	f.write('\n')
	f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in triangles]))
	f.close()
