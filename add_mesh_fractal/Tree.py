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

import bpy
from bpy.types import Operator
from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        IntProperty,
        FloatVectorProperty,
        StringProperty,
        )
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from . import common_functions

def addspline(point1, point2, radius, curve):
    newSpline = curve.splines.new(type='POLY')
    newSpline.points.add(1)
    newSpline.points[0].co = (point1.x, point1.y, point1.z, 1)
    newSpline.points[0].radius = radius
    newSpline.points[1].co = (point2.x, point2.y, point2.z, 1)
    newSpline.points[1].radius = radius

def brunch(startpoint, direction, refdirection, length, radius, curve, iteration):

    if iteration <= 0:
        return

    length = 0.5*length
    radius = radius/(iteration+1)*iteration

    dir1 = (direction + refdirection).normalized()
    point1 = startpoint + length*dir1
    addspline(startpoint, point1, radius, curve)

    dir2 = (direction - refdirection).normalized()
    point2 = startpoint + length*dir2
    addspline(startpoint, point2, radius, curve)

    refdirnew = direction.cross(refdirection)*1.414
    dir3 = (direction + refdirnew).normalized()
    point3 = startpoint + length*dir3
    addspline(startpoint, point3, radius, curve)

    dir4 = (direction - refdirnew).normalized()
    point4 = startpoint + length*dir4
    addspline(startpoint, point4, radius, curve)

    # new brunch
    brunch(point1, dir1, refdirnew, length, radius, curve, iteration-1)
    brunch(point2, dir2, refdirnew, length, radius, curve, iteration-1)
    brunch(point3, dir3, refdirection, length, radius, curve, iteration-1)
    brunch(point4, dir4, refdirection, length, radius, curve, iteration-1)


def add_tree(iteration, context):
    # create curvedatablock
    curve = bpy.data.curves.new("Tree", type='CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = 0.01

    newpoints = [
        Vector((0,0,0)),
        Vector((0,0,1)),
    ]
    radius = 1
    addspline(newpoints[0], newpoints[1], radius, curve)

    startpoint = newpoints[1]
    direction = newpoints[1] - newpoints[0]
    refdirection = Vector((1,1,0))
    length = 1

    # create new spline
    brunch(startpoint, direction, refdirection, length, radius, curve, iteration)

    common_functions.create_curve_object(context, curve, "Tree")


class OBJECT_OT_add_tree(Operator, AddObjectHelper):
    """Create a new curve Object"""
    bl_idname = "curve.add_tree"
    bl_label = "Add Tree"
    bl_options = {'REGISTER', 'UNDO'}

    iteration: IntProperty(
        attr='tree_iteration',
        name='iteration', default=4,
        min=1, soft_min=1,
        max=8,
        description='Tree iteration',
    )

    def execute(self, context):

        add_tree(self.iteration, context)

        return {'FINISHED'}


# Registrate menu
def add_tree_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_tree.bl_idname,
        text="Add Tree",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_tree_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.curve.add_tree", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_tree)
    bpy.utils.register_manual_map(add_tree_manual_map)
    bpy.types.VIEW3D_MT_curve_add.append(add_tree_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_tree)
    bpy.utils.unregister_manual_map(add_tree_manual_map)
    bpy.types.VIEW3D_MT_curve_add.remove(add_tree_button)


if __name__ == "__main__":
    register()
