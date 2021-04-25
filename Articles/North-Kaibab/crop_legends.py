from PIL import Image

x0, x1 = 28, 628
h = 30
def r(y0, dx=0):
    return (x0+dx,y0, x1+dx,y0+h)
plan = [
    #(1, 'Mr', (x0,13+30, x1,104)),
    (1, 'Mr', r(13+30)),
    (1, 'Dtb', r(105)),
    (1, 'Cm', r(155)),
    (1, 'Cba', r(155+h)),
    (1, 'Ct', r(155+2*h)),
    (1, 'Yi', r(354-h)),
    (1, 'Yd', r(354)),
    (1, 'Ys', r(354+h)),
    (1, 'Yh', r(354+h*2)),
    (1, 'Yb', r(354+h*3)),
    (2, 'Xgr', r(77, 1)),
    (2, 'Xv', r(195, 1)),
    (2, 'Xbr', r(195+h, 1)),
    (2, 'Xr', r(195+2*h, 1)),
]
for n, name, coords in plan:
    im = Image.open(f'layers-screenshot-{n}.png')
    rect = im.crop(coords)
    data = list(rect.getdata(0))

    # At which x coordinate does the text label start?
    w = rect.width
    h = rect.height
    xhist = [
        min(data[x::w])
        for x in range(w)
    ]
    for x in range(72, w):
        if xhist[x] < 255:
            break

    # Move the text left so the gap between color and text is uniform.
    text = rect.crop((x,0, w,h))
    rect.paste(text, (80,0))

    rect.save('legend-' + name + '.png')
