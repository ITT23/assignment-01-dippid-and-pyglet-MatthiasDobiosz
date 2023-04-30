import pyglet

class SpriteWithBbox:

    def __init__(self, img, offset_left, offset_right, offset_bottom, offset_top):
        self.offset_left = offset_left
        self.offset_right = offset_right
        self.offset_bottom = offset_bottom
        self.offset_top = offset_top
        self.width = img.width - (offset_left+offset_right)
        self.height = img.height - (offset_bottom + offset_top)
        self.img = img

