import numpy as np
import cv2
from tqdm import tqdm

def build_segmentation_3d(axials, sagittals, sgt_index):
    """
    axials: np array of shape (N,H,W). contains every axial 
    bone segmented images(bg=0, bone=1). axis order: (-z,-x,y) \n
    sagittals: np array of shape (n,N,H). contains some sagittal 
    label segmented images(bg=0,c1=1,c2=2,...c7=7). axis order: (y,-z,-x)\n
    sgt_index: y-wise indices of sagittal slices

    returns fillcount of each label, 
    axials of label segmented images of shape (N,H,W) (bg=0,c1=1,...,c7=7)
    """
    N, H, W = axials.shape

    # fillcount
    fillcount = [0,0,0,0,0,0,0,0]
    
    # choose the best sagittal image 
    sgt_y = np.argmax(np.sum(sagittals != 0,axis=(1,2)))
    sgt = sagittals[sgt_y]
    # some sagittal images are stretched into squares. 
    # resize sgt to match axial.shape[0]
    sgt = cv2.resize(sgt,(axials.shape[1],axials.shape[0]), \
                     interpolation=cv2.INTER_NEAREST)
    
    sgt_y = sgt_index[sgt_y]
    for z in range(N):
        # maybe
        # apply small gausian to properly seperate segments
        axials[z] = cv2.GaussianBlur(axials[z]*8,(3,3),1,1)
        # change bone label from 1 to 8 (to differentiate from c1)
        axials[z] = (axials[z] >= 7)*8
        
        sgt_strip = sgt[z]*(axials[z,:,sgt_y]==8)
        labels, ids_x = np.unique(sgt_strip,return_index=True)

        for label, idx_x in zip(labels, ids_x):
            label = int(label)
            if label != 0:
                if axials[z,idx_x, sgt_y] == 8:
                    ret = cv2.floodFill(axials[z],None,(sgt_y,idx_x),label)
                    fillcount[label] += ret[0]
                    axials[z] = ret[1]
                else:
                    while True:
                        idx_x += 1
                        # if idx_x out of range
                        if idx_x >= H:
                            #print(f'segment {label} at axials[{z}] is missing')
                            break
                        # if new seedpoint for label is found
                        elif sgt_strip[idx_x] == label and axials[z,idx_x,sgt_y] == 8:
                            ret = cv2.floodFill(axials[z],None,(sgt_y,idx_x),label)
                            fillcount[label] += ret[0]
                            axials[z] = ret[1]
                            break
    # initial fill from z=0 to z=N done
    # fill the unfilled patches dotted around
    for z in tqdm(range(N)):
        # find unlabeled bone(=8)
        i = 0
        ri, ci = (axials[z]==8).nonzero()
        while i < len(ri):
            adj_label = 0
            for z_, r_, c_ in [
                (z+1,ri[i],ci[i]),(z,ri[i]+1,ci[i]),(z,ri[i],ci[i]+1),
                (z-1,ri[i],ci[i]),(z,ri[i]-1,ci[i]),(z,ri[i],ci[i]-1),
                ]:
                if  0 <= z_ and z_ < N and\
                    0 <= r_ and r_ < H and\
                    0 <= c_ and c_ < W :
                    if 0 < axials[z_,r_,c_] and axials[z_,r_,c_] < 8:
                        if adj_label == 0:
                            adj_label = axials[z_,r_,c_]
                        elif adj_label == axials[z_,r_,c_]:
                            continue
                        else: # adj_label != axials[z_,r_,c_]
                            adj_label = 0
                            break
            if 0 < adj_label: # 0 < adj < 8
                # 3d fill from z, ri[i], ci[i]
                cnt, axials = fill3d(axials,ci[i],ri[i],z,adj_label)
                fillcount[adj_label] += cnt
                i = 0
                ri, ci = (axials[z]==8).nonzero()
            else:
                i+=1
    return fillcount, axials


def fill(img, x, y, color):
    """
    img  : np array of shape (H,W,C) \n
    x, y : start point of fill (origin: top left) \n
    color: fill color of shape (B, G, R)  
    
    returns img  
    """
    count = 0
    queue = []
    cur_color = img[y, x].copy()
    img[y,x,:] = color
    queue.append((x,y))
    height, width = img.shape[:2]
    while len(queue) != 0:
        count+=1
        x, y = queue.pop(0)
        # for neighboring pixels
        for x2, y2 in [(x-1,y),(x+1,y),(x,y+1),(x,y-1)]:
            # if it is not out of bound
            if 0<=x2 and x2<width and 0<=y2 and y2<height:
                # if the color is same
                if (img[y2,x2] == cur_color).all():
                    # fill this pixel
                    img[y2,x2,:] = color
                    queue.append((x2,y2))
    return count, img

def fill3d(vol, x, y, z, color):
    """
    vol  : volume, np array of shape (D,H,W,C) \n
    x, y, z : start point of fill -> vol[z,y,x] \n
    color: fill color of shape (B, G, R)  \n
    returns img  
    """
    count = 0
    queue = []
    cur_color = vol[z, y, x].copy()
    vol[z,y,x] = color
    queue.append((x,y,z))
    depth, height, width = vol.shape[:3]
    while len(queue) != 0:
        count+=1
        x, y, z = queue.pop(0)
        # for neighboring pixels
        for x2, y2, z2 in \
            [(x-1,y,z),(x+1,y,z),(x,y+1,z),(x,y-1,z),(x,y,z-1),(x,y,z+1)]:
            # if it is not out of bound
            if 0<=x2 and x2<width and 0<=y2 and y2<height and 0<=z2 and z2<depth:
                # if the color is same
                if (vol[z2,y2,x2] == cur_color).all():
                    # fill this pixel
                    vol[z2,y2,x2] = color
                    queue.append((x2,y2,z2))
    return count, vol





            # adj_label = 0
            # # if first, only see one after
            # if z == 0:
            #     if axials[z+1,ri[i],ci[i]] != 0:
            #         adj_label = axials[z+1,ri[i],ci[i]]
            # # if last, only see one before
            # elif z == N-1:
            #     if axials[z-1,ri[i],ci[i]] != 0:
            #         adj_label = axials[z-1,ri[i],ci[i]]
            # # if middle, see both
            # else:               
            #     voxBef = axials[z-1,ri[i],ci[i]]
            #     voxAft = axials[z+1,ri[i],ci[i]]
            #     voxBef = voxAft if voxBef == 0 else voxBef
            #     voxAft = voxBef if voxAft == 0 else voxAft
            #     # if same label
            #     if voxBef == voxAft:
            #         adj_label = voxBef
            #     # if one is bone
            #     elif voxBef == 8:
            #         adj_label = voxAft
            #     elif voxAft == 8:
            #         adj_label = voxBef
            #     # if no bone, different label 
            #     else:
            #         adj_label = 0
                    
            # # if adjcent label is black(=0) and no bones around, color itself black
            # if adj_label == 0:
            #     no_bone = True
            #     for r_, c_ in [(ri[i]+1,ci[i]),(ri[i]-1,ci[i]),(ri[i],ci[i]+1),(ri[i],ci[i]-1)]:
            #         if 0<=r_ and r_<H and 0<=c_ and c_<W:
            #             if axials[z,r_,c_] == 8:
            #                 no_bone = False
            #                 break
            #     if no_bone:
            #         axials[z,ri[i],ci[i]] = 0
            # elif 

            



                                
                    

        