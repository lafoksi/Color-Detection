import requests
import cv2
import numpy as np
import imutils

url = "http://192.168.0.177:8080/shot.jpg"

# Function to detect colors in an image
def detect_colors(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for detection (you can modify these ranges based on your requirements)
    color_ranges = {
        'red': ([0, 50, 50], [10, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'green': ([36, 25, 25], [70, 255, 255]),
        'blue': ([90, 50, 50], [120, 255, 255]),
    }

    # Detect colors in the image
    detected_colors = []
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            detected_colors.append(color)

    return detected_colors

# While loop to continuously fetch data from the URL
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)

    # Detect colors in the image
    detected_colors = detect_colors(img)

    # Display the image
    cv2.imshow("Phone Cam", img)

    # Display the detected colors
    print("Detected colors:", detected_colors)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
