from PIL import Image

x0, x1 = 28, 628
h = 30
def r(y0, dx=0):
    return (x0+dx,y0, x1+dx,y0+h)
plan = [
    (1, 'Mr', (x0,13+30, x1,104)),
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
    rect.save('legend-' + name + '.png')
