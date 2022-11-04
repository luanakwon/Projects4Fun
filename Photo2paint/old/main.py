import cv2
import numpy as np

print(1/(1+np.exp(-1.3862)))

img = cv2.imread('crop1.png')
img = (img/40).astype(np.uint8)*40
img = cv2.bilateralFilter(img,9,200,10)
print(img.dtype)
cv2.imshow('image',img)
cv2.waitKey()

