import cv2
import numpy
img = cv2.imread("bigdan.jfif", cv2.IMREAD_COLOR)
shape = img.shape
height,width = img.shape[:2]
custom = input("custom for custom size, blank to allow resizing, anything else to leave at normal size: ")
stretch = input("would you like to stretch the image? leave blank for no: ")
if custom == "custom":
    width = int(input("enter width: "))
    height = int(input("enter height"))
    img = cv2.resize(img,   (width, height))
if not custom and not stretch and width > 571:
    scale = 571 / width
    img = cv2.resize(img, (int(width*scale), int(height * scale)))
if not custom and stretch and width > 191:
    print("7")
    scale = 191 / width
    img = cv2.resize(img, (int(width*scale), int(height * scale)))

print(width)
brightnessMatrix = numpy.empty((img.shape[0], img.shape[1]), dtype=object) 

#list of ascii things
#.:-=+*#%@ 
#`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$
#@$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'. 
# .oO@ 
# .·´¨°oOØ♢♖♜♛♠█ 
# ░▒▓█ 

invert = True #inverts colors

asciiMatrix =  "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
asciiMap = {}
brightnessRange = 256
mapRange = brightnessRange / len(asciiMatrix)
#mapMod = brightnessRange % len(asciiMatrix)
for i in range(brightnessRange+1):
    index = min(int(i // mapRange), len(asciiMatrix) - 1)  # cap index safely
    asciiMap[i] = asciiMatrix[index]

#for x, y in asciiMap.items():
 # print(x, y)


def sRGBtoLin(colour):
    #takes a decimal srgb gamma encoded color value between 1 and 0and then linerizes it
    if colour <= 0.04045:
        return colour/12.92
    else:
        return pow((colour + 00.055)/1.055  ,2.4)

def calculateBrightness(rgb, method): # i have been informed that opencv is bgr not rgb whoopsy
    if method == 1: #averages
        
        return numpy.mean(rgb)
    if method == 2: #averages the max and the min
        rgb = rgb.astype(numpy.uint16) #originally an 8 bit integer, gotta change that so it doesnt overflow
        return (numpy.max(rgb) + numpy.min(rgb)) / 2
    if method == 3: #random luminance shit i found off stackoverflow
        rgb = rgb.astype(numpy.uint16)
        return (0.299 *(rgb[2]**2) + 0.587*(rgb[1]**2) + 0.114*(rgb[0]**2)) **0.5
    if method == 4: #percieved lightness
        vb = rgb[0] / 255
        vr = rgb[2] /255
        vg = rgb[1] / 255
        Y = (0.2126 * sRGBtoLin(vr) + 0.7152 * sRGBtoLin(vg) + 0.0722 * sRGBtoLin(vb))
        if Y <= (216/24389):
            LSTAR = Y*(24389/27)
        else:
            LSTAR = pow(Y,(1/3)) * 116 - 16
        return int((LSTAR/100)*255)
            



for y in range(len(img)):
    for x in range(len(img[y])):
        brightness =  int(calculateBrightness(img[y,x], 3)) #change last parameter to alter the method for calculating brightness
        if invert:
            
            brightness = 256-brightness
        brightnessMatrix[y,x] =asciiMap[brightness]

      #  print(img[y,x])

f = open("output.txt", "w",encoding="utf-8")
for x in brightnessMatrix:
    if stretch:
        s = "".join([str(i)*3 for i in x.astype(str)])
    else:
        s = "".join([i for i in x.astype(str)])
    s = str(s)
    f.write(s+"\n")
  #  print(s[:571])
    
    

cv2.waitKey(0)



    

