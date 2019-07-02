from openslide import open_slide

target_slname = './data/target/N14-02_02.svs'

target_slide = open_slide(target_slname)

x, y = target_slide.dimensions

patch_size = 1000
target = target_slide.read_region((x//2, y//2), 0, (patch_size, patch_size))

target.save('target.png')
