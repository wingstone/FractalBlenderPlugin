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

def add_sierpinski_curtain(interation, context):
    verts, faces = common_functions.sier_cur_gen(interation)
    common_functions.create_mesh_object(context, verts, [], faces, "sierpinski_cur")

class OBJECT_OT_add_sier_cur(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_sierpinski_curtain"
    bl_label = "Add Sierpinski Curtain"
    bl_options = {'REGISTER', 'UNDO'}

    iteration: IntProperty(
        attr='sierpinski_curtain_iteration',
        name='iteration', default=3,
        min=1, soft_min=1,
        max=5,
        description='Sierpinski iteration',
    )

    def execute(self, context):

        add_sierpinski_curtain(self.iteration, context)

        return {'FINISHED'}


# Registrate menu
def add_sier_cur_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_sier_cur.bl_idname,
        text="Add Sierpinski Curtain",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_sier_cur_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_sierpinski_curtain", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_sier_cur)
    bpy.utils.register_manual_map(add_sier_cur_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_sier_cur_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_sier_cur)
    bpy.utils.unregister_manual_map(add_sier_cur_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_sier_cur_button)


if __name__ == "__main__":
    register()
