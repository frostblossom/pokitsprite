from pokitsprite import read_in_image

test_asset_root = 'test_assets'
test_image_suffix = '.png'
def test_image(subpath = 'SantaSheet'):
    return test_asset_root + '/' + subpath + test_image_suffix 


def test_foo():
    assert test_image('SantaSheet') == 'test_assets/SantaSheet.png'