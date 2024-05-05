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
TAKE_SNAPSHOT = False

def highlightSection(title, rect, color='red', duration=3):
    if not TAKE_SNAPSHOT:
        return
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
            if TAKE_SNAPSHOT:
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

# Assume we start with first family member displayed.
blessing = None
advanced_blessing = None
fellow_blessing = None
cancel = None
next_member = None
for x in range(0, 39):
    # Display blessing screen
    if blessing is None:
        blessing = pyautogui.locateOnWindow('resources/ss/data/family/blessing_available.png', APP_TITLE, grayscale=True, confidence=0.7)
    pyautogui.click(blessing)

    # Click on advanced. If there is no blessing it will display warning.
    image = 'resources/ss/data/family/advanced_blessing.png'
    if advanced_blessing is None:
        advanced_blessing = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=True, confidence=0.4)
        # pyautogui.locateOnScreen('resources/ss/data/family/advanced_blessing.png', 1, grayscale=True, confidence=0.7)
    log.info(f'Click ({int(advanced_blessing.left + advanced_blessing.width / 2)}, {int(advanced_blessing.top + advanced_blessing.height / 2)}) {image}')
    highlightSection(os.path.basename(image), advanced_blessing)
    pyautogui.click(advanced_blessing)
    time.sleep(1)
    # If there is no blessing it will display warning. Dismiss any waring
    pyautogui.click(blessing)

    # Click on fellow blessing in case we have both blessings.
    image = 'resources/ss/data/family/fellow_blessing.png'
    if fellow_blessing is None:
        fellow_blessing = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=True, confidence=0.7)
    log.info(f'Click ({int(fellow_blessing.left + fellow_blessing.width / 2)}, {int(fellow_blessing.top + fellow_blessing.height / 2)}) {image}')
    highlightSection(os.path.basename(image), fellow_blessing)
    pyautogui.click(fellow_blessing)
    # If there is no blessing it will display warning. Dismiss any waring
    time.sleep(1)
    pyautogui.click(blessing)

    # Display blessing screen
    image = 'resources/ss/data/family/cancel.png'
    if cancel is None:
        cancel = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=True, confidence=0.7)
    time.sleep(1)
    highlightSection(os.path.basename(image), cancel)
    log.info(f'Click ({int(cancel.left + cancel.width / 2)}, {int(cancel.top + cancel.height / 2)}) {image}')
    pyautogui.click(cancel)

    # wait for screen to appear
    time.sleep(1)
    # Save each buildings in resources/ss/data/buildings
    log.info(f'Take screenshot family_member{x}.png')
    if TAKE_SNAPSHOT:
        pyautogui.screenshot(region=mini_region, imageFilename=f'resources/ss/data/generated/family/family_member{x}.png'.replace(' ', '_'))

    # go to next member. Confidence max was 0.548
    image = 'resources/ss/data/family/next_family_member.png'
    if next_member is None:
        next_member = pyautogui.locateOnWindow('resources/ss/data/family/next_family_member.png', APP_TITLE, grayscale=True, confidence=0.5)
        highlightSection(os.path.basename('resources/ss/data/family/next_family_member.png'), next_member)
    time.sleep(1)
    highlightSection(os.path.basename(image), next_member)
    log.info(f'Click ({int(next_member.left + next_member.width / 2)}, {int(next_member.top + next_member.height / 2)}) {image}')
    pyautogui.click(next_member)
    # Click twice anywhere to dismiss dialogue
    if TAKE_SNAPSHOT:
        time.sleep(10)
    else:
        time.sleep(1)
