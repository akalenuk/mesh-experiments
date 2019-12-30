import time
import obj_io
from oneliners import *

OUTPUT = 'ppout.obj'
SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 - 1.    # spere 0-1
R3 = 3**0.5

def grad(f, xyz):
    EPS = 1.e-5;
    return [(f(sum_of(xyz, [EPS, 0., 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., EPS, 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., 0., EPS])) - f(xyz)) / EPS]

def snap(f, xyz):
    return sum_of(xyz, scaled(normalized(grad(f, xyz)), -f(xyz)))

def is_proj_in_tri(xyz, xyz1, xyz2, xyz3):
    a1 = sub_of(xyz2, xyz1)
    a2 = sub_of(xyz3, xyz1)
    a3 = cross_of(a1, a2)
    # 3-axis equation
    x1, y1, z1 = tuple(a1)
    x2, y2, z2 = tuple(a2)
    x3, y3, z3 = tuple(a3)
    x, y, z = tuple(xyz)
    a = (x*(y2*z3 - y3*z2) - y*(x2*z3 - x3*z2) + z*(x2*y3 - x3*y2))/(x1*y2*z3 - x1*y3*z2 - x2*y1*z3 + x2*y3*z1 + x3*y1*z2 - x3*y2*z1)
    b = (-x*(y1*z3 - y3*z1) + y*(x1*z3 - x3*z1) - z*(x1*y3 - x3*y1))/(x1*y2*z3 - x1*y3*z2 - x2*y1*z3 + x2*y3*z1 + x3*y1*z2 - x3*y2*z1)
    return a >= 0 and b >= 0 and a + b <=1

def add_tri(f, a, p1, p2, p0, i1, i2, in1, in2, vs, ts, x):
    if x == 0:
        return
    old_norm = normalized(cross_of(sub_of(p0, p1), sub_of(p2, p1)))
    new_point_dir = normalized(cross_of(old_norm, sub_of(p2, p1)))
    new_point = sum_of(scaled(sum_of(p1, p2), 0.5), scaled(new_point_dir, a))
    new_snapped_point = snap(f, new_point)
    
    d1 = distance_between(new_snapped_point, p1)
    d2 = distance_between(new_snapped_point, p2)
    
    in_vs = False
    new_point_i = len(vs)
    for i in range(len(vs)):
        if distance_between(vs[i], new_snapped_point) < min(d1, d2):
            # the in_tri check
            if is_proj_in_tri(vs[i], p1, p2, new_snapped_point):
                in_vs = True
                new_point_i = i
                new_snapped_point = vs[i]
                break
    for i in range(len(ts)):
        if sorted(ts[i]) == sorted([i1, i2, new_point_i]):
            return
    if not in_vs:
        vs += [new_snapped_point]
    ts += [[i1, i2, new_point_i]]
    if x % 2 == 0:
        add_tri(f, a, p1, new_snapped_point, p2, i1, new_point_i, in1, in_vs, vs, ts, x-1)
        add_tri(f, a, new_snapped_point, p2, p1, new_point_i, i2, in_vs, in2, vs, ts, x-1)
    else:
        add_tri(f, a, new_snapped_point, p2, p1, new_point_i, i2, in_vs, in2, vs, ts, x-1)
        add_tri(f, a, p1, new_snapped_point, p2, i1, new_point_i, in1, in_vs, vs, ts, x-1)



if __name__ == "__main__":
    vs = []
    ts = []
    a = 0.2

    first_tri_ps = [snap(SDF, [0., 0., 1.]), snap(SDF, [0., 0.1, 1.]), snap(SDF, [0.1, 0., 1.])]
    vs += [snap(SDF, [0., 0., 1.]), snap(SDF, [0., a, 1.])]

    add_tri(SDF, a, vs[0], vs[1],  snap(SDF, [a, 0., 1.]), 0, 1, True, True, vs, ts, 16)
    
    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

