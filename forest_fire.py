import obj_io
import least_squares

# plane_map - index to list of planes indexed vectors belong to
# fill_map - index to boolean if all point neighbours found their plane
# plane_no - number of plane, basically the count
def find_plane(i, vertexes, neighbours, plane_map, fill_map, plane_no):
	plane_indexes = [[i]]
	for j in neighbours[i]:
		if fill_map[j] == False:
			if len(plane_indexes) < 3:
				plane_indexes += [j]
			else:
				
	

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

	plane_map = [[] for v in vertexes]

	fill_map = [False for v in vertexes]

	print "vertexes", len(vertexes)
	print "triangles", len(triangles)
	print "first point neighbours", neighbours[0]
