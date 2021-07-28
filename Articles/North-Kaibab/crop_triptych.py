from PIL import Image

im = Image.open('section3.png')

y1 = 140
y2 = im.height
bottom_margin = 60

left_scale = im.crop((20,y1, 93,y2))
river = im.crop((176+25,y1, 312,y2))
first_third_a = im.crop((412,y1, 556,y2)) # skip pixel to avoid vertical line
first_third_b = im.crop((557,y1, 873,y2))
width = river.width + (first_third_a.width + first_third_b.width)
second_third = im.crop((811,y1, 1377,y2))
third_third = im.crop((1302,y1, 1853,y2))
right_scale = im.crop((91,y1, 91+(93-20),y2))
plan = [
    ['triptych1.png', [left_scale, river, first_third_a,
                       first_third_b, right_scale], 277],
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
