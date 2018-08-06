import pytesseract
from PIL import Image
import cv2
import os
import glob
import pandas as pd

storenum = '1954'
list = []
os.chdir(storenum)
for filename in glob.glob(storenum + "*.png"):
    print(filename)
    # load the example image and convert it to grayscale
    image = cv2.imread( filename)
    size = image.shape

    numNames = int(size[0]/16)
    print(numNames)
    for i in range(numNames):
    	tl = int((i)*16) + 2
    	bl = int((i+1)*16)
    	tempImage = image[tl:bl, 6:size[1]-6]
    	color = image[6,size[1]-2]
    	tempImage = cv2.resize(tempImage, (0,0), fx=3, fy=2.5)
    	# tempImage[np.where((tempImage == color).all(axis = 2))] = [225,255,255]
    	gray = cv2.cvtColor(tempImage, cv2.COLOR_BGR2GRAY)

    	# check to see if we should apply thresholding to preprocess the
    	# image
    	gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    	# write the grayscale image to disk as a temporary file so we can
    	# apply OCR to it
    	filename = "{}.png".format(os.getpid())
    	cv2.imwrite(filename, gray)

    	# load the image as a PIL/Pillow image, apply OCR, and then delete
    	# the temporary file
    	text = pytesseract.image_to_string(Image.open(filename)).encode('ascii', 'ignore').decode()
    	os.remove(filename)
    	list.append(text)

filename = 'SM_' + storenum + '.csv'
os.chdir('..\\')
df = pd.DataFrame(list)
df.columns = ['street']
print(df)
df.to_csv(filename, index = False)
