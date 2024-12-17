import cv2
import numpy as np

def get_dominant_color(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calculate the histogram to find the most common hue
    hist = cv2.calcHist([hsv_image], [0], None, [180], [0, 180])
    dominant_hue = np.argmax(hist)
    
    # Create a color based on the most common hue with full saturation and value
    dominant_color_hsv = np.uint8([[[dominant_hue, 255, 255]]])
    dominant_color_bgr = cv2.cvtColor(dominant_color_hsv, cv2.COLOR_HSV2BGR)[0][0]

    return tuple(int(i) for i in dominant_color_bgr)

# Open a connection to the default camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a single frame
ret, frame = cap.read()

# Release the camera
cap.release()

if not ret:
    print("Error: Can't receive frame. Exiting ...")
    exit()

# Resize frame for processing
frame = cv2.resize(frame, (800, 600))

# Convert to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Use Canny edge detection to find the edges of the buttons
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

button_colors = []

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 10 and h > 10:  # Filter out small contours
        button = frame[y:y+h, x:x+w]
        color = get_dominant_color(button)
        button_colors.append(color)
        # Draw rectangle around each detected button
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

# Display the result
cv2.imshow('TV Remote Buttons', frame)
print("Detected button colors (BGR):", button_colors)

# Press any key to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
