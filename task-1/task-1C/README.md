Task 1C – ArUco Based Perspective Correction and Plant Infection Detection
Overview
This task was completed as part of the simulation round of the e-Yantra Krishi Drone theme.
The objective of Task 1C was to:
Detect four ArUco markers placed around a farm image
Perform perspective transformation to obtain a top-down view
Correct image orientation automatically
Extract the farm region of interest
Divide the farm into plant sections
Detect infected plants based on green pixel density
Print the output in the required format
This entire pipeline is automated and works through command-line input as required in the task.
Approach and Implementation
1. ArUco Marker Detection
I used OpenCV’s predefined DICT_4X4_100 dictionary to detect the markers.
After detection:
I extracted the marker corners
Computed centroids using image moments
Identified the four extreme points
Used those to define the transformation region
If fewer than four markers are detected, the program exits to prevent incorrect transformation.
2. Perspective Transformation
Using the detected centroids:
I defined destination coordinates forming a rectangle
Used cv2.getPerspectiveTransform
Applied cv2.warpPerspective
This produces a top-down aligned farm image.
However, after perspective correction, the image orientation was not always consistent, which led to the next step.
3. Orientation Correction
Even after warping, the farm image could be rotated.
To fix this, I implemented a white pixel density heuristic:
Converted the image to grayscale
Applied thresholding
Checked white pixel count in different halves (top, bottom, left, right)
Rotated the image depending on which region had the highest white density
The assumption here is that the correct orientation will show the largest white background region in the expected location.
This approach worked consistently across simulation test cases.
4. ROI Cropping
After orientation correction:
I removed a fixed percentage from all sides to eliminate unwanted borders
Further cropped the region to isolate the plant rows
These cropping values were finalized after testing on multiple sample images.
5. Plant Division
The farm layout follows:
2 vertical blocks
Each block contains 3 plants
Total = 6 plant regions
Each plant section was extracted independently for analysis.
6. Infection Detection Logic
For each plant region:
Converted the image to HSV
Applied a green mask using tuned HSV thresholds
Counted green pixels
If the green pixel percentage was below 10% of the plant region, the plant was marked as infected.
HSV was chosen instead of BGR because it provides more stable color segmentation under varying brightness conditions.
Challenges Faced
Identifying the correct ArUco dictionary initially required experimentation.
Orientation correction after perspective transform was not straightforward.
Green threshold tuning required multiple trials.
Cropping margins had to be adjusted carefully to avoid losing plant data.
Since this was part of the simulation round, all validation was done using the provided test images and command-line evaluation system.
Assumptions
Exactly four ArUco markers are present.
The farm layout is fixed (2 blocks × 3 plants).
White background can be used reliably for orientation detection.
Green density is a valid indicator of plant health.
Key Learnings
Through this task, I gained hands-on experience with:
ArUco marker detection
Perspective geometry
Image warping and coordinate mapping
HSV-based color segmentation
Designing heuristics for image alignment
This task strengthened my understanding of building a complete computer vision pipeline rather than solving isolated image processing steps.
Conclusion
The final implementation successfully performs:
Marker detection → Perspective correction → Orientation alignment → ROI extraction → Plant segmentation → Infection detection → Structured output
The solution works fully through command-line input and follows the required task format.
