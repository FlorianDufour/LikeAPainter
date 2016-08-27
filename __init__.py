bl_info = {
    'name': 'Like A Painter',
    'author': 'Florian Dufour & Laurine Dufour',
    'version': (0, 0, 1),
    'blender': (2, 77, 0),
    'location': 'Node Editor > Add > Filter > LAPainter',
    'description': 'Node filter to transform an image input to an painting image',
    'warning': 'Alpha version',
    'wiki_url': '',
    'tracker_url': 'https://github.com/Whitefalcon42/LikeAPainter/',
    'support': 'COMMUNITY',
    'category': 'Node'}

#NOTE: Run this code first then use SHIFT-A, below, to add Custom Float node type.

import bpy
from bpy.types import NodeTree, Node, NodeSocket

# Implementation of custom nodes from Python
# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class LAPTree(NodeTree):
    bl_idname = 'LAPTreeType'
    bl_label = 'Custom Node Tree'

# Defines a poll function to enable filtering for various node tree types.
class LAPTreeNode :
    @classmethod
    def poll(cls, ntree):
        b = False
        # Make your node appear in different node trees by adding their bl_idname type here.
        if ntree.bl_idname == 'CompositorNodeTree': b = True
        return b

# Derived from the Node base type.
class LAPNode(Node, LAPTreeNode):
    '''A custom node'''
    bl_idname = 'LAPNodeType'
    bl_label = 'Like A Painter'
    bl_icon = 'INFO'

    def update_value(self, context):
        print("update")
        self.outputs["Image"].default_value = self.inputs["Image"].default_value
        self.update ()

    def init(self, context):
        self.inputs.new('NodeSocketColor', "Image")

        self.outputs.new('NodeSocketColor', "Image")
        self.outputs["Image"].default_value = self.inputs["Image"].default_value

    def update(self):
        #image_in = self.inputs["Image"]
        #if image_in.is_linked:
            #self.inputs["Image"].default_value =
        #self.outputs["Image"].default_value = self.inputs["Image"].get()

        try:
            image_in = self.inputs["Image"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if image_in.is_linked:
                for i in image_in.links:
                    if i.is_valid:
                        self.inputs["Image"].default_value = i.to_socket.node.outputs[i.to_socket.name].default_value

        try:
            image_out = self.outputs["Image"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if image_out.is_linked:
                for o in image_out.links:
                    if o.is_valid:
                        o.to_socket.node.inputs[o.to_socket.name].default_value = self.outputs["Image"].default_value
        # #Review linked outputs.
        # try:
        #     out = self.outputs["Image"]
        #     can_continue = True
        # except:
        #     can_continue = False
        # if can_continue:
        #     if out.is_linked:
        #         # I am an ouput node that is linked, try to update my link.
        #         for o in out.links:
        #             if o.is_valid:
        #                 o.to_socket.node.inputs[o.to_socket.name].default_value = self.inputs["Image"].default_value   #self.some_value

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "some_value",text = '')

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically.
    def draw_label(self):
        return "Like A Painter"

### Node Categories ###
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our target tree type
class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        b = False
        # Make your node appear in different node trees by adding their bl_idname type here.
        if context.space_data.tree_type == 'CompositorNodeTree': b = True
        return b

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory("SOMENODES", "Phoenix Nodes", items=[
        NodeItem("LAPNodeType"),
        ]),
    ]

def register():
    bpy.utils.register_class(LAPNode)
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    bpy.utils.unregister_class(LAPNode)

# def pre_frame_change(scene):
#     if scene.render.engine == 'CYCLES':
#         # Scan materials to see if I have a custom node within any of the trees.
#         for m in bpy.data.materials:
#             if m.node_tree != None:
#                 for n in m.node_tree.nodes:
#                     if n.bl_idname == 'LAPNodeType':
#                         print(n.bl_idname)
#                         # One of our custom nodes, let's update it.
#                         # When we set the value that will trigger an update inside the node.
#                         # Even if we change it to the same value it was.
#                         v = n.some_value
#                         n.some_value = v

if __name__ == "__main__":
    register()
    bpy.app.handlers.frame_change_pre.append(pre_frame_change)
