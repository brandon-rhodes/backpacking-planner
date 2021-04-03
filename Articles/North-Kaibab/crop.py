from PIL import Image

im = Image.open('section3.png')

y1 = 140
y2 = im.height
bottom_margin = 60

left_scale = im.crop((20,y1, 93,y2))
river = im.crop((176,y1, 312,y2))
first_third = im.crop((412,y1, 920,y2))
second_third = im.crop((890,y1, 1445,y2))
third_third = im.crop((1300,y1, 1853,y2))
right_scale = im.crop((91,y1, 91+(93-20),y2))
plan = [
    ['triptych1.png', [left_scale, river, first_third, right_scale], 270],
    ['triptych2.png', [left_scale, second_third, right_scale], 250],
    ['triptych3.png', [left_scale, third_third, right_scale], 230],
]
for path, pieces, h in plan:
    w = sum(piece.size[0] for piece in pieces)
    out = Image.new(im.mode, (w, h + bottom_margin))
    x = 0
    for p in pieces:
        out.paste(p, (x,0))
        out.paste(p.crop((0,435, p.width,p.height)), (x,h))
        x += p.size[0]
    out.save(path)
