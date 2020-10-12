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
def LRC(filenamel,filenamer,kernel_size,max_disparity):
    imgl=Image.open(filenamel).convert('L')
    imgr=Image.open(filenamer).convert('L')
    imgl,imgr=np.asarray(imgl),np.asarray(imgr)
    assert imgl.shape==imgr.shape
    kernel_boundary=int(kernel_size/2)
    # imgl=np.pad(imgl,kernel_boundary,'constant')
    # print(imgl[4:-4,4:-4 ])
    # imgr=np.pad(imgr,kernel_boundary,'constant')

    
    offset_adjust = 255 / max_disparity
    # imgl=rank_transform(imgl,5)
    # Image.fromarray(np.asarray(imgl)).save('imgl1.jpg')
    # imgr=rank_transform(imgr,5)
    # Image.fromarray(np.asarray(imgr)).save('imgr1.jpg')
    # exit()
    dml=ssd(imgl,imgr,offset_adjust,kernel_boundary,max_disparity,1,0)
    dmr=ssd(imgl,imgr,offset_adjust,kernel_boundary,max_disparity,0,1)
    Image.fromarray(np.asarray(dmr*offset_adjust,np.uint8)).save('disparity_map_r.jpg')
    Image.fromarray(np.asarray(dml*offset_adjust,np.uint8)).save('disparity_map_l.jpg')
    disparity_map=np.zeros(imgl.shape,np.uint8)
    exit()
    for i in range(dml.shape[0]):
        for j in range(dml.shape[1]):
            if abs(dml[i,j]-dml[i,j-dml[i,j]])>6:
                disparity_map[i][j]=np.median(dml[max(0,i-w_boundary):min(dml.shape[0],i+w_boundary),max(0,j-w_boundary):min(dml.shape[1],j+w_boundary)])
    # disparity_map*=offset_adjust
    Image.fromarray(np.asarray(dml*offset_adjust,np.uint8)).save('disparity_map.jpg')
def ssd(imgl,imgr,offset_adjust,kernel_boundary,max_disparity,lmode,rmode):
    disparity_map=np.zeros(imgl.shape,np.uint8)

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
                        if lmode==1:
                            ssd_tmp=int(imgl[x+u,y+v])-int(imgr[x+u,y+v-disparity*lmode])
                        else:
                            ssd_tmp=int(imgl[x+u,y+v+disparity if y+v+disparity<imgl.shape[1] else y+v+disparity- imgl.shape[1]])-int(imgr[x+u,y+v])
                        # ssd+=ssd_tmp*ssd_tmp
                        ssd+=abs(ssd_tmp)
                if ssd<loss:
                    loss=ssd
                    best_disparity=disparity
            disparity_map[x,y]=best_disparity
            # disparity_map[x,y]=best_disparity*offset_adjust
        # exit()
    # color_coef=int(255/(np.max(disparity_map)-np.min(disparity_map)))

    # disparity_map=((disparity_map-np.min(disparity_map))*color_coef)
    # disparity_map=(disparity_map*(255/max_disparity))
    return disparity_map
    if np.max(disparity_map)>255:
        print('exceed 255')
        exit()
    print(disparity_map[0],type(disparity_map))
    Image.fromarray(np.asarray(disparity_map)).save('disparity_map.jpg')

LRC('xid-14489712_1.jpg','xid-14489713_1.jpg',6,20)
# LRC('imgl1.jpg','imgr1.jpg',11,30)

