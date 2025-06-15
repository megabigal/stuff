import cv2 as cv
import numpy as np
import os   
import json
import hashlib
from playsound3 import playsound
import random


#img2 = cv.imread("sadmoai.png",cv.IMREAD_COLOR)


imageName = "i.png"
img =  cv.imread("images/"+imageName,cv.IMREAD_COLOR) #image for the photomosaic
imageset = "flower_images" #path for the image set
imagepath = "croppedimagesets/"+ imageset
squaresize = 25 #size of each image in the photomosaic

choice = str(input(" Enter Y for fine detail mode: "))
if choice.upper() == "Y":
    print("yummers")
    choice = True
else:
    print(": (")
    choice = False
cacheChoice = str(input(" Would you like to run the program without checking for a cache(only do if cache exists to save time): "))
if cacheChoice.upper() == "Y":
    print("yummers")
    cacheChoice = True
else:
    print(": (")
    cacheChoice = False

h, w,channels = img.shape
blank= np.zeros((h,w,3), np.uint8) #blank image

if choice:
    cache = imageset+"Dcache.json" #sets up the name for the cache files
    tempCache = imageset+"DtempCache.json"
else:
    cache = imageset+"cache.json" #sets up the name for the cache files
    tempCache = imageset+"tempCache.json"
cacheDirec = "caches/" + cache
tempCacheDirec = "caches/" + tempCache


def hashFile(p): #hashes the file #glitch
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
    
def saveData(p, d):
    p = "caches/" + p
    with open(p, "w") as f:
        json.dump(d,f)
def loadData(p):
    with open(p, "r") as f:
        return json.load(f)
    

 

def getDom(img): #gets dominant colour
    height,width,c = img.shape
    #reshapes the image so its a list of pixels
    data = np.reshape(img, (height * width, c)).astype(np.float32) #float32 required for clustering
    clusters = 5
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0) #termination criteria,iterations,  accuracy
    flags = cv.KMEANS_RANDOM_CENTERS#random initial centers
    _, labels, centers=cv.kmeans(data,clusters,None,criteria,10,flags)
    unique_labels, counts = np.unique(labels, return_counts=True)
    dominant_cluster = unique_labels[np.argmax(counts)]
    
    # Return the center of the dominant cluster
    return centers[dominant_cluster]



colorData = {}

if not cacheChoice:
    for f in os.listdir(imagepath): #sets up the cache, iterates through all the images
        f = os.path.join(imagepath, f)
        img2 =  cv.imread(f,cv.IMREAD_COLOR)
        h0, w0,channels0 = img2.shape
        if choice:
            dic = {}
            ind = 0
            for y in range(0,h0,h0//2):
                for x in range(0,w0,w0//2):
                    ind += 1
                    square = img2[y:y+h0//2, x:x+w0//2]
                    colo= getDom(square)
                    colo = [round(float(c), 2) for c in colo]
                    dic[str(ind)] = colo
            colorData[f] = dic

        else: #no quadrants
            colo = getDom(img2)
            colo = [round(float(c), 2) for c in colo]
            
            colorData[f] = colo

    if not os.path.exists(cacheDirec):

        saveData(cache,colorData)
    else:
        
        saveData(tempCache,colorData)



    try:
        if hashFile(tempCacheDirec) != hashFile(cacheDirec):
            os.replace(tempCacheDirec, cacheDirec)
        else:
            os.remove(tempCacheDirec)
    except:
        pass
doneCheck = True

with open(cacheDirec, "r") as f:
    colorData = json.load(f)


count = 0
#main algo
for y in range(0,h,squaresize): #splits the image into squares
    for x in range(0,w,squaresize):
        count += 1
      
        square = img[y:y+squaresize, x:x+squaresize]
        lowest = float('inf')
        temp = []
        name = ''
        if choice: #IF SPLITTING INTO QUADRANTS
            h1,w1 = square.shape[:2]
           # h1 -= h % 2
           # w1 -= w % 2
           # square = square[:h1, :w1]
            p = []
            for i in colorData:
                p = []
                quadrants = colorData[i]
                ind = 0
                quadarray = []
                for y2 in range(0,h1,h1//2):
                    for x2 in range(0,w1,w1//2):
                        
                        
                        squareQ = square[y2:y2+h1//2, x2:x2+w1//2]
                        quadarray.append(getDom(squareQ))
                for n in quadarray:

                
                
                    ind += 1
                
                    try:
                        colo = np.array(quadrants[str(ind)])
                    except:
                        pass

                
                    p.append(np.sqrt(np.sum((colo - n)**2)))
                        
                p = sum(p)/4
                if p < lowest:
                    lowest = p
                    temp = i
                    name = f


        else: #IF COMPARING FULL IMAGES
            

            color = getDom(square)

            for i in colorData:
                colo = colorData[i]
                
                p = np.sqrt(np.sum((colo - color)**2))
                
                if p < lowest:
                    lowest = p
                    temp = i
                    name = f
                



        print(temp)
        try:
            img2 = cv.imread(temp,cv.IMREAD_COLOR)
            img2 = cv.resize(img2, (squaresize,squaresize),interpolation=cv.INTER_AREA)
            try:
                blank[y:y+squaresize, x:x+squaresize] = img2
            except:
                pass
        except:
            pass
        
            
            




print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
playsound("rah.mp3")
cv.imshow("image", blank)
os.chdir("result") 
nameCounter = 0
while os.path.exists(imageName[:-4]+str(nameCounter)+".png"):
    nameCounter += 1
cv.imwrite(imageName[:-4]+str(nameCounter)+".png", blank)
cv.waitKey(0)
cv.destroyAllWindows()

