# Python programe to illustrate  
# arithmetic operation of 
# addition of two images 
    
# organizing imports  
import cv2  
import numpy as np  
import os

# path to input images are specified and   
# images are loaded with imread command  
image1 = cv2.imread('input1.jpg')  
image2 = cv2.imread('input2.jpg') 
directory = "img" 
# cv2.addWeighted is applied over the 
# image inputs with applied parameters 
weightedSum = cv2.addWeighted(image1, 0.5, image2, 0.4, 0) 

#os.chdir(directory) 
  
# List files and directories   
# in 'C:/Users/Rajnish/Desktop/GeeksforGeeks'   
print("Before saving image:")   
print(os.listdir(directory))   
  
# Filename 
filename = 'img/input1input2.jpg'
  
# Using cv2.imwrite() method 
# Saving the image 
cv2.imwrite(filename, weightedSum) 
  
# List files and directories   
# in 'C:/Users / Rajnish / Desktop / GeeksforGeeks'   
print("After saving image:")    
print(os.listdir(directory))   
print('Successfully saved') 
