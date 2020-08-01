# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# ----------------------------------------------------------
# Author: Wu Ning
# ----------------------------------------------------------

# ------------------------------------------------------------
# Create a new mesh (object) from verts/edges/faces.
# verts/edges/faces ... List of vertices/edges/faces for the
#                    new mesh (as used in from_pydata).
# name ... Name of the new mesh (& object)

import bpy
from math import *
from bpy_extras import object_utils
from mathutils import *

def create_mesh_object(context, verts, edges, faces, name):
    # Create new mesh
    mesh = bpy.data.meshes.new(name)
    # Make a mesh from a list of verts/edges/faces.
    mesh.from_pydata(verts, [], faces)
    # Update mesh geometry after adding stuff.
    mesh.update()
    return object_utils.object_data_add(context, mesh, operator=None)

def create_curve_object(context, curve, name):
    return object_utils.object_data_add(context, curve, operator=None)


# Generate Sierpinski Triangle mesh
def sier_tri_gen(interation):

    #base triangle
    baseverts = []
    basefaces = []
    for i in range (0, 3):
        angle = i * pi * 2 / 3
        baseverts.append(Vector((cos(angle), sin(angle), 0)))
    basefaces.append([0, 1, 2])

    #recursive
    for i in range (0, interation):
        newverts = []
        newfaces = []
        for j in range (0, len(basefaces)):
            poly = basefaces[j]
            v0 = baseverts[poly[0]]
            v1 = baseverts[poly[1]]
            v2 = baseverts[poly[2]]

            mid0 = 0.5*(v0+v1)
            mid1 = 0.5*(v1+v2)
            mid2 = 0.5*(v2+v0)

            newverts.append(v0)
            newverts.append(mid0)
            newverts.append(v1)
            newverts.append(mid1)
            newverts.append(v2)
            newverts.append(mid2)

            bottom = j*6 - 1
            newfaces.append([bottom+1, bottom+2, bottom+6])
            newfaces.append([bottom+2, bottom+3, bottom+4])
            newfaces.append([bottom+6, bottom+4, bottom+5])
        
        baseverts = newverts
        basefaces = newfaces

    return baseverts, basefaces

# help function
def add_poly4(newverts, newfaces, v1, v2, v3, v4, bottom):
    newverts.append(v1)
    newverts.append(v2)
    newverts.append(v3)
    newverts.append(v4)

    newfaces.append([bottom+1, bottom+2, bottom+3])
    newfaces.append([bottom+1, bottom+3, bottom+4])
    newfaces.append([bottom+1, bottom+4, bottom+2])
    newfaces.append([bottom+4, bottom+3, bottom+2])

# Generate Sierpinski Triangle volume mesh
def sier_tri_vol_gen(interation):

    #base triangle volume
    baseverts = []
    basefaces = []
    baseverts.append(Vector((1, 1, 1)))
    baseverts.append(Vector((-1, -1, 1)))
    baseverts.append(Vector((1, -1, -1)))
    baseverts.append(Vector((-1, 1, -1)))
    basefaces.append([0, 1, 2])
    basefaces.append([0, 2, 3])
    basefaces.append([0, 3, 1])
    basefaces.append([3, 2, 1])

    #recursive
    for i in range (0, interation):
        newverts = []
        newfaces = []
        for j in range (0, int(len(baseverts)/4)):
            v0 = baseverts[j*4+0]
            v1 = baseverts[j*4+1]
            v2 = baseverts[j*4+2]
            v3 = baseverts[j*4+3]

            mid01 = 0.5*(v0+v1)
            mid02 = 0.5*(v0+v2)
            mid03 = 0.5*(v0+v3)
            mid12 = 0.5*(v1+v2)
            mid23 = 0.5*(v2+v3)
            mid31 = 0.5*(v3+v1)

            bottom = j*16 - 1
            add_poly4(newverts, newfaces, v0, mid01, mid02, mid03, bottom)
            bottom = j*16 + 3
            add_poly4(newverts, newfaces, mid01, v1, mid12, mid31, bottom)
            bottom = j*16 + 7
            add_poly4(newverts, newfaces, mid02, mid12, v2, mid23, bottom)
            bottom = j*16 + 11
            add_poly4(newverts, newfaces, mid03, mid31, mid23, v3, bottom)
        
        baseverts = newverts
        basefaces = newfaces

    return baseverts, basefaces

# Generate Sierpinski curtain mesh
def sier_cur_gen(interation):
    #base quad
    baseverts = []
    basefaces = []
    baseverts.append(Vector((1, 1, 0)))
    baseverts.append(Vector((-1, 1, 0)))
    baseverts.append(Vector((-1, -1, 0)))
    baseverts.append(Vector((1, -1, 0)))
    basefaces.append([0, 1, 2, 3])

    #recursive
    for i in range (0, interation):
        newverts = []
        newfaces = []
        for j in range (0, len(basefaces)):
            poly = basefaces[j]
            v0 = baseverts[poly[0]]
            v1 = baseverts[poly[1]]
            v2 = baseverts[poly[2]]
            v3 = baseverts[poly[3]]

            line_mid01_0 = 0.333333333*(2*v0 + v1)
            line_mid01_1 = 0.333333333*(v0 + 2*v1)
            line_mid12_0 = 0.333333333*(2*v1 + v2)
            line_mid12_1 = 0.333333333*(v1 + 2*v2)
            line_mid23_0 = 0.333333333*(2*v2 + v3)
            line_mid23_1 = 0.333333333*(v2 + 2*v3)
            line_mid30_0 = 0.333333333*(2*v3 + v0)
            line_mid30_1 = 0.333333333*(v3 + 2*v0)

            face_mid0 = 0.333333333*(2*line_mid01_0 + line_mid23_1)
            face_mid1 = 0.333333333*(2*line_mid01_1 + line_mid23_0)
            face_mid2 = 0.333333333*(line_mid01_1 + 2*line_mid23_0)
            face_mid3 = 0.333333333*(line_mid01_0 + 2*line_mid23_1)

            newverts.append(v0)
            newverts.append(line_mid01_0)
            newverts.append(line_mid01_1)
            newverts.append(v1)
            newverts.append(line_mid12_0)
            newverts.append(line_mid12_1)
            newverts.append(v2)
            newverts.append(line_mid23_0)
            newverts.append(line_mid23_1)
            newverts.append(v3)
            newverts.append(line_mid30_0)
            newverts.append(line_mid30_1)
            newverts.append(face_mid0)
            newverts.append(face_mid1)
            newverts.append(face_mid2)
            newverts.append(face_mid3)

            bottom = j*16 - 1
            newfaces.append([bottom+1, bottom+2, bottom+13, bottom+12])
            newfaces.append([bottom+2, bottom+3, bottom+14, bottom+13])
            newfaces.append([bottom+3, bottom+4, bottom+5, bottom+14])
            newfaces.append([bottom+14, bottom+5, bottom+6, bottom+15])
            newfaces.append([bottom+15, bottom+6, bottom+7, bottom+8])
            newfaces.append([bottom+16, bottom+15, bottom+8, bottom+9])
            newfaces.append([bottom+11, bottom+16, bottom+9, bottom+10])
            newfaces.append([bottom+12, bottom+13, bottom+16, bottom+11])
        
        baseverts = newverts
        basefaces = newfaces

    return baseverts, basefaces

# help function
def add_box(newverts, newfaces, center, len, bottom):
    v1 = center + len*Vector((1, 1, 1))
    v2 = center + len*Vector((-1, 1, 1))
    v3 = center + len*Vector((-1, -1, 1))
    v4 = center + len*Vector((1, -1, 1))
    v5 = center + len*Vector((1, 1, -1))
    v6 = center + len*Vector((-1, 1, -1))
    v7 = center + len*Vector((-1, -1, -1))
    v8 = center + len*Vector((1, -1, -1))

    newverts.append(v1)
    newverts.append(v2)
    newverts.append(v3)
    newverts.append(v4)
    newverts.append(v5)
    newverts.append(v6)
    newverts.append(v7)
    newverts.append(v8)

    newfaces.append([bottom+1, bottom+2, bottom+3, bottom+4])
    newfaces.append([bottom+1, bottom+5, bottom+6, bottom+2])
    newfaces.append([bottom+2, bottom+6, bottom+7, bottom+3])
    newfaces.append([bottom+3, bottom+7, bottom+8, bottom+4])
    newfaces.append([bottom+4, bottom+8, bottom+5, bottom+1])
    newfaces.append([bottom+8, bottom+7, bottom+6, bottom+5])

# Generate Sierpinski curtain mesh
def sier_cur_vol_gen(interation):
    #base quad
    baseverts = []
    basefaces = []
    baseverts.append(Vector((1, 1, 1)))
    baseverts.append(Vector((-1, 1, 1)))
    baseverts.append(Vector((-1, -1, 1)))
    baseverts.append(Vector((1, -1, 1)))
    baseverts.append(Vector((1, 1, -1)))
    baseverts.append(Vector((-1, 1, -1)))
    baseverts.append(Vector((-1, -1, -1)))
    baseverts.append(Vector((1, -1, -1)))

    basefaces.append([0, 1, 2, 3])
    basefaces.append([0, 4, 5, 1])
    basefaces.append([1, 5, 6, 2])
    basefaces.append([2, 6, 7, 3])
    basefaces.append([3, 7, 4, 0])
    basefaces.append([7, 6, 5, 4])

    #recursive
    for i in range (0, interation):
        newverts = []
        newfaces = []
        for j in range (0, int(len(baseverts)/8)):
            v0 = baseverts[j*8+0]
            v1 = baseverts[j*8+1]
            v2 = baseverts[j*8+2]
            v3 = baseverts[j*8+3]
            v4 = baseverts[j*8+4]
            v5 = baseverts[j*8+5]
            v6 = baseverts[j*8+6]
            v7 = baseverts[j*8+7]

            leng = abs(v0.x-v1.x)*0.5*0.333333333
            center = 0.5*(v0+v6)
            
            bottom = j*160 - 1
            add_box(newverts, newfaces, center + Vector((2*leng, 2*leng, 2*leng)), leng, bottom)
            bottom = j*160 + 7
            add_box(newverts, newfaces, center + Vector((0, 2*leng, 2*leng)), leng, bottom)
            bottom = j*160 + 15
            add_box(newverts, newfaces, center + Vector((-2*leng, 2*leng, 2*leng)), leng, bottom)
            bottom = j*160 + 23
            add_box(newverts, newfaces, center + Vector((-2*leng, 2*leng, 0)), leng, bottom)
            bottom = j*160 + 31
            add_box(newverts, newfaces, center + Vector((-2*leng, 2*leng, -2*leng)), leng, bottom)
            bottom = j*160 + 39
            add_box(newverts, newfaces, center + Vector((0, 2*leng, -2*leng)), leng, bottom)
            bottom = j*160 + 47
            add_box(newverts, newfaces, center + Vector((2*leng, 2*leng, -2*leng)), leng, bottom)
            bottom = j*160 + 55
            add_box(newverts, newfaces, center + Vector((2*leng, 2*leng, 0)), leng, bottom)

            bottom = j*160 + 63
            add_box(newverts, newfaces, center + Vector((2*leng, 0, 2*leng)), leng, bottom)
            bottom = j*160 + 71
            add_box(newverts, newfaces, center + Vector((2*leng, 0, -2*leng)), leng, bottom)
            bottom = j*160 + 79
            add_box(newverts, newfaces, center + Vector((-2*leng, 0, -2*leng)), leng, bottom)
            bottom = j*160 + 87
            add_box(newverts, newfaces, center + Vector((-2*leng, 0, 2*leng)), leng, bottom)

            bottom = j*160 + 95
            add_box(newverts, newfaces, center + Vector((2*leng, -2*leng, 2*leng)), leng, bottom)
            bottom = j*160 + 103
            add_box(newverts, newfaces, center + Vector((0, -2*leng, 2*leng)), leng, bottom)
            bottom = j*160 + 111
            add_box(newverts, newfaces, center + Vector((-2*leng, -2*leng, 2*leng)), leng, bottom)
            bottom = j*160 + 119
            add_box(newverts, newfaces, center + Vector((-2*leng, -2*leng, 0)), leng, bottom)
            bottom = j*160 + 127
            add_box(newverts, newfaces, center + Vector((-2*leng, -2*leng, -2*leng)), leng, bottom)
            bottom = j*160 + 135
            add_box(newverts, newfaces, center + Vector((0, -2*leng, -2*leng)), leng, bottom)
            bottom = j*160 + 143
            add_box(newverts, newfaces, center + Vector((2*leng, -2*leng, -2*leng)), leng, bottom)
            bottom = j*160 + 151
            add_box(newverts, newfaces, center + Vector((2*leng, -2*leng, 0)), leng, bottom)

        baseverts = newverts
        basefaces = newfaces

    return baseverts, basefaces
