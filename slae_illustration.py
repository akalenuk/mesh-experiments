from oneliners import *
from html_bitmap import *
from la_exp import *

A = [[-0.35, 1], [-1.25, 1]]
B = [2, -2]
X = [1, 1]
SHOW_ITERATIVE = True
SHOW_DIRECT = True

COLORS =[
	to_hex(200, 40, 90),
	to_hex(70, 40, 200),
	to_hex(70, 180, 90)
]

def x2s(x):
	return 100*x

def y2s(y):
	return 400-100*y

def solution_iteration(bitmap, A, B, Xi, i):
	if distance_between(multiplication_of(A, Xi), B) < 0.0001:
		return Xi
	else:
		Xj = projected_on_plane(Xi, A[i % len(B)], B[i % len(B)])
		line_on(bitmap, x2s(Xi[0]), y2s(Xi[1]), x2s(Xj[0]), y2s(Xj[1]), to_hex(180, 200, 190), 1)
		return solution_iteration(bitmap, A, B, Xj, i+1)

def solution_direct(bitmap, A, B, cache):
	p = [0. for each in B]
	for i in xrange(len(A)):
		plane_n = A[i]
		plane_d = -B[i]
		other_planes_ns = A[:i] + A[i+1:]
		projection_vector = cross_of(other_planes_ns, cache)
		new_p = project_by_vector(p, projection_vector, plane_n, plane_d)
		line_on(bitmap, x2s(p[0]), y2s(p[1]), x2s(new_p[0]), y2s(new_p[1]), to_hex(200, 170, 200), 1)
		p = new_p
	return p

def add_grid_to(bitmap):
	line_on(bitmap, 0, 0, 0, 399, to_hex(0, 0, 0), 1)
	line_on(bitmap, 0, 0, 7, 20, to_hex(0, 0, 0), 1)
	line_on(bitmap, 0, 99, 7, 99, to_hex(0, 0, 0), 1)
	line_on(bitmap, 0, 199, 7, 199, to_hex(0, 0, 0), 1)
	line_on(bitmap, 0, 299, 7, 299, to_hex(0, 0, 0), 1)
	line_on(bitmap, 0, 399, 499, 399, to_hex(0, 0, 0), 1)
	line_on(bitmap, 479, 392, 499, 399, to_hex(0, 0, 0), 1)
	line_on(bitmap, 99, 399, 99, 392, to_hex(0, 0, 0), 1)
	line_on(bitmap, 199, 399, 199, 392, to_hex(0, 0, 0), 1)
	line_on(bitmap, 299, 399, 299, 392, to_hex(0, 0, 0), 1)
	line_on(bitmap, 399, 399, 399, 392, to_hex(0, 0, 0), 1)

def add_lines(bitmap):
	for i in range(len(B)):
		line_on(bitmap, x2s(0), y2s(B[i]), x2s(5), y2s(B[i] - A[i][0] * 5), COLORS[i], 2)

if __name__ == "__main__":
	bitmap = new_bitmap(500, 400)	
	add_lines(bitmap)
	if SHOW_ITERATIVE:
		solution_iteration(bitmap, A, B, X, 1)
	if SHOW_DIRECT:
		cache = precalculate_map_of_E_and_indexes(len(B))
		solution_direct(bitmap, A, B, cache)
	add_grid_to(bitmap)	
	print to_html(bitmap)
