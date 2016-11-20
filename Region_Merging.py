from cv2 import *
import numpy as np
from scipy import signal
import math



def crack_img(img):
    shape=(len(img)*2,len(img[0])*2)
    crack=np.zeros(shape)
    for i in range(len(img)):
        for j in range(len(img[0])):
            crack[i*2][j*2]=img[i][j]

    for i in range(0,len(crack)):
        for j in range(0,len(crack[0])):
            if i%2==0 and j%2==0:
                crack[i][j-1]=abs(crack[i][j]-crack[i][j-2])
                crack[i-1][j]=abs(crack[i][j]-crack[i-2][j])
    return crack
            

def segment(img):
    T1=30
    crack=img
    for i in range(0,len(crack)):
        for j in range(0,len(crack[0])):
            if i%2==0 and j%2==0:
                if(crack[i][j-1]<T1):
                    crack[i][j-1]=0
                else:
                    crack[i][j-1]=255
                if(crack[i-1][j]<T1):
                    crack[i-1][j]=0
                else:
                    crack[i-1][j]=255


    
    return crack



def regions_segment(crack,regions):
    for k in range(30):

        for i in range(len(regions)-1):
            for j in range(len(regions[0])-1):
                if regions[i][j]!=regions[i][j+1]:
                    if(crack[i*2][j*2+1]==0):
                        regions[i][j+1]=regions[i][j]
                if regions[i][j]!=regions[i+1][j]:
                    if(crack[i*2+1][j*2]==0):
                        regions[i+1][j]=regions[i][j]
                        

        
    x=float(255.0/np.amax(regions))

##UNCOMMENT FOR WEAKER CRITERION- Approximately 2 minutes
##    T3=20
##    peri={}
##    peri[0]={}
##    for i in range(len(regions)-1):
##        for j in range(len(regions[0])-1):
##            if(regions[i][j]!=regions[i][j+1]):
##                if regions[i][j] not in peri.keys():
##                    peri[regions[i][j]]={}
##                peri[regions[i][j]][i]=j
##    for i in peri.keys():
##        z=0;
##        temp=0
##        count=0
##        region=0
##        for j in peri[i].keys():
##            region=i
##            if z==0:
##                z=1
##                temp=regions[j][peri[i][j]+1]
##            if regions[j][peri[i][j]+1]==temp: #or regions[j+1][peri[i][j]]==temp:
##                count+=1
##        if count<T3:
##            for k in range(len(regions)):
##                for l in range(len(regions[0])):
##                    if(regions[k][l]==temp):
##                        regions[k][l]=region

    regions=regions*x
    return regions



img=imread("MixedVegetables.jpg",0)
shape=(len(img)*2,len(img[0])*2)

crack=np.zeros(shape)

crack=crack_img(img)

crack=crack.astype("uint8")

imshow("Original Image",img)
imshow("Crack Edges",crack)

crack=segment(crack)

imshow("Crack Edges with weaker edges removed",crack)

count=0;
regions=np.zeros(img.shape)
for i in range(len(img)):
    for j in range(len(img[0])):
        regions[i][j]=count
        count=count+1

regions=regions_segment(crack,regions)

regions=regions.astype("uint8")
imshow("Segmented Regions",regions)

waitKey(0)
destroyAllWindows() 
