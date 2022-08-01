import numpy as np
import cv2

img = cv2.imread('/home/samarth/learningProject/resumes/Screenshot (44).png', 1)
# cv2.imshow('Original', img)

img_scale_up = cv2.resize(img, (0, 0), fx=1.5, fy=1.5)

# cv2.imshow('Upscaled Image', img_scale_up)
if not cv2.imwrite(r'/home/samarth/learningProject/upscaledimg11.png', img_scale_up):
    raise Exception('Could not write image')
cv2.waitKey(0)
# cv2.destroyAllWindows()