#!/usr/bin/env python

# import matplotlib.pyplot as plt
# import numpy as np
# import cv2

# a = 'www.bobbordasch.com/trips/GC-Oct13-Flip/Map-Day1.jpg'
# b = 'www.bobbordasch.com/trips/GC-Oct13-Flip/Map-Day2.jpg'
a, b = 'a.jpg', 'b.jpg'
o = 'locations.png'

# image = cv2.imread(a)
# template = cv2.imread(b)
# heat_map = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# h, w, _ = template.shape
# y, x = np.unravel_index(np.argmax(heat_map), heat_map.shape)
# cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 5)

# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
#imagePaths = sorted(list(paths.list_images(args["images"])))

copyright_height = 14
imagePaths = [a, b]

images = []
# loop over the image paths, load each one, and add them to our
# images to stitch list

# Successful attempt to remove header and footer from each image:

def crop_image(image):
    height, width, depth = image.shape
    y_brightness = image.sum(axis=(1,2))
    y_top = np.argmin(y_brightness[:100])
    y_bottom = height - 100 + np.argmin(y_brightness[-100:])
    #print('top and bottom:', y_top, y_bottom)
    image = image[y_top + 1 : y_bottom - 1 - copyright_height]
    return image

for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    original_shape = image.shape
    image = crop_image(image)
    print(original_shape, '->', image.shape)
    images.append(image)
    cv2.imwrite(o, image)
    # exit()

# initialize OpenCV's image stitcher object and then perform the image
# stitching
print("[INFO] stitching images...")
print(imutils.is_cv3())
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
#print(stitcher.mode)
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
    # write the output stitched image to disk
    cv2.imwrite(o, stitched)
    # display the output stitched image to our screen
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
    # otherwise the stitching failed, likely due to not enough keypoints)
    # being detected
else:
    print("[INFO] image stitching failed ({})".format(status))
