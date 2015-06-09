#!/usr/bin/env python

from gimpfu import *
from gimpenums import *

w = 350
h = 100

fg = (0, 0, 0)
bg = (255, 255, 255)

def gen_img(text, filename):
    image = gimp.Image(w, h, RGB)

    layer_bg = gimp.Layer(image, 'Button', w, h, RGB_IMAGE, 100, NORMAL_MODE)
    image.add_layer(layer_bg, 0)

    gimp.set_foreground((128, 128, 128))
    gimp.set_background((255, 255, 255))
    layer_bg.fill(BACKGROUND_FILL)
    pdb.gimp_edit_blend(layer_bg, FG_BG_RGB_MODE, NORMAL_MODE,
        GRADIENT_BILINEAR, 100, 0, 0, True, False, 0, 0, True, 0, h / 2, 0, h)

    gimp.set_foreground(fg)
    points = (0, 0, w, 0, w, h, 0, h, 0, 0)
    pdb.gimp_context_set_brush('Circle (05)')
    pdb.gimp_paintbrush_default(layer_bg, len(points), points)

    gimp.set_foreground(fg)
    layer_text = pdb.gimp_text_fontname(image, None, 0, 0, text, 10, True, 25,
        PIXELS, "Arial")
    xo = 100
    yo = (h - layer_text.height) / 2
    layer_text.translate(xo, yo)

    layer_logo = pdb.gimp_file_load_layer(image, "fcch-logo.png")
    yo = (h - layer_logo.height) / 2
    xo = yo
    layer_logo.translate(xo, yo)
    image.add_layer(layer_logo, 0)

    image.merge_visible_layers(0)
    layer_merged = image.layers[0]

    pdb.file_png_save(image, layer_merged, filename, "raw_filename", 0, 9, 0,
        0, 0, 0, 0)

plans = (
    ("First Month", "first-month"),
    ("Single Month", "single-month"),
    ("Monthly Plan", "monthly-plan"),
    ("Prepay One Year", "one-year"),
)

levels = (
    ("Student / Senior", "student-senior"),
    ("Individual", "individual"),
    ("Family", "family"),
    ("Sponsor", "sponsor"),
)

images = []
for plan in plans:
    for level in levels:
        images.append((level[0] + "\n" + plan[0],
            "shopping-" + plan[1] + "-" + level[1] + ".png"))
images.append(("View Cart", "shopping-view-cart.png"))
images.append(("Check Out", "shopping-check-out.png"))
images.append(("Donate Now", "shopping-donate-now.png"))

for (label, filename) in images:
    gen_img(label, filename)
