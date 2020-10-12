import numpy as np 
from PIL import Image
def rank_transform(img,w_size,K=18):

    w_boundary=int(w_size/2)
    transformed_img=np.zeros(img.shape,np.uint8)
    w_size_adjust=255/(w_size**2)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window=img[max(0,i-w_boundary):min(img.shape[0]-1,i+w_boundary),max(0,j-w_boundary):min(img.shape[1]-1,j+w_boundary)]
            median=np.median(window)
            rank=0
            for u in range(window.shape[0]):
                for v in range(window.shape[1]):
                    rank+=min(1,max(0,(window[u,v]-median)/K))
            transformed_img[i,j]=int(rank*w_size_adjust)
    return transformed_img
def ssd(filenamel,filenamer,kernel_size,max_disparity):
    imgl=Image.open(filenamel).convert('L')
    imgr=Image.open(filenamer).convert('L')
    imgl,imgr=np.asarray(imgl),np.asarray(imgr)
    assert imgl.shape==imgr.shape
    kernel_boundary=int(kernel_size/2)
    # imgl=np.pad(imgl,kernel_boundary,'constant')
    # print(imgl[4:-4,4:-4 ])
    # imgr=np.pad(imgr,kernel_boundary,'constant')

    disparity_map=np.zeros(imgl.shape,np.uint8)
    offset_adjust = 255 / max_disparity
    imgl=rank_transform(imgl,7)
    Image.fromarray(np.asarray(imgl)).save('imgl.jpg')
    imgr=rank_transform(imgr,7)
    Image.fromarray(np.asarray(imgr)).save('imgr.jpg')

    for x in range(kernel_boundary,imgr.shape[0]-kernel_boundary):
        for y in range(kernel_boundary,imgr.shape[1]-kernel_boundary):
            best_disparity=max_disparity
            loss=float('inf')
            
            for disparity in range(max_disparity):
                ssd=0
                # disparity+=1
                # left_boundary=max(y-disparity-kernel_boundary,0)
                # print(y+kernel_boundary-(y-kernel_boundary-min(y-disparity-kernel_boundary,0)),y-disparity+kernel_boundary-left_boundary)
                # if y-disparity+kernel_boundary<0:
                #     continue
                # ssd=imgl[x-kernel_boundary:x+kernel_boundary,y-kernel_boundary-min(y-disparity-kernel_boundary,0):y+kernel_boundary]-imgr[x-kernel_boundary:x+kernel_boundary,left_boundary:y-disparity+kernel_boundary]
                # ssd=(ssd**2/(ssd.shape[0]*ssd.shape[1])).sum()
                for u in range(-kernel_boundary,kernel_boundary):
                    for v in range( -kernel_boundary,kernel_boundary):
                        ssd_tmp=int(imgl[x+u,y+v])-int(imgr[x+u,y+v-disparity])
                        # ssd+=ssd_tmp*ssd_tmp
                        ssd+=abs(ssd_tmp)
                if ssd<loss:
                    loss=ssd
                    best_disparity=disparity

            disparity_map[x,y]=best_disparity*offset_adjust
        # exit()
    # color_coef=int(255/(np.max(disparity_map)-np.min(disparity_map)))

    # disparity_map=((disparity_map-np.min(disparity_map))*color_coef)
    # disparity_map=(disparity_map*(255/max_disparity))
    if np.max(disparity_map)>255:
        print('exceed 255')
        exit()
    print(disparity_map[0],type(disparity_map))
    Image.fromarray(np.asarray(disparity_map)).save('disparity_map.jpg')

ssd('xid-14489712_1.jpg','xid-14489713_1.jpg',6,30)
