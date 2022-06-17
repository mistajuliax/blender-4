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
    "name": "Clip Editor Pies: Key: 'hotkey list Below'",
    "description": "Clip Editor Pies",
    "author": "Antony Riakiotakis, Sebastian Koenig",
    "version": (0, 1, 1),
    "blender": (2, 77, 0),
    "location": "Q, W, Shift W, E, Shift S, Shift A, Shift E",
    "warning": "",
    "wiki_url": "",
    "category": "Pie Menu"
    }

import bpy
from bpy.types import Menu, Operator



##############################
# CLASSES
##############################


class CLIP_PIE_refine_pie(Menu):
    # Refinement Options
    bl_label = "Refine Intrinsics"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return (space.type == 'CLIP_EDITOR') and space.clip

    def draw(self, context):
        clip = context.space_data.clip
        settings = clip.tracking.settings

        layout = self.layout
        pie = layout.menu_pie()
        pie.prop(settings, "refine_intrinsics", expand=True)


class CLIP_PIE_geometry_reconstruction(Menu):
    # Geometry Reconstruction
    bl_label = "Reconstruction"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("clip.bundles_to_mesh", icon='MESH_DATA')
        pie.operator("clip.track_to_empty", icon='EMPTY_DATA')


class CLIP_PIE_display_pie(Menu):
    # Display Options
    bl_label = "Marker Display"

    def draw(self, context):
        space = context.space_data

        layout = self.layout
        pie = layout.menu_pie()
        pie.prop(space, "show_names", text="Show Track Info", icon='WORDWRAP_ON')
        pie.prop(space, "show_disabled", text="Show Disabled Tracks", icon='VISIBLE_IPO_ON')
        pie.prop(space, "show_marker_search", text="Display Search Area", icon='VIEWZOOM')
        pie.prop(space, "show_marker_pattern", text="Display Pattern Area", icon='BORDERMOVE')


class CLIP_PIE_marker_pie(Menu):
    # Settings for the individual markers
    bl_label = "Marker Settings"

    def draw(self, context):
        clip = context.space_data.clip
        tracks = getattr(getattr(clip, "tracking", None), "tracks", None)
        track_active = tracks.active if tracks else None

        layout = self.layout
        pie = layout.menu_pie()
        # Use Location Tracking
        prop = pie.operator("wm.context_set_enum", text="Loc", icon='OUTLINER_DATA_EMPTY')
        prop.data_path = "space_data.clip.tracking.tracks.active.motion_model"
        prop.value = "Loc"
        # Use Affine Tracking
        prop = pie.operator("wm.context_set_enum", text="Affine", icon='OUTLINER_DATA_LATTICE')
        prop.data_path = "space_data.clip.tracking.tracks.active.motion_model"
        prop.value = "Affine"
        # Copy Settings From Active To Selected 
        pie.operator("clip.track_settings_to_track", icon='COPYDOWN')
        # Make Settings Default
        pie.operator("clip.track_settings_as_default", icon='SETTINGS')
        if track_active:
        # Use Normalization
            pie.prop(track_active, "use_normalization", text="Normalization")
        # Use Brute Force
            pie.prop(track_active, "use_brute", text="Use Brute Force")
        # Use The blue Channel
            pie.prop(track_active, "use_blue_channel", text="Blue Channel")
        # Match Either Previous Frame Or Keyframe
            if track_active.pattern_match == "PREV_FRAME":
                prop = pie.operator("wm.context_set_enum", text="Match Previous", icon='KEYINGSET')
                prop.value = 'KEYFRAME'
            else:
                prop = pie.operator("wm.context_set_enum", text="Match Keyframe", icon='KEY_HLT')
                prop.value = 'PREV_FRAME'

            prop.data_path = "space_data.clip.tracking.tracks.active.pattern_match"


class CLIP_PIE_tracking_pie(Menu):
    # Tracking Operators
    bl_label = "Tracking"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Track Backwards
        prop = pie.operator("clip.track_markers", icon='PLAY_REVERSE')
        prop.backwards = True
        prop.sequence = True
        # Track Forwards
        prop = pie.operator("clip.track_markers", icon='PLAY')
        prop.backwards = False
        prop.sequence = True
        # Disable Marker
        pie.operator("clip.disable_markers", icon='RESTRICT_VIEW_ON').action = 'TOGGLE'
        # Detect Features
        pie.operator("clip.detect_features", icon='ZOOM_SELECTED')
        # Clear Path Backwards
        pie.operator("clip.clear_track_path", icon='BACK').action = 'UPTO'
        # Clear Path Forwards
        pie.operator("clip.clear_track_path", icon='FORWARD').action = 'REMAINED'
        # Refine Backwards
        pie.operator("clip.refine_markers", icon='LOOP_BACK').backwards = True
        # Refine Forwards
        pie.operator("clip.refine_markers", icon='LOOP_FORWARDS').backwards = False


class CLIP_PIE_clipsetup_pie(Menu):
    # Setup the clip display options
    bl_label = "Clip and Display Setup"

    def draw(self, context):
        space = context.space_data

        layout = self.layout
        pie = layout.menu_pie()
        # Reload Footage
        pie.operator("clip.reload", text="Reload Footage", icon='FILE_REFRESH')
        # Prefetch Footage
        pie.operator("clip.prefetch", text="Prefetch Footage", icon='LOOP_FORWARDS')
        # Mute Footage
        pie.prop(space, "use_mute_footage", text="Mute Footage", icon='MUTE_IPO_ON')
        # Render Undistorted
        pie.prop(space.clip_user, "use_render_undistorted", text="Render Undistorted")
        # Set Scene Frames
        pie.operator("clip.set_scene_frames", text="Set Scene Frames", icon='SCENE_DATA')
        # PIE: Marker Display
        pie.operator("wm.call_menu_pie", text="Marker Display", icon='PLUS').name = "CLIP_PIE_display_pie"
        # Set Active Clip
        pie.operator("clip.set_active_clip", icon='CLIP')
        # Lock Selection
        pie.prop(space, "lock_selection", icon='LOCKED')


class CLIP_PIE_solver_pie(Menu):
    # Operators to solve the scene
    bl_label = "Solving"

    def draw(self, context):
        clip = context.space_data.clip
        settings = getattr(getattr(clip, "tracking", None), "settings", None)

        layout = self.layout
        pie = layout.menu_pie()
        # create Plane Track
        pie.operator("clip.create_plane_track", icon='MESH_PLANE')
        # Solve Camera
        pie.operator("clip.solve_camera", text="Solve Camera", icon='OUTLINER_OB_CAMERA')
        # PIE: Refinement
        if settings:
            pie.operator("wm.call_menu_pie", text="Refinement",
                        icon='CAMERA_DATA').name = "CLIP_PIE_refine_pie"
        # Use Tripod Solver
            pie.prop(settings, "use_tripod_solver", text="Tripod Solver")
        # Set Keyframe A
        pie.operator("clip.set_solver_keyframe", text="Set Keyframe A",
                    icon='KEY_HLT').keyframe = 'KEYFRAME_A'
        # Set Keyframe B
        pie.operator("clip.set_solver_keyframe", text="Set Keyframe B",
                    icon='KEY_HLT').keyframe = 'KEYFRAME_B'
        # Clean Tracks
        prop = pie.operator("clip.clean_tracks", icon='STICKY_UVS_DISABLE')
        # Filter Tracks
        pie.operator("clip.filter_tracks", icon='FILTER')
        prop.frames = 15
        prop.error = 2


class CLIP_PIE_reconstruction_pie(Menu):
    # Scene Reconstruction
    bl_label = "Reconstruction"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Set Active Clip As Viewport Background
        pie.operator("clip.set_viewport_background", text="Set Viewport Background", icon='SCENE_DATA')
        # Setup Tracking Scene
        pie.operator("clip.setup_tracking_scene", text="Setup Tracking Scene", icon='SCENE_DATA')
        # Setup Floor
        pie.operator("clip.set_plane", text="Setup Floor", icon='MESH_PLANE')
        # Set Origin
        pie.operator("clip.set_origin", text="Set Origin", icon='MANIPUL')
        # Set X Axis
        pie.operator("clip.set_axis", text="Set X Axis", icon='AXIS_FRONT').axis = 'X'
        # Set Y Axis
        pie.operator("clip.set_axis", text="Set Y Axis", icon='AXIS_SIDE').axis = 'Y'
        # Set Scale
        pie.operator("clip.set_scale", text="Set Scale", icon='ARROW_LEFTRIGHT')
        # PIE: Reconstruction
        pie.operator("wm.call_menu_pie", text="Reconstruction",
                    icon='MESH_DATA').name = "CLIP_PIE_geometry_reconstruction"


class CLIP_PIE_timecontrol_pie(Menu):
    # Time Controls
    bl_label = "Time Control"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # Jump To Startframe
        pie.operator("screen.frame_jump", text="Jump to Startframe", icon='TRIA_LEFT').end = False
        # Jump To Endframe
        pie.operator("screen.frame_jump", text="Jump to Endframe", icon='TRIA_RIGHT').end = True
        # Jump To Start Of The Track
        pie.operator("clip.frame_jump", text="Start of Track", icon='REW').position = 'PATHSTART'
        # Jump To End of The Track
        pie.operator("clip.frame_jump", text="End of Track", icon='FF').position = 'PATHEND'
        # Play Backwards
        pie.operator("screen.animation_play", text="Playback Backwards", icon='PLAY_REVERSE').reverse = True
        # Play Forwards
        pie.operator("screen.animation_play", text="Playback Forwards", icon='PLAY').reverse = False
        # Go One Frame Back
        pie.operator("screen.frame_offset", text="Previous Frame", icon='TRIA_LEFT').delta = -1
        # Go One Frame Forwards
        pie.operator("screen.frame_offset", text="Next Frame", icon='TRIA_RIGHT').delta = 1



addon_keymaps = []

classes = (
    CLIP_OT_select_zero_weighted,
    CLIP_OT_weight_fade,
    CLIP_PIE_geometry_reconstruction,
    CLIP_PIE_tracking_pie,
    CLIP_PIE_display_pie,
    CLIP_PIE_marker_pie,
    CLIP_PIE_solver_pie,
    CLIP_PIE_refine_pie,
    CLIP_PIE_reconstruction_pie,
    CLIP_PIE_clipsetup_pie,
    CLIP_PIE_timecontrol_pie
)


def register():
    addon_keymaps.clear()
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:

        km = wm.keyconfigs.addon.keymaps.new(name="Clip", space_type='CLIP_EDITOR')

        kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS')
        kmi.properties.name = "CLIP_PIE_marker_pie"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", 'W', 'PRESS')
        kmi.properties.name = "CLIP_PIE_clipsetup_pie"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", 'E', 'PRESS')
        kmi.properties.name = "CLIP_PIE_tracking_pie"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", 'S', 'PRESS', shift=True)
        kmi.properties.name = "CLIP_PIE_solver_pie"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", 'W', 'PRESS', shift=True)
        kmi.properties.name = "CLIP_PIE_reconstruction_pie"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", 'A', 'PRESS', shift=True)
        kmi.properties.name = "CLIP_PIE_timecontrol_pie"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", 'E', 'PRESS', shift=True)
        kmi.properties.name = "CLIP_PIE_tracking_tools"
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    if kc := wm.keyconfigs.addon:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
