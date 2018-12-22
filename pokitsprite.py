from PIL import Image
import math as m
from collections import namedtuple

Margins = namedtuple('Margins', ['top', 'right', 'bottom', 'left'])
Area = namedtuple('Area', ['width', 'height'])

class SpriteSheet:
    def __init__(self, img,
                 sprite_px_area = None,
                 margins = Margins(0, 0, 0, 0)):
        self._img = img
        self.sheet_px = Area(img.size[0], img.size[1])
        self.sprite_px = Area(sprite_px_area[0], sprite_px_area[1]) if sprite_px_area else Area(self.sheet_px.width, self.sheet_px.height)
        self.margins = margins if isinstance(margins, Margins) else Margins(margins[0],margins[1],margins[2],margins[3],)
        self.sprite_region_px_width = self.sprite_px.width + self.margins.left + self.margins.right
        self.sprite_region_px_height = self.sprite_px.width + self.margins.top + self.margins.bottom
        self.sprites_wide = m.floor(self.sheet_px.width / (self.sprite_region_px_width))
        self.sprites_high = m.floor(self.sheet_px.height / (self.sprite_region_px_height))
        self.sprites = [x for x in generate_sprites(self)]

    def _make_sprite_seq_(self):
        pass

def generate_sprites(spritesheet):
    for sx in range(spritesheet.sprites_wide):
        for sy in range(spritesheet.sprites_high):
            inset_left = (spritesheet.sprite_region_px_width * sx) + spritesheet.margins.left
            inset_top = (spritesheet.sprite_region_px_height * sy) + spritesheet.margins.top
            inset_right = inset_left + spritesheet.sprite_px.width
            inset_bottom = inset_top + spritesheet.sprite_px.height
            yield spritesheet._img.crop((inset_left, inset_top, inset_right, inset_bottom))


def spritesheet_from_file (imgpath,
                           sprite_px_area = None,
                           margins = Margins(0, 0, 0, 0)):
    i = Image.open(imgpath)
    return SpriteSheet(i,
                       sprite_px_area,
                       margins)
