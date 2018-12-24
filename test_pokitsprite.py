from pokitsprite import SpriteSheet, spritesheet_to_bytes

test_asset_root = 'test_assets'
test_image_suffix = '.png'
def test_image(subpath = 'SantaSheet'):
    return test_asset_root + '/' + subpath + test_image_suffix 


def test_asset_path_maker():
    assert test_image('SantaSheet') == 'test_assets/SantaSheet.png'

santasheet = SpriteSheet.FromFile(test_image('SantaSheet'), (16, 16), (0, 0, 0, 0))

def test_spritesheet_load():
    s = santasheet
    assert s.sprite_px.width == 16
    assert s.sprite_px.height == 16
    assert s.sprites_wide == 8
    assert s.sprites_high == 8
    assert len(s.sprites) == 64

def test_spritesheet_cuts_sprites():
    s = santasheet
    for counter, sprite in enumerate(santasheet):
        sprite.save(test_asset_root + '/out/' + str(counter) + ".png")

def test_sprite_to_bytes():
    assert 0 == len(spritesheet_to_bytes(santasheet))
