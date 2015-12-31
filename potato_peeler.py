import obj_io
from oneliners import *

EPS = 2.0
NORM_DOT = 0.9
INPUT = 'big_ellipsoid.obj'
OUTPUT = 'ffout.obj'

def peel(triangle_i, plane_id, plane_n, plane_d):
	global vertexes, triangles, normals, triangle_normals, vertexes_to_triangles # immutable
	global vertex_to_planes, triangle_to_planes # mutable

	if len(triangle_to_planes[triangle_i]) != 0:
		return

	# normal check
	for n in [normals[triangle_normals[triangle_i][j]] for j in range(3)]:
		if abs(dot(n, plane_n)) < NORM_DOT:
			return

	# distance check
	pts = [vertexes[tri] for tri in triangles[triangle_i]]
	for pt in pts:
		d = distance(pt, project(pt, plane_n, plane_d))
		if abs(d) > EPS:
			return

	# mark plane_map
	for vi in triangles[triangle_i]:
		vertex_to_planes[vi] = list(set(vertex_to_planes[vi] + [plane_id]))
	triangle_to_planes[triangle_i] += [plane_id]

	# ignite neighbours
	for vi in triangles[triangle_i]:
		for tri in vertexes_to_triangles[vi]:
			peel(tri, plane_id, plane_n, plane_d)



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

	# make plane map - vertex_index to list of planes it belongs to	
	print 'Peeling...',
	vertex_to_planes = [[] for every in vertexes]
	triangle_to_planes = [[] for every in triangles]
	for i in range(len(triangles)):
		tris = triangles[i]
		vs = [vertexes[tri] for tri in tris]
		v = [vector(vs[0], vs[1]), vector(vs[0], vs[2])]
		cross = [v[0][1]*v[1][2] - v[0][2]*v[1][1],
			 v[0][2]*v[1][0] - v[0][0]*v[1][2],
			 v[0][0]*v[1][1] - v[0][1]*v[1][0]]
		plane_d = dot(cross, vs[0]) / length(cross)
		plane_n = normalize(cross)
		peel(i, i, plane_n, plane_d)
		if i % 1000 == 0 and i != 0:
			print 1000,
	print len(triangles) % 1000 


	# reverse plane_map
	planes_to_vertexes = {}
	for (vertex_index, set_of_planes) in zip(range(len(vertex_to_planes)), vertex_to_planes):
		tuple_of_planes = tuple(set(set_of_planes))
		if tuple_of_planes in planes_to_vertexes:
			planes_to_vertexes[tuple_of_planes] += [vertex_index]
		else:
			planes_to_vertexes[tuple_of_planes] = [vertex_index]

	# 3 step contour retrival
	# step 1 - get contour points: points of 3+ planes intersection
	planes_to_contour_point = {}
	for (planes, vertex_indexes) in planes_to_vertexes.iteritems():
		if len(planes) > 2:
			contour_point = centroid([vertexes[vi] for vi in vertex_indexes])
			planes_to_contour_point[planes] = contour_point
			for vi in vertex_indexes:
				vertexes[vi] = [xi for xi in contour_point]

	# step 2 - merge edge points (where 2 planes intersect) to contour points
	for (planes, vertex_indexes) in planes_to_vertexes.iteritems():
		if len(planes) == 2:
			potential_vertexes = []
			for (cp_planes, vertex) in planes_to_contour_point.iteritems():
				if planes[0] in cp_planes and planes[1] in cp_planes:
					potential_vertexes += [vertex]

			for vi in vertex_indexes:
				potential_vertexes = sorted(potential_vertexes, key = lambda pv: distance(vertexes[vi], pv))
				vertexes[vi] = [xi for xi in potential_vertexes[0]]

	# step 3 - delete plane points that don't intersect anything (just zero them for now)
	for (planes, vertex_indexes) in planes_to_vertexes.iteritems():
		if len(planes) == 1:
			plane_points_centroid = centroid([vertexes[vi] for vi in vertex_indexes])
			for vi in vertex_indexes:
#				vertexes[vi] = [0., 0., 0.]
				vertexes[vi] = plane_points_centroid
			
	print 'Output model:', OUTPUT
	print '  Contour points:', len(planes_to_contour_point)

	f = open(OUTPUT, 'w')
	f.write(obj_io.str_from_vertexes(vertexes))
	f.write('\n')
	f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in triangles]))
	f.close()