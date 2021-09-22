from PIL import Image
from PIL.ImageDraw import Draw

h = 1024
margin = 20
images = []
for i in range(1, 3):
    im = Image.open(f'/home/brandon/Downloads/hikers{i}.jpeg')
    w = im.width * h // im.height
    im = im.resize((w, h))
    white = Image.new(im.mode, im.size, 'white')
    mask = Image.new('L', im.size, 0)
    draw = Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), fill='white', width=0, radius=150)
    out = Image.composite(im, white, mask)
    images.append(out)
w = sum(im.width for im in images) + margin
out = Image.new(im.mode, (w, h), 'white')
out.paste(images[0], (0, 0))
out.paste(images[1], (images[0].width + margin, 0))
out.save('hikers.jpg')
