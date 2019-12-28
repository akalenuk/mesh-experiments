import time
import obj_io
from oneliners import *

OUTPUT = 'ppout.obj'
SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 - 1.    # spere 0-1

def grad(f, xyz):
    EPS = 1.e-5;
    return [(f(sum_of(xyz, [EPS, 0., 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., EPS, 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., 0., EPS])) - f(xyz)) / EPS]

def snap(f, xyz):
    return sum_of(xyz, scaled(normalized(grad(f, xyz)), -f(xyz)))

if __name__ == "__main__":
    vs = []
    ts = []

    first_tri_ps = [snap(SDF, [0., 0., 1.]), snap(SDF, [0., 0.1, 1.]), snap(SDF, [0.1, 0., 1.])]
    print first_tri_ps
    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

