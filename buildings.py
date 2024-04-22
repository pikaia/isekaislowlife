import logging.handlers
import os
import sys
import time

from tkinter import *
import pyautogui
import pygetwindow

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.DEBUG)
h.setFormatter(formatter)
log.addHandler(h)

APP_TITLE = 'BlueStacks App Player'

buildings = ['inn', 'apothecary', 'workshop', 'scroll shop', 'spring resort', 'central station',
             'patisserie', 'archery range', 'clinic', 'market street', 'bank', 'tailor shop',
             'sports park', 'museum']


def highlightSection(title, rect, color='red', duration=3):
    win = Tk()
    win.title = title
    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/geometry.html
    # A geometry string has this general form: 'wxh±x±y'
    # where:
    # The w and h parts give the window width and height in pixels. They are separated by the character 'x'.
    # If the next part has the form +x, it specifies that the left side of the window should be x pixels
    # from the left side of the desktop. If it has the form -x, the right side of the window is x pixels
    # from the right side of the desktop.
    geometry = str(rect[2]) + 'x' + str(rect[3]) + '+' + str(rect[0]) + '+' + str(rect[1])
    win.geometry(geometry)
    log.debug(f'title={title}, str = {geometry}')
    win.configure(background=color)
    win.overrideredirect(1)
    win.attributes('-alpha', 0.3)
    win.wm_attributes('-topmost', 1)
    win.after(duration * 1000, lambda: win.destroy())
    win.mainloop()


def click_image(image, grayscale=True, confidence=0.5):
    location = None

    while location is None:
        try:
            log.debug('Looking for ' + image)
            # pyautogui.locateOnScreen(image, 1, grayscale=grayscale, confidence=confidence)
            #  location = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=grayscale, confidence=0.4)
            location = pyautogui.locateOnScreen(image, 1, grayscale=grayscale, confidence=confidence)
            # highlight(x=location.left, y=location.top, width=location.width, height=location.height)
            highlightSection(os.path.basename(image), location)
            pyautogui.click(int(location.left + location.width / 2), int(location.top + location.height / 2))
            log.info(
                f'Click ({int(location.left + location.width / 2)}, {int(location.top + location.height / 2)}) {image}')
        except Exception as e:
            time.sleep(1)
            log.debug(repr(e))

    log.debug('Found ' + image + ' at:' + repr(location))


# Get the coordinates of the window
app = pygetwindow.getWindowsWithTitle(APP_TITLE)[0]

# Whole app window
screenshot = pyautogui.screenshot(region=(app.left, app.top, app.right - app.left,
                                          app.bottom - app.top), imageFilename='resources/ss/data/full_app.png')

# Minus caption on top and bottom
mini_region = (app.left, app.top + 60, app.right - app.left,
               app.bottom - app.top - 70 - 60)
mini_screenshot = pyautogui.screenshot(region=mini_region,
                                       imageFilename='resources/ss/data/mini_app.png')

# Assume we start with Inn having focus.
earnings = None
location = None
for bldg in buildings:
    # Display earnings breakout
    if earnings is None:
        earnings = pyautogui.locateOnScreen('resources/ss/data/buildings/earnings.png', 1, grayscale=True, confidence=0.7)
    pyautogui.click(earnings)
    # wait for screen to appear
    time.sleep(3)
    # Save each building in resources/ss/data/buildings
    pyautogui.screenshot(region=mini_region, imageFilename=f'resources/ss/data/buildings/{bldg}.png'.replace(' ', '_'))
    # Dismiss screen
    pyautogui.click(app.right - 10, app.bottom - app.top - 70 - 60 - 10)
    # Click on arrow to go to next building
    if location is None:
        location = pyautogui.locateOnScreen('resources/ss/data/buildings/next_building.png', 1, grayscale=True, confidence=0.7)
    pyautogui.click(location)
    time.sleep(1)
