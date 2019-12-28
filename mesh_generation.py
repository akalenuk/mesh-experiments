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

def add_tri(f, a, p1, p2, p0, i1, i2, in1, in2, vs, ts):
    old_norm = normalized(cross_of(sub_of(p0, p1), sub_of(p2, p1)))
    new_point_dir = normalized(cross_of(old_norm, sub_of(p2, p1)))
    new_point = sum_of(scaled(sum_of(p1, p2), 0.5), scaled(new_point_dir, a))
    new_snapped_point = snap(f, new_point)
    in_vs = False
    new_point_i = len(vs)
    for i in range(len(vs)):
        if distance_between(vs[i], new_snapped_point) < a*R3/4.:
            in_vs = True
            new_point_i = i
            new_snapped_point = vs[i]
            break
    if in1 and in2 and in_vs:
        return
    if not in_vs:
        vs += [new_snapped_point]
    ts += [[i1, i2, new_point_i]]
    add_tri(f, a, p1, new_snapped_point, p2, i1, new_point_i, in1, in_vs, vs, ts)
    add_tri(f, a, p2, new_snapped_point, p1, i2, new_point_i, in2, in_vs, vs, ts)


if __name__ == "__main__":
    vs = []
    ts = []

    first_tri_ps = [snap(SDF, [0., 0., 1.]), snap(SDF, [0., 0.1, 1.]), snap(SDF, [0.1, 0., 1.])]
    vs += first_tri_ps
    ts += [0, 1, 2]

    add_tri(SDF, 0.8, first_tri_ps[0], first_tri_ps[1],  first_tri_ps[2], 0, 1, True, True, vs, ts)
    add_tri(SDF, 0.8, first_tri_ps[1], first_tri_ps[2],  first_tri_ps[0], 1, 2, True, True, vs, ts)
    add_tri(SDF, 0.8, first_tri_ps[2], first_tri_ps[0],  first_tri_ps[1], 2, 0, True, True, vs, ts)

    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

