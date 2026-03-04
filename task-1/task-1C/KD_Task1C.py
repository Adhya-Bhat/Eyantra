# Libraries used
import cv2 #this is the opencv library used for computer vision and image processing 
import numpy as np #this is the numpy library which is used to handle arrays (consider images as large number grids)
import argparse #this library is used to take input from the command line as that was how the files were said to be provided in the automatic task checking system in eyantra competition

# Function : white_pixel_count : this function counts the number of white pixels in an image after converting it to grayscale
def white_pixel_count(img):    
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #converting the image to grayscale (i.e., colour is removed and only the brightness aspect is left)
  _, bImg = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY) #if the brightness of the pixel is > 150 then it turns white(255) else turns black (0).
  pCnt = cv2.countNonZero(bImg) #non zero means white as we saw in the previous line and so counting all the non zero pixels
  return pCnt

# Function : green_pixel_count : Used to count the number of green pixels
def green_pixel_count(img):
  img = img[:,1:,] # we know that the image is in the form of BGR so here we are extracting only the green elements
  ret, img = cv2.threshold(img, 70,255,cv2.THRESH_BINARY)    #  

  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #HSV: hue,saturation,value this is a better option for detecting colours.
  lower_green = np.array([35, 100, 100])  # lower bound for green
  upper_green = np.array([85, 255, 255])  # upper bound for green
# All the pixels whose brightness lies between these two bounds are to be considered as green
# All the bounds or ranges in this program has been taken first from other standard programs / example programs and then altered by trial and error according to the task sample image.
  # Create a mask for green pixels
  mask = cv2.inRange(hsv, lower_green, upper_green) # creating a mask i.e., making the green pixels white and everything else black

  # Count the number of green pixels
  return cv2.countNonZero(mask) # Again like the white pixel count... we are counting the number of non zero pixels.
        
def main():

  #extra code for command line arguments --image or -i, this is following the specified format given in the task description
  parser = argparse.ArgumentParser(description="e-yantra task1")
  parser.add_argument("-i", "--image",type=str, help="Specify image file to process")

  args = parser.parse_args()
  
  if not args.image:
    parser.print_help()
    exit(1)
  else:
    img = cv2.imread(args.image)        
    if img is None:
      print(f"Error: Could not load image from {args.image}.")
      exit(1)
  #command line arguments code ends here
  
  rows,cols = img.shape[:2] # Getting the image size..
  
  dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100) #Using the predefined dictionary of the aruco markers. Again this was chosen by trial and error as I couldnt figure out which dictionary the given sample aruco marker belonged to even by using google lens.
  corn, ids, _ = cv2.aruco.detectMarkers(img, dict) #corn short for corners and ids are the marker ids
  
  detected_markers = {}
  oldC = [(0,0),(0,0),(0,0),(0,0)] #old centroids
  maxX = maxY = 0 #this is how we find max and minimum in general for max we take the minimum possible value and keep comparing and storing the max between two values and vice versa for minimum
  minX, minY = rows,cols
  m_id = 101 
  if ids is not None:
    if len(ids) != 4: #As the four corners need an aruco marker each and if not detected then wrong
      print (f"Error: {len(ids)} aruco markers found")
      exit(1)
      
    for i in range(len(ids)):
      M = cv2.moments(corn[i][0])
      if M["m00"] != 0: #finding the centroid
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # finding the positions of the aruco markers (imagine a rectangle)
        if cX > maxX : maxX = cX
        if cY > maxY : maxY = cY
        if cX < minX : minX = cX
        if cY < minY : minY = cY
        if ids[i]<m_id : m_id = int(ids[i])
        
        marker_info = {
          'Id'      : ids[i],
          'Centroid': (cX, cY),
          'Corners' : corn[i][0]
        }
        
        #original aruco marker centroids
        oldC[i]=(cX,cY)
        detected_markers[ids[i][0]] = marker_info

    with open("output.txt","w") as file:
      print("Detected marker IDs:",list(detected_markers.keys()),file=file)
      print("",file=file)

    #Perspective Transform Original Centroids to Transform Centroids    
    newC = [(minX,minY),(maxX,minY),(minX,maxY),(maxX,maxY)]
    cenX = int((oldC[0][0] + oldC[1][0] + oldC[2][0] + oldC[3][0])/4)
    cenY = int((oldC[0][1] + oldC[1][1] + oldC[2][1] + oldC[3][1])/4)
    for i in range(4):
      if oldC[i][0] < cenX and oldC[i][1] < cenY:
        newC[i]=(minX,minY)
      elif oldC[i][0] < cenX and oldC[i][1] > cenY:
        newC[i]=(minX,maxY)
      elif oldC[i][0] > cenX and oldC[i][1] < cenY:
        newC[i]=(maxX,minY)
      elif oldC[i][0] > cenX and oldC[i][1] > cenY:
        newC[i]=(maxX,maxY)

    j=0
    for i in list(detected_markers.keys()):
      detected_markers[i]['Centroid'] = newC[j]
      j+=1
              
    pts1 = np.float32(oldC)
    pts2 = np.float32(newC)
    trn = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,trn,(rows,cols))
    dst = dst[minY:maxY,minX:maxX]
            
    #rotate image based on marker id: basically trying to get the least numbered aruco marker on the left top corner and so on...as given in the sample image
    tmp = dst.copy()
    dMark = detected_markers[m_id]['Centroid']
    if dMark[0] == maxX:
      if dMark[1] == maxY:
        tmp = cv2.rotate(tmp, cv2.ROTATE_90_COUNTERCLOCKWISE)
      tmp = cv2.rotate(tmp, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
      if dMark[1] == maxY:
        tmp = cv2.rotate(tmp, cv2.ROTATE_90_CLOCKWISE)

    height, width = tmp.shape[:2]
    roi = tmp[int(height/2):height,0:width] #extracting the ROI cutting only the bottom half

    #After perspective transformation, the farm region may still be incorrectly oriented (rotated 90°, 180°, etc.). Since plant
    #detection depends on correct alignment, we verify the orientation
    #using white pixel density.
    #We check if the current ROI contains at least 25% white pixels.
    #To determine correct orientation, we test 4 possible halves:
    #    1. Top half
    #    2. Bottom half
    #    3. Left half
    #   4. Right half
    #For each half:
    #   Extract the region
    #   Count white pixels
    #   Keep the region with the highest white pixel count

    #Assumption:
    #   The correctly oriented farm image will contain the
    #   largest visible white background region.
    #Depending on which half has the maximum white pixels:

    # If top half → rotate 180°
    # If bottom half → keep as is
    # If left half → rotate 90° counterclockwise
    # If right half → rotate 90° clockwise

    #So that finally we have the ROI in the bottom half
    #After selecting correct orientation, we crop margins to remove distortion and unwanted edges again this is through trial and error.
    # Remove 10% from top and bottom Remove 8% from left and right
    # This keeps only the central farm region.
    #Another 10% is removed from top and bottom to ensure only plant rows remain for analysis.

    if (white_pixel_count(roi) < (height*width*.25)):
      #divide width into 2 for block 1 and block 2
      #divide height into 3 equal parts (remove unwanted 60% above and 12% below image)
      #if number of green pixel less means infected plant, 
      #   further divide into two parts if green_pixels almost nill,block row 1 else add 3 to plant code
      
      maxC = 0
      roi = None
      for i in range(2):
        height, width = dst.shape[:2]
        tmp = dst[int(i*height/2):int(height*((i+1)/2)),0:width]      
        pCnt = white_pixel_count(tmp)
        if pCnt > maxC:
          maxC = pCnt
          height, width = tmp.shape[:2]
          if (i==0):
            roi = cv2.rotate(tmp,cv2.ROTATE_90_COUNTERCLOCKWISE)
            roi = cv2.rotate(roi,cv2.ROTATE_90_COUNTERCLOCKWISE)
          else:
            roi = tmp.copy()
        
        height, width = dst.shape[:2]  
        tmp = dst[0:height,int(i*width/2):int(width*((1+i)/2))]
        pCnt = white_pixel_count(tmp)
        if pCnt > maxC:
          maxC = pCnt
          height, width = tmp.shape[:2]
          rt = cv2.ROTATE_90_CLOCKWISE if (i==1) else cv2.ROTATE_90_COUNTERCLOCKWISE
          roi = cv2.rotate(tmp,rt)
    
      height, width = roi.shape[:2]

    height,width = roi.shape[:2]
    roi = roi[int(height*.10):int(height*.90),int(width*.08):int(width*0.92)]

    height,width = roi.shape[:2]
    dst = roi[int(height*.10):int(height*.90),0:width] 
    pCode = ['A','B','C','D','E','F']   
    #dividing the image into 2 vertical blocks each block has 3 plants 
    for j in range(2):        
      height, width = dst.shape[:2]
         
      dst2 = dst.copy()
      dst2 = dst[0:height, int(j*width/2):int(width*(j+1)/2)]  
      height, width = dst2.shape[:2]
      #each block has 3 plants  and if the green area is less than 10% the plant is infected, then assigning the plant codes 
      for i in range(3): 
        height, width = dst2.shape[:2]
        tmp = dst2[int(height*i*.32):int(height*(i+1)*.32), 0:width]
        pCnt = green_pixel_count(tmp)
        height, width = tmp.shape[:2]
        if(pCnt < height*width*.10):
          height, width = dst2.shape[:2]
          pcnt = green_pixel_count(dst2[int(height*i*.32):int(height*(i+1)*.32), 0:int(width/2)])
          plant = pCode[i] if pcnt < 875 else pCode[i+3]
          
          #writing the output file
          with open("output.txt","a") as file:
            print("Infected plant in Block",str(j+1) + ": P" + str(j+1) +plant,file=file)
  else:
    print ("Error: No aruco markers found")
    exit(1)
      
if __name__ == "__main__":
  main()
