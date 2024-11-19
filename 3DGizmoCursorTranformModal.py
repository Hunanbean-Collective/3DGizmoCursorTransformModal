# Coding Credit to CGPT. Based on Prompts by Hunanbean
import bpy

def snap_cursor_to_empty(scene):
    """Syncs the 3D Cursor to the Empty's location."""
    empty = bpy.data.objects.get("CursorVisualizer")
    if empty and bpy.context.active_object != empty:
        bpy.context.scene.cursor.location = empty.location

def auto_select_cursor_visualizer():
    """Automatically selects the CursorVisualizer when using the Cursor tool."""
    if bpy.context.scene.tool_settings.transform_pivot_point == 'CURSOR':
        empty = bpy.data.objects.get("CursorVisualizer")
        if empty and bpy.context.active_object != empty:
            bpy.context.view_layer.objects.active = empty
            bpy.ops.object.select_all(action='DESELECT')
            empty.select_set(True)

class CursorVisualizerHandler(bpy.types.Operator):
    """Operator to manage Cursor Visualizer integration."""
    bl_idname = "wm.cursor_visualizer_handler"
    bl_label = "Cursor Visualizer Handler"
    bl_options = {'REGISTER'}

    _timer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            auto_select_cursor_visualizer()
        return {'PASS_THROUGH'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)

# Ensure the CursorVisualizer Empty exists
if "CursorVisualizer" not in bpy.data.objects:
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=bpy.context.scene.cursor.location)
    empty = bpy.context.active_object
    empty.name = "CursorVisualizer"
else:
    empty = bpy.data.objects["CursorVisualizer"]
    empty.location = bpy.context.scene.cursor.location

# Ensure handlers are added
if not any(handler.__name__ == "snap_cursor_to_empty" for handler in bpy.app.handlers.depsgraph_update_post):
    bpy.app.handlers.depsgraph_update_post.append(snap_cursor_to_empty)

# Register and start the modal operator
if not bpy.app.timers.is_registered(CursorVisualizerHandler):
    bpy.utils.register_class(CursorVisualizerHandler)
    bpy.ops.wm.cursor_visualizer_handler()

print("Enhanced Cursor Visualizer setup complete.")
