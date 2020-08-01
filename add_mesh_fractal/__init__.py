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

bl_info = {
    "name": "FractalFactory",
    "author": "Wu Ning",
    "version": (0, 1, 0),
    "blender":  (2, 80, 0),
    "location": "View3D",
    "description": "Add a Fractal model",
    "warning": "WIP",
    "wiki_url": "",
    "category": "Add Mesh",
}


if "bpy" in locals():
    import importlib
    importlib.reload(SierpinskiTriangle)
    importlib.reload(SierpinskiCurtain)
    importlib.reload(SierpinskiTriangleVolume)
    importlib.reload(SierpinskiCurtainVolume)
    importlib.reload(Tree)
else:
    from . import SierpinskiTriangle
    from . import SierpinskiCurtain
    from . import SierpinskiTriangleVolume
    from . import SierpinskiCurtainVolume
    from . import Tree

import bpy


# ### REGISTER ###

classes = (
    SierpinskiTriangle,
    SierpinskiCurtain,
    SierpinskiTriangleVolume,
    SierpinskiCurtainVolume,
    Tree,
)

def register():
    SierpinskiTriangle.register()
    SierpinskiCurtain.register()
    SierpinskiTriangleVolume.register()
    SierpinskiCurtainVolume.register()
    Tree.register()

def unregister():
    SierpinskiTriangle.unregister()
    SierpinskiCurtain.unregister()
    SierpinskiTriangleVolume.unregister()
    SierpinskiCurtainVolume.unregister()
    Tree.unregister()

if __name__ == "__main__":
    register()
