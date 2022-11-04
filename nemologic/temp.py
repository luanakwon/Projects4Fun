import cv2
import numpy as np

img = np.ones((728,728),dtype=np.uint8)*255
img[218:718,10:500] = 150


# img = cv2.addText(img,'20',(20,50),'Arial',pointSize=10,color=(0,0,0,0))
img = cv2.putText(img,'20',(20,50),cv2.FONT_HERSHEY_COMPLEX,0.5,0,1)




cv2.imshow('title', img)
cv2.waitKey()
