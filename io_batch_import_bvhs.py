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
# <pep8 compliant>


bl_info = {
    "name": "Batch Import BVH (.bvh)",
    "author": "ruslan",
    "version": (0, 5, 0),
    "blender": (3, 3, 0),
    "location": "File > Import-Export",
    "description": "Import multiple BVH files",
    "doc_url": "https://github.com/ruslanmustafin/blender-batch-import-bvh",
    "tracker_url": "https://github.com/ruslanmustafin/blender-batch-import-bvh",
    "category": "Import-Export"}


import bpy
from pathlib import Path

from bpy_extras.io_utils import ImportHelper

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       IntProperty,
                       EnumProperty,
                       CollectionProperty)


def negative_post_process(value):
    if 'NEGATIVE_' in value:
        return value.replace('NEGATIVE_', '-')
    return value


class ImportAnim_OT_batchBVH(bpy.types.Operator, ImportHelper):
    """Batch Import Wavefront"""
    bl_idname = "import_anim.bvh_import_batch"
    bl_label = "Import multiple BVH's"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".bvh"

    filter_glob = StringProperty(
            default="*.bvh",
            options={'HIDDEN'})

    files: CollectionProperty(type=bpy.types.PropertyGroup)

    clamp_size_setting: FloatProperty(
            name="Clamp Bounding Box",
            description="Resize the objects to keep bounding box" \
                    "under this value. Value 0 diables clamping",
            min=0.0, max=1000.0,
            soft_min=0.0, soft_max=1000.0,
            default=0.0)

    scale_setting: FloatProperty(
            name="Scale",
            description="Scale the BVH by this value",
            min=0.0, max=100.0,
            soft_min=0.0, soft_max=1000.0,
            default=1.0
    )

    rotation_setting: EnumProperty( # 'QUATERNION', 'NATIVE', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'
            name="Rotation",
            items=(('QUATERNION', "QUATERNION", ""),
                   ('NATIVE', "NATIVE", ""),
                   ('XYZ', "XYZ", ""),
                   ('XZY', "XZY", ""),
                   ('YXZ', "YXZ", ""),
                   ('YZX', "YZX", ""),
                   ('ZXY', "ZXY", ""),
                   ('ZYX', "ZYX", ""),
                   ),
            default='NATIVE')
    
    axis_forward_setting: EnumProperty(
            name="Forward Axis",
            items=(('X', "X", ""),
                   ('Y', "Y", ""),
                   ('Z', "Z", ""),
                   ('NEGATIVE_X', "-X", ""),
                   ('NEGATIVE_Y', "-Y", ""),
                   ('NEGATIVE_Z', "-Z", ""),
                   ),
            default='NEGATIVE_Z')
            
    axis_up_setting: EnumProperty(
            name="Up",
            items=(('X', "X", ""),
                   ('Y', "Y", ""),
                   ('Z', "Z", ""),
                   ('NEGATIVE_X', "-X", ""),
                   ('NEGATIVE_Y', "-Y", ""),
                   ('NEGATIVE_Z', "-Z", ""),
                   ),
            default='Y')

    start_frame_setting: IntProperty(
            name="Start frame",
            min=-10000,
            max=10000,
            soft_min=-10000,
            soft_max=10000,
            default=1
    )
            
    scale_fps_setting: BoolProperty(
            name="Scale FPS",
            description="")
    
    loop_setting: BoolProperty(
            name="Loop",
            description="")

    update_scene_fps_setting: BoolProperty(
            name="Update scene FPS",
            description="")

    update_scene_duration_setting: BoolProperty(
            name="Update scene duration",
            description="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        
        box = layout.box()
        box.label(text="Transform", icon='OBJECT_DATA')
        col = box.column()
        col.prop(self, "scale_setting")
        col.prop(self, "rotation_setting")
        col.prop(self, "axis_forward_setting")
        col.prop(self, "axis_up_setting")
        
        box = layout.box()
        box.label(text="Animation", icon='EXPORT')
        col = box.column()
        col.prop(self, "start_frame_setting")
        col.prop(self, "scale_fps_setting")
        col.prop(self, "loop_setting")
        col.prop(self, "update_scene_fps_setting")
        col.prop(self, "update_scene_duration_setting")


    def execute(self, context):
        folder = Path(self.filepath)
        for selection in self.files:
            fp = Path(folder.parent, selection.name)
            if fp.suffix == '.bvh':
                bpy.ops.import_anim.bvh(
                                filepath = str(fp),
                                axis_forward = negative_post_process(self.axis_forward_setting),
                                axis_up = negative_post_process(self.axis_up_setting),
                                global_scale = self.scale_setting,
                                frame_start = self.start_frame_setting,
                                use_fps_scale = self.scale_fps_setting,
                                update_scene_fps = self.update_scene_fps_setting,
                                update_scene_duration = self.update_scene_duration_setting,
                                use_cyclic = self.loop_setting,
                                rotate_mode = self.rotation_setting,
                                )
        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(
                ImportAnim_OT_batchBVH.bl_idname, 
                text="BVH Batch (.bvh)")

def register():
    bpy.utils.register_class(ImportAnim_OT_batchBVH)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportAnim_OT_batchBVH)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()
