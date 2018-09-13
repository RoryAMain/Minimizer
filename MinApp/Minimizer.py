import cv2
import numpy as np
from matplotlib import pyplot as plt

class Minimizer:

	def __init__(self,imageIn,sampleCountWidthIn,sampleCountHeightIn,sampleSizeIn):
		self.img = cv2.imread(imageIn,1)
		self.imageHeight = self.img.shape[0]
		self.imageWidth = self.img.shape[1]
		
		self.desiredSampleCountWidth = sampleCountWidthIn
		self.desiredSampleCountHeight = sampleCountHeightIn

		self.sampleSize = sampleSizeIn

		self.spacing = 0

		if(self.imageHeight < self.imageWidth):
			self.spacing = int(self.imageHeight/self.desiredSampleCountHeight) - self.sampleSize
		else:
			self.spacing = int(self.imageWidth/self.desiredSampleCountWidth) - self.sampleSize

		self.sampleCountWidth = int(self.imageWidth/(self.spacing + self.sampleSize))
		self.sampleCountHeight = int(self.imageHeight/(self.spacing + self.sampleSize))

	def printInfo(self):
		print("Minimizer Object Info")
		print("Shape: " + str(self.img.shape))
		print("Number of Samples: " + str(self.sampleCountHeight) + " x " + str(self.sampleCountWidth))
		print("Spacing: " + str(self.spacing))
		print("Sample Size: " + str(self.sampleSize))

	def outlineSamples(self):
		topLeftX = 0
		topLeftY = 0
		bottomRightX = self.sampleSize
		bottomRightY = self.sampleSize

		for y in range(0,self.sampleCountHeight):
			for x in range(0,self.sampleCountWidth):
				img = cv2.rectangle(self.img,(topLeftX,topLeftY),(bottomRightX,bottomRightY),(0,255,0),3)
				topLeftX += self.sampleSize + self.spacing
				bottomRightX += self.sampleSize + self.spacing
			topLeftY += self.sampleSize + self.spacing
			bottomRightY += self.sampleSize + self.spacing
			topLeftX = 0
			bottomRightX = self.sampleSize

	def displayImage(self):
		cv2.imshow('image',self.img)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def cutSamples(self):
		xCounter = 0
		yCounter = 0

		newImage = self.createBlankCopy()

		for y in range(0,self.sampleCountHeight):
			for x in range(0,self.sampleCountWidth):
				sample = self.img[((yCounter*self.sampleSize) + (yCounter*self.spacing)):(((yCounter+1) * self.sampleSize) + (yCounter*self.spacing)), ((xCounter*self.sampleSize) + (xCounter*self.spacing)):(((xCounter+1) * self.sampleSize) + (xCounter*self.spacing))]
				newImage[(yCounter*self.sampleSize):((yCounter+1)*self.sampleSize),(xCounter*self.sampleSize):((xCounter+1)*self.sampleSize)] = sample
				xCounter = xCounter + 1

			yCounter = yCounter + 1
			xCounter = 0

		croppedImage = newImage[0:((self.sampleCountHeight)*self.sampleSize),0:((self.sampleCountWidth)*self.sampleSize)]
		return croppedImage

	def create_blank(self,width, height, rgb_color=(0, 0, 0)):
	    """Create new image(numpy array) filled with certain color in RGB"""
	    # Create black blank image
	    image = np.zeros((height, width, 3), np.uint8)

	    # Since OpenCV uses BGR, convert the color first
	    color = tuple(reversed(rgb_color))
	    # Fill image with color
	    image[:] = color

	    return image

	def createBlankCopy(self):
		white = (255,255,255)
		image = self.create_blank(self.imageWidth,self.imageHeight,rgb_color=white)
		return image

	def saveTo(self,urlIn,imageIn):
		cv2.imwrite(urlIn,imageIn)

	def minimizeAndSave(self,urlIn):
		newImage = self.cutSamples()
		self.saveTo(urlIn,newImage)


#imageLink = input("Enter image name: ")
#sampleCountIn = input("Enter number of samples: ")
#sampleSizeIn = input("Enter size of samples: ")

#minTest = Minimizer(imageLink,int(sampleCountIn),int(sampleCountIn),int(sampleSizeIn))
#minTest = Minimizer("D:\\Users\\ramai\\Documents\\Programming\\StupidStuff\\DjangoMinimizer\\Minimizer\\media\\Protect.jpg",20,20,5)
#minTest.printInfo()
#newImage = minTest.cutSamples()
#cv2.imwrite('Minimized' + imageLink ,newImage)
#minTest.minimizeAndSave("D:\\Users\\ramai\\Documents\\Programming\\StupidStuff\\DjangoMinimizer\\Minimizer\\media\\","Protect.jpg")