import cv2
import numpy as np


a = np.zeros((500,500))
cv2.imshow('a',a)
key = cv2.waitKey()
print(key)