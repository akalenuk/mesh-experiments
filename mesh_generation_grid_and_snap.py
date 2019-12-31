import time
import obj_io
from oneliners import *

OUTPUT = 'ppout.obj'
SDF = lambda xyz : (xyz[0]**2 + xyz[1]**2 + xyz[2]**2) ** 0.5 - 0.5    # spere 0-0.5
R3 = 97./56.

# three axes
a1 = [R3, 1., 0]
a2 = [R3, -1., 0]
a3 = [1., 0, R3]

def grad(f, xyz):
    EPS = 1.e-5;
    return [(f(sum_of(xyz, [EPS, 0., 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., EPS, 0.])) - f(xyz)) / EPS,
            (f(sum_of(xyz, [0., 0., EPS])) - f(xyz)) / EPS]

def snap(f, xyz):
    return sum_of(xyz, scaled(normalized(grad(f, xyz)), -f(xyz)))


def triangulate(sdf, p0, scale, subdivisions, ts, vs):
    if subdivisions > 0:
        # subdivide
        p1 = sum_of(p0, scaled(a1, scale / 2.))
        p2 = sum_of(p0, scaled(a2, scale / 2.))
        p3 = sum_of(p0, scaled(a3, scale / 2.))
        p12 = sum_of(sum_of(p0, scaled(a1, scale / 2.)), scaled(a2, scale / 2.))
        p23 = sum_of(sum_of(p0, scaled(a2, scale / 2.)), scaled(a3, scale / 2.))
        p31 = sum_of(sum_of(p0, scaled(a3, scale / 2.)), scaled(a1, scale / 2.))
        p123 = sum_of(sum_of(p0, scaled(a1, scale / 2.)), sum_of(scaled(a2, scale / 2.), scaled(a3, scale / 2.)))
        ps = [p0, p1, p2, p3, p12, p23, p31, p123]
        for p in ps:
            triangulate(sdf, p, scale / 2., subdivisions - 1, ts, vs)
    else:
        # triangulate
        p1 = sum_of(p0, scaled(a1, scale))
        p2 = sum_of(p0, scaled(a2, scale))
        p3 = sum_of(p0, scaled(a3, scale))
        p12 = sum_of(sum_of(p0, scaled(a1, scale)), scaled(a2, scale))
        p23 = sum_of(sum_of(p0, scaled(a2, scale)), scaled(a3, scale))
        p31 = sum_of(sum_of(p0, scaled(a3, scale)), scaled(a1, scale))
        p123 = sum_of(sum_of(p0, scaled(a1, scale)), sum_of(scaled(a2, scale), scaled(a3, scale)))
        ps = [p0, p1, p2, p3, p12, p23, p31, p123]
        sdfs = [sdf(p) for p in ps]
        if sum([1 for p in ps if sdf(p) > 0]) == 8: # no conflict
            return

        def xyz(i, j, quad):
            ti = i / 4.
            tj = j / 4.
            return sum_of(
                sum_of(
                    scaled(scaled(quad[0], 1-ti), 1-tj), 
                    scaled(scaled(quad[1], 1-ti), tj)),
                sum_of(
                    scaled(scaled(quad[2], ti), 1-tj), 
                    scaled(scaled(quad[3], ti), tj)))

        quads = [[p0,  p1,  p2,  p12], [p0, p2,   p3,  p23], [p0, p3,  p1,  p31],
                 [p1, p12, p31, p123], [p2, p23, p12, p123], [p3, p23, p31, p123]]
        for quad in quads:
            if sum([1 for p in quad if sdf(p) > 0]) == 4: # quad is out
                for i in range(4):
                    for j in range(4):
                        tsi = len(vs)
                        vs += [snap(sdf, xyz(i,j, quad))]
                        vs += [snap(sdf, xyz(i,j+1, quad))]
                        vs += [snap(sdf, xyz(i+1,j, quad))]
                        vs += [snap(sdf, xyz(i+1,j+1, quad))]
                        ts += [[tsi, tsi+1, tsi+2]]
                        ts += [[tsi+2, tsi+1, tsi+3]]

 
if __name__ == "__main__":
    vs = []
    ts = []
    triangulate(SDF, [-3*R3/2., 0, -R3/2.], 2, 2, ts, vs)

    print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

    f = open(OUTPUT, 'w')
    f.write(obj_io.str_from_vertexes(vs))
    f.write('\n')
    f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
    f.close()

