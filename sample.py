import cv2
import numpy as np

# Define the chessboard size (number of inner corners per chessboard row and column)
chessboard_size = (7, 7)  # Update this to match the inner corners of the chessboard

# Open the camera feed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from the camera.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    found, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if found:
        # Create a 2D array to represent the chessboard
        chessboard_array = np.zeros((chessboard_size[1] + 1, chessboard_size[0] + 1), dtype=int)

        # Process squares and determine if they are black or white
        for i in range(chessboard_size[1] + 1):
            for j in range(chessboard_size[0] + 1):
                # Determine if the square is white (1) or black (0)
                chessboard_array[i, j] = (i + j) % 2

        print("Chessboard array (1 = White, 0 = Black):")
        print(chessboard_array)
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
