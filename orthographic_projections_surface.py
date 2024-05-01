from mesh_generation_surface_grid_and_crawl import *

from sympy import *

xs = [-0.9, +0.7, +0.8]
ys = [-0.1, +0.8, -0.6]
zs = [-0.2, +0.0, +0.3]

#{ax: (y1 - y2)/(x1*y2 - x2*y1), ay: (-x1 + x2)/(x1*y2 - x2*y1)}

x1, x2, x3, y1, y2, y3, z1, z2, z3 = symbols('x1 x2 x3 y1 y2 y3 z1 z2 z3')
ax1_z, ax2_z, ax3_z, ay1_z, ay2_z, ay3_z, az1_z, az2_z, az3_z = symbols('ax1_z ax2_z ax3_z ay1_z ay2_z ay3_z az1_z az2_z az3_z')
ax1_y, ax2_y, ax3_y, ay1_y, ay2_y, ay3_y, az1_y, az2_y, az3_y = symbols('ax1_z ax2_z ax3_z ay1_z ay2_z ay3_z az1_z az2_z az3_z')
ax1_x, ax2_x, ax3_x, ay1_x, ay2_x, ay3_x, az1_x, az2_x, az3_x = symbols('ax1_x ax2_x ax3_x ay1_x ay2_x ay3_x az1_x az2_x az3_x')

x, y, z = symbols('x y z')
a, b, c = symbols('a b c')


# z-plane
eqs = solve([
    ax1_z*x1 + ay1_z*y1 + 1,
    ax1_z*x2 + ay1_z*y2 + 1
    ], (ax1_z, ay1_z))
ax1_z = eqs[ax1_z]
ay1_z = eqs[ay1_z]

eqs = solve([
    ax2_z*x2 + ay2_z*y2 + 1,
    ax2_z*x3 + ay2_z*y3 + 1
    ], (ax2_z, ay2_z))
ax2_z = eqs[ax2_z]
ay2_z = eqs[ay2_z]

eqs = solve([
    ax3_z*x3 + ay3_z*y3 + 1,
    ax3_z*x1 + ay3_z*y1 + 1
    ], (ax3_z, ay3_z))
ax3_z = eqs[ax3_z]
ay3_z = eqs[ay3_z]

# y-plane
eqs = solve([
    ax1_y*x1 + 1 + az1_y*z1,
    ax1_y*x2 + 1 + az1_y*z2
    ], (ax1_y, az1_y))
ax1_y = eqs[ax1_y]
az1_y = eqs[az1_y]

eqs = solve([
    ax2_y*x2 + 1 + az2_y*z2,
    ax2_y*x3 + 1 + az2_y*z3
    ], (ax2_y, az2_y))
ax2_y = eqs[ax2_y]
az2_y = eqs[az2_y]

eqs = solve([
    ax3_y*x3 + 1 + az3_y*z3,
    ax3_y*x1 + 1 + az3_y*z1
    ], (ax3_y, az3_y))
ax3_y = eqs[ax3_y]
az3_y = eqs[az3_y]

# x-plane
eqs = solve([
    1 + ay1_x*y1 + az1_x*z1,
    1 + ay1_x*y2 + az1_x*z2
    ], (ay1_x, az1_x))
ay1_x = eqs[ay1_x]
az1_x = eqs[az1_x]

eqs = solve([
    1 + ay2_x*y2 + az2_x*z2,
    1 + ay2_x*y3 + az2_x*z3
    ], (ay2_x, az2_x))
ay2_x = eqs[ay2_x]
az2_x = eqs[az2_x]

eqs = solve([
    1 + ay3_x*y3 + az3_x*z3,
    1 + ay3_x*y1 + az3_x*z1
    ], (ay3_x, az3_x))
ay3_x = eqs[ay3_x]
az3_x = eqs[az3_x]

#print(ax1_z, ax1_y, ay1_x)
#print(ay1_z, az1_y, az1_x)
#print(ax2_z, ax2_y, ay2_x)
#print(ay2_z, az2_y, az2_x)
#print(ax3_z, ax3_y, ay3_x)
#print(ay3_z, az3_y, az3_x)

# surface equations
eqs = solve(
[(ax1_z*x + ay1_z*y + 1)*(ax2_z*x + ay2_z*y + 1)*(ax3_z*x + ay3_z*y + 1) - a,
 (ax1_y*x + 1 + az1_y*z)*(ax2_y*x + 1 + az2_y*z)*(ax3_y*x + 1 + az3_y*z) - b,
 (1 + ay1_x*x + az1_x*z)*(1 + ay2_x*x + az2_x*z)*(1 + ay3_x*x + az3_x*z) - c
], (a, b, c))

a = eqs[a]
b = eqs[b]
c = eqs[c]

_a = a.subs([(x1, xs[0]), (x2, xs[1]), (x3, xs[2]), (y1, ys[0]), (y2, ys[1]), (y3, ys[2]), (z1, zs[0]), (z2, zs[1]), (z3, zs[2])])
_b = a.subs([(x1, xs[0]), (x2, xs[1]), (x3, xs[2]), (y1, ys[0]), (y2, ys[1]), (y3, ys[2]), (z1, zs[0]), (z2, zs[1]), (z3, zs[2])])
_c = c.subs([(x1, xs[0]), (x2, xs[1]), (x3, xs[2]), (y1, ys[0]), (y2, ys[1]), (y3, ys[2]), (z1, zs[0]), (z2, zs[1]), (z3, zs[2])])


def SDF(xyz):
    fa = _a.subs([(x, xyz[0]), (y, xyz[1]), (z, xyz[2])]).evalf()
    fb = _b.subs([(x, xyz[0]), (y, xyz[1]), (z, xyz[2])]).evalf()
    fc = _c.subs([(x, xyz[0]), (y, xyz[1]), (z, xyz[2])]).evalf()
    return fa*fb*fc


OUTPUT = '_ortographic_projections_surface.obj'
(vs, ts) = triangulate([-1.1, -1.1, -1.1], [+1.1, +1.1, +1.1], 0.1, SDF)

print ("triangles: " + str(len(ts)) + "   vertices: " + str(len(vs)))

f = open(OUTPUT, 'w')
f.write(obj_io.str_from_vertexes(vs))
f.write('\n')
f.write(obj_io.str_from_faces([[ti+1 for ti in tri] for tri in ts]))
f.close()
