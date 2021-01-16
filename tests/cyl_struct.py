# Builds a structured O-grid mesh

import numpy as np
from ofblockmeshdicthelper import BlockMeshDict, CylBlockStructContainer, Boundary, SimpleGradingElement, \
	MultiGradingElement, get_grading_info

bmd = BlockMeshDict()
bmd.set_metric('mm')

rs = np.array([0.3, 0.6, 1.0])
ts = np.linspace(0, 2 * np.pi, 9, endpoint=True)  # Try 8*n+1 for any positive integer n (e.g. 9,17, etc...)
zs = np.array([0.0, 0.5, 1.5])

ndr = np.full_like(rs, 6)
ndt = np.full_like(ts, 6)
ndz = np.full_like(zs, 8)

cyl = CylBlockStructContainer(rs, ts, zs, ndr, ndt, ndz, zone='ts', eighth_twist=True)

cyl.tube_struct['grading'][0, 0, :, 1] = SimpleGradingElement(3)

# Twist the block structure
cyl.tube_struct['vertices'][-1, :-1, -1, 1] += 3 * np.pi / 16

# Attempt to reduce the o-grid inclusion angle through precise grading
len_pcts = np.array([0.2, 0.6, 0.2])
dens = np.array([2.0, 1., 1., 2.0])
grd_elm = MultiGradingElement(*get_grading_info(len_pcts, dens))
t_grad[0, :, :, 1] = grd_elm
c_grad[:, :, :, [0, 1]] = grd_elm

wall_faces = cyl.tube_struct['faces'][-1, :-1, :-1, 0].flatten()
wall_bnd = Boundary('patch', 'wall', faces=wall_faces)
bmd.add_boundary(wall_bnd)

cyl.write(bmd)

with open(r'OF_case/system/blockMeshDict', 'w') as infile:
	infile.write(bmd.format())
