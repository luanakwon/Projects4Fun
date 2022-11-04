from typing import ValuesView
import cv2
import numpy as np

def get_line_label(line):
    out = []
    pxl_0 = 1
    j_len = 0
    for pxl in line:
        # if this pixel is black
        # inc len
        if pxl == 0:
            j_len += 1
        # if this pixel is not black but last pixel is black
        # write j_len and reset
        elif pxl != 0 and pxl_0 == 0:
            out.append(j_len)
            j_len = 0
        # if this pixel is not black and last pixel is not black
        # do nothing
        pxl_0 = pxl
    # if last pixel is black, append len
    if line[-1] == 0:
        out.append(j_len)
    
    return out

def format_n_print(labels, max_len, orientation, indent = 0):
    if orientation == 'horizontal':
        out = np.zeros((len(labels),max_len),dtype=np.int32)
        for i, label in enumerate(labels):
            out[i,max_len-len(label):] = np.array(label)
        out = np.transpose(out)
        for idx, line_out in enumerate(out):
            sep = ',' if idx+1 < len(out) else '.'
            sep_empty = '    ' if idx+1 < len(out) else '   .'
            line_str = ''
            for item in line_out:
                line_str += '%3d%c'%(item,sep) if item != 0 else sep_empty
            print(line_str)
    elif orientation == 'vertical':
        for label in labels:
            print(f"{' '*indent}{label}")
    else:
        raise ValueError("orientation should be either 'horizontal' or 'vertical'")

def plot_labels(img, labels, orientation):
    if orientation == 'horizontal':
        for i, label in enumerate(labels):
            for j, item in enumerate(label):
                img = cv2.putText(img,f'{item}',
                        (int(10+i*(500/len(labels))),218-(len(label)-j-1)*23),
                        cv2.FONT_HERSHEY_COMPLEX,0.5,0,1)
    elif orientation == 'vertical':
        for i, label in enumerate(labels):
            img = cv2.putText(img, f'{label}'.strip('[]'),
                    (510,int(222+i*(500/len(labels)))),
                    cv2.FONT_HERSHEY_COMPLEX,0.5,0,1)
    else:
        raise ValueError("orientation should be either 'horizontal' or 'vertical'")

    return img

def plot_grid(img, n_rows, n_cols):
    ycors = np.linspace(218,718,n_rows+1).astype(np.int32)+7
    xcors = np.linspace(10,510,n_cols+1).astype(np.int32)-5
    for y in ycors:
        img[y,5:505] = 0
    for x in xcors:
        img[225:725,x] = 0
    return img

img_path = 'simbol_at.png'
# img_path = 'tree.png'
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
# check if file exists
if not isinstance(img,np.ndarray):
    raise FileNotFoundError(img_path)

H, W = img.shape
# binerize image
img = img*(img>128)
# label to be printed on top
y_label = []
# label to be printed on the right
x_label = []

# fill y_label 
y_label_max_len = 0
for i in range(W):
    line = img[:,i]
    label = get_line_label(line)
    y_label_max_len = max(y_label_max_len,len(label))
    y_label.append(label)
# fill x_label
x_label_max_len = 0
for line in img:
    label = get_line_label(line)
    x_label_max_len = max(x_label_max_len,len(label))
    x_label.append(label)

format_n_print(y_label,y_label_max_len,orientation='horizontal')
format_n_print(x_label,0,orientation='vertical',indent=4*len(y_label))

blank = np.ones((728,728),dtype=np.uint8)*255
blank = plot_labels(blank,y_label,'horizontal')
blank = plot_labels(blank,x_label,'vertical')
blank = plot_grid(blank,len(x_label),len(y_label))


cv2.imshow('blank',blank)
cv2.waitKey()

cv2.imwrite(f'quest_{img_path}',blank)