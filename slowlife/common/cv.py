import cv2
import pyautogui

# Load the image to be matched
image = cv2.imread('../../resources/mainmenu/home.png')

# Load the screenshot
screenshot = cv2.imread('../../log/test.png')

# Convert the image and screenshot to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Find the template in the screenshot
result = cv2.matchTemplate(gray_screenshot, gray_image, cv2.TM_CCOEFF_NORMED)

# Get the minimum and maximum values
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# If the match is good enough, draw a rectangle around the template
if max_val > 0.5:
    top_left = max_loc # Tuple of width, height
    bottom_right = (top_left[0] + image.shape[1], top_left[1] + image.shape[0])
    # cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

    anchor_left = (top_left[0], int(top_left[1] - 6 * image.shape[1]))
    anchor_right = (top_left[0]+ image.shape[1], int(top_left[1]  - 5 * image.shape[1]))
    cv2.rectangle(screenshot, anchor_left, anchor_right, (0, 0, 255), 2)

# Display the screenshot
cv2.imshow('Screenshot', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()
exit()
