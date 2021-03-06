from PIL import Image

y1 = 90
y2 = 610
h = y2 - y1
im = Image.open('section3.png')
left_scale = im.crop((65,y1, 175,y2))
first_third = im.crop((175,y1, 901,y2))
second_third = im.crop((901,y1, 1358,y2))
third_third = im.crop((1358,y1, 1853,y2))
right_scale = im.crop((1853,y1-7, 1853+110,y2))
plan = [
    ['triptych1.png', [left_scale, first_third, right_scale], 306],
    ['triptych2.png', [left_scale, second_third, right_scale], 266],
    ['triptych3.png', [left_scale, third_third, right_scale], 224],
    #['triptych3.png', [left_scale, right_scale], 224],
]
for path, pieces, h in plan:
    w = sum(piece.size[0] for piece in pieces)
    out = Image.new(im.mode, (w, h))
    x = 0
    for piece in pieces:
        out.paste(piece, (x,0))
        x += piece.size[0]
    out.save(path)
