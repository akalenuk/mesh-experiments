from oneliners import *
from random import randint
import time

def v__E(a):
	''' Levi-Civita symbol '''
	n = 0
	t = [ti for ti in a]
	for i in xrange(0, len(a)):
		for j in xrange(0, len(a)-i-1):
			if t[j]==t[j+1]:
				return 0
			if t[j]>t[j+1]:
				n+=1
				t[j], t[j+1] = t[j+1], t[j]
	if n % 2 == 0:
		return 1
	else:
		return -1


def precalculate_map_of_E_and_indexes(dimm):
	N = dimm - 1
	map_of_E_and_indexes = {}
	for i in xrange(0, dimm):
		for jk in xrange(0, dimm ** N):
			indexes = [i] + [(jk / (dimm ** (N-j-1))) % dimm for j in xrange(0, N)]
			E = v__E(indexes)
			map_of_E_and_indexes[(i, jk)] = (E, indexes)
	return map_of_E_and_indexes


def cross_of(A, cached_E_and_indexes = None):
	''' n-dimensional cross product on (n-1) vectors in list A '''
	DIMM = len(A[0])
	N = len(A)

	v_res = [0.] * DIMM
	for i in xrange(0, DIMM):
		for jk in xrange(0, DIMM ** N):
			if cached_E_and_indexes:
				(t_res, v_ijk) = cached_E_and_indexes[(i, jk)]
			else:
				v_ijk = [i] + [(jk/(DIMM ** (N-j-1))) % DIMM for j in xrange(0, N)]
				t_res = v__E(v_ijk)
			if t_res != 0:
				for k in xrange(0, N):
					t_res *= A[k][v_ijk[k + 1]]
				v_res[i] += t_res
	return v_res


def point_on_plane(n, d):
	return [-d/n[0]] + [0]*(len(n)-1)

def project_by_vector(point, projection_vector, plane_n, plane_d):
	ponp = point_on_plane(plane_n, plane_d)
	k = dot_of(vector(point, ponp), plane_n) / dot_of(projection_vector, plane_n)
	return sum_of(point, scaled(projection_vector, k))

def solution_for(A, B, cache):
	p = [0. for each in B]
	for i in xrange(len(A)):
		plane_n = A[i]
		plane_d = -B[i]
		other_planes_ns = A[:i] + A[i+1:]
		projection_vector = cross_of(other_planes_ns, cache)
		p = project_by_vector(p, projection_vector, plane_n, plane_d)
	return p


def is_valid_solution(A, B, X, eps = 0.0001):
	new_B = [dot_of(Ai, X) for Ai in A]
	for (Bi, new_Bi) in zip(B, new_B):
		if abs(Bi - new_Bi) > eps:
			return False
	return True

if __name__ == '__main__':
	plane_n = [2., 3., 1.]
	plane_d = 4.
	point = point_on_plane(plane_n, plane_d)
	print 'Point on plane equation fit:', dot_of(plane_n, point) + plane_d
	point_to_project = [1., 1., 2.]
	projection_vector = [2., 1., 0.]
	projected_point = project_by_vector(point_to_project, projection_vector, plane_n, plane_d)	
	print 'Projected point equation fit:', dot_of(plane_n, projected_point) + plane_d
	
	timestamp = time.clock()
	dimm = 6
	cache = precalculate_map_of_E_and_indexes(dimm)
	for n in range(0, 50):
		A = [[] for each in range(dimm)]
		B = []
		for i in range(0, dimm):
			A += []
			for j in range(0, dimm):
				A[i] += [randint(-100, 100) / 100.0]
			B += [randint(-100, 100) / 100.0]
	
		try:
			X = solution_for(A, B, cache)
			print is_valid_solution(A, B, X)
		except ZeroDivisionError:
			print 'No solution'
	print 'In', time.clock() - timestamp, 'seconds'
