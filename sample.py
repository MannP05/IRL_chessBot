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

# Define HSV ranges for multiple colors
color_ranges = {
    'blue': (np.array([100, 150, 50]), np.array([130, 255, 255])),
    'red': (np.array([0, 120, 70]), np.array([10, 255, 255])),
    'green': (np.array([35, 100, 50]), np.array([85, 255, 255])),
    'yellow': (np.array([25, 150, 50]), np.array([35, 255, 255]))
}

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Can't receive frame. Exiting ...")
            break

        # Resize frame for processing
        frame = cv2.resize(frame, (800, 600))

        # Define the region of interest (ROI) around the controller
        roi_x, roi_y, roi_w, roi_h = 200, 100, 400, 400
        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Convert the ROI to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Use Canny edge detection to find the edges of the buttons
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_colors = {color: False for color in color_ranges}

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 10 and h > 10:  # Filter out small contours
                button = roi[y:y+h, x:x+w]
                color = get_dominant_color(button)
                # Convert the BGR color to HSV to check for multiple colors
                hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)[0][0]
                for color_name, (lower, upper) in color_ranges.items():
                    if lower[0] <= hsv_color[0] <= upper[0]:
                        detected_colors[color_name] = True
                        # Draw rectangle around detected button
                        cv2.rectangle(roi, (x, y), (x + w, y + h), color, 2)

        # Place the ROI back in the frame
        frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w] = roi

        # Display the result
        cv2.imshow('TV Remote Buttons', frame)

        for color_name, detected in detected_colors.items():
            if detected:
                print(f"{color_name.capitalize()} button detected!")
            else:
                print(f"No {color_name} button detected.")

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the camera and close windows
    cap.release()
    cv2.destroyAllWindows()
