import cv2
import numpy as np

chessboard_size = (7, 7) 
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from the camera.")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if found:
        chessboard_array = np.zeros((chessboard_size[1] + 1, chessboard_size[0] + 1), dtype=int)
        for i in range(chessboard_size[1] + 1):
            for j in range(chessboard_size[0] + 1):
                chessboard_array[i, j] = (i + j) % 2

        print("Chessboard array (1 = White, 0 = Black):")
        print(chessboard_array)
        break
    
cap.release()
cv2.destroyAllWindows()
