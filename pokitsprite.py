from PIL import Image
import math as m
import os as os
from collections import namedtuple, Counter

Margins = namedtuple('Margins', ['top', 'right', 'bottom', 'left'])
Area = namedtuple('Area', ['width', 'height'])

famicubePalette = [

]

class SpriteSheet:
    @classmethod
    def FromFile(cls, imgpath, sprite_px_area = None, margins = Margins(0,0,0,0), palette_src = None):
        i = Image.open(imgpath)
        p = Image.open(palette_src if palette_src else os.path.dirname(imgpath) + '/palette.png') 
        return cls(i, sprite_px_area, margins, palette_img = p)

    def __init__(self, img,
                 sprite_px_area = None,
                 margins = Margins(0, 0, 0, 0), 
                 palette_img = None):
        self._img = img
        self.sheet_px = Area(img.size[0], img.size[1])
        self.sprite_px = Area(sprite_px_area[0], sprite_px_area[1]) if sprite_px_area else Area(self.sheet_px.width, self.sheet_px.height)
        self.margins = margins if isinstance(margins, Margins) else Margins(margins[0],margins[1],margins[2],margins[3],)
        self.sprite_region_px_width = self.sprite_px.width + self.margins.left + self.margins.right
        self.sprite_region_px_height = self.sprite_px.width + self.margins.top + self.margins.bottom
        self.sprites_wide = m.floor(self.sheet_px.width / (self.sprite_region_px_width))
        self.sprites_high = m.floor(self.sheet_px.height / (self.sprite_region_px_height))
        self.sprites = [x for x in generate_sprites(self)]
        self._palette_img = palette_img

    
    def __iter__(self):
        return self.sprites.__iter__()
    

def get_palette(spritesheet):
    # return [e for e in spritesheet._palette_img.getdata()]
    rawpalette = [e for e in spritesheet._palette_img.convert().getdata()]
    hashpalette = {(e[0], e[1], e[2]):n+1 for n, e in enumerate(rawpalette)}
    hashpalette.update({0: 0})
    return hashpalette

def get_spritesheet_colors(spritesheet):
    colors = Counter(spritesheet._img.getdata())
    return colors.most_common()

def get_sprite_colors(sprite):
    return [e[0] for e in Counter(sprite.getdata()).most_common() if e[0][3] > 128]

def getColorMapping(colorcount):
    # no_trans = [ (e[0][0], e[0][1], e[0][2]) for e in colorcount if e[0][3] < 126 ]
    return list(colorcount)

def generate_sprites(spritesheet):
    for sy in range(spritesheet.sprites_high):
        for sx in range(spritesheet.sprites_wide):
            inset_left = (spritesheet.sprite_region_px_width * sx) + spritesheet.margins.left
            inset_top = (spritesheet.sprite_region_px_height * sy) + spritesheet.margins.top
            inset_right = inset_left + spritesheet.sprite_px.width
            inset_bottom = inset_top + spritesheet.sprite_px.height
            yield spritesheet._img.crop((inset_left, inset_top, inset_right, inset_bottom))
        
def spritesheet_to_bytes(spritesheet):
    palette_convertion = get_palette(spritesheet)
    indexes = [sprite_index(e, palette_convertion) for e in spritesheet]
    shrunk = [shrink_palette_space(e) for e in indexes]
    tb_byte_array = build_initial_array(spritesheet)
    seperated_shrunk = seperate_shrunk_space(shrunk)
    tb_byte_array.append(len(seperated_shrunk['palettes']))
    for e in seperated_shrunk['palettes']:
        tb_byte_array.append(len(e))
        [tb_byte_array.append(n) for n in e]
    for e in seperated_shrunk['sprites']:
        rawsprite = e['seq']
        e['seq'] = compactify_sprite_seq(rawsprite)
    for e in seperated_shrunk['sprites']:
        tb_byte_array.append(e['mapping'])
        [tb_byte_array.append(n) for n in e['seq']]
    byteboi = bytearray(tb_byte_array)
    # print(byteboi)
    # print(tb_byte_array)
    # return byteman
    return byteboi

def compactify_sprite_seq(spriteseq):
    spriteseq = list(spriteseq)
    if (len(spriteseq) % 2 == 0):
        spriteseq.append(0)
    return [h << 4 | b for h, b in zip(*[iter(spriteseq)] * 2)]

def sprite_index(sprite, convertion_dict):
    return [convertion_dict.get(e, 0) for e in colors_for_sprite(sprite)]

def colors_for_sprite(sprite):
    l = [(e[0], e[1], e[2]) if e[3] > 126 else 0 for e in sprite.getdata()]
    return l

def shrink_palette_space(intseq):
    mappings = {0:0}
    reverts = [0]
    accum = []
    new_color_counter = 1
    for index in intseq:
        indmap = mappings.get(index, None)
        if (indmap != None):
            accum.append(indmap)
        else:
            mappings.update({index:new_color_counter})
            accum.append(new_color_counter)
            reverts.append(index)
            new_color_counter = new_color_counter + 1
    return {'mapping': reverts, 'seq': accum}

def seperate_shrunk_space(shrunk_sprites):
    paletterev = {(0,):0}
    palettes = [(0,)]
    palette_counter = 1
    for spriti in shrunk_sprites:
        palette = tuple(spriti['mapping'])
        data = spriti['seq']
        palette_ind = paletterev.get(palette, None)
        if (palette == (0)):
            spriti['mapping'] = 0
        elif (palette_ind != None):
            spriti['mapping'] = palette_ind
        else:
            paletterev.update({palette: palette_counter})
            palettes.append(palette)
            spriti['mapping'] = palette_counter
            palette_counter = palette_counter + 1
    return {'palettes': palettes, 'sprites': shrunk_sprites}


def build_initial_array(spritesheet):
    return [
        spritesheet.sprite_region_px_width,
        spritesheet.sprite_region_px_width
        ]