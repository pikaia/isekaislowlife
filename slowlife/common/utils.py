import logging.handlers
import os
import sys
import time
from tkinter import *

import numpy as np
import pyautogui
import wx

from slowlife.resources.constants import APP_TITLE


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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


def highlight(x, y, width, height):
    # init
    app = wx.App()
    dc = wx.ScreenDC()

    # set line and fill style
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetPen(wx.Pen((255, 0, 0), width=3, style=wx.PENSTYLE_SOLID))

    # draw (x, y, width, height)
    dc.DrawRectangle(x, y, width, height)


def match_image(image, grayscale=True, confidence=0.5):
    try:
        log.debug('looking for ' + image)
        location = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=grayscale, confidence=confidence)
        highlightSection('app', location)

        log.info(f'Found {image} at {location}')
        return location
    except Exception as e:
        log.error(f'{image} Not Found. Exception: {repr(e)}')
        return None


def wait_for_image(image):
    location = None
    x = 0
    while location is None:
        try:
            log.debug('looking for ' + image)
            location = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=True, confidence=0.5)
            highlightSection(os.path.basename(image), location)
            log.debug('Found ' + image)
            return True
        except Exception as e:
            log.debug(f'Not Found {image}. Exception: {repr(e)}')
            time.sleep(1)
            log.debug('.'),
            x += 1
            if x > 5:
                return False

    log.debug('Found image at:' + repr(location))
    return True


def wait_for_images(images):
    if np.isscalar(images):
        log.error('Error should only be called if searching for list of')
        exit(-1)

    # For each call, capture your screen only once.
    haystack = pyautogui.screenshot()

    location = None
    x = 0
    while location is None:
        log.debug('looking for one of ' + repr(images))

        for image in images:

            # Get coordinates of image within screen capture
            try:
                location = pyautogui.locate(image, haystack, grayscale=True)
                log.debug('Found ' + image + ' at ' + repr(location))
                return True
            except AttributeError:
                log.debug('Ignore exception while searching through: ' + image)

        log.debug('Not Found ' + repr(images))
        log.debug('.'),
        x += 1
        if x > 5:
            log.debug('Not Found after 5 tries: ' + repr(images))
            return False


def click_one_of_images(images, grayscale=True, confidence=0.5):
    """
    Loops through a list of conditions and returns the first one that evaluates to True.
    If none of the conditions are satisfied, returns None.
    """
    for image in images:
        if click_image(image, grayscale, confidence):
            return True
    return False


def click_image(image, grayscale=True, confidence=0.5):
    location = None

    while location is None:
        try:
            log.debug('Looking for ' + repr(image))
            # pyautogui.locateOnScreen(image, 1, grayscale=grayscale, confidence=confidence)
            #  location = pyautogui.locateOnWindow(image, APP_TITLE, grayscale=grayscale, confidence=0.4)
            location = pyautogui.locateOnScreen(image, 1, grayscale=grayscale, confidence=confidence)
            # highlight(x=location.left, y=location.top, width=location.width, height=location.height)
            highlightSection(os.path.basename(image), location)
            pyautogui.click(int(location.left + location.width / 2), int(location.top + location.height / 2))
            log.info(
                f'Click ({int(location.left + location.width / 2)}, {int(location.top + location.height / 2)}) {image}')
            return location
        except Exception as e:
            time.sleep(1)
            log.debug(repr(e))

    log.debug('Found ' + image + ' at:' + repr(location))


def click_image_one_of(image1, image2, grayscale=True, confidence=0.5):
    location = None

    image = image1
    while location is None:
        try:
            log.debug('Looking for ' + image1)

            # Try looking for first image
            try:
                location = pyautogui.locateOnScreen(image, 1, grayscale=grayscale, confidence=confidence)
            except pyautogui.ImageNotFoundException as e:
                image = image2
                location = pyautogui.locateOnScreen(image2, 1, grayscale=grayscale, confidence=confidence)

            # highlight(x=location.left, y=location.top, width=location.width, height=location.height)
            highlightSection(os.path.basename(image), location)
            pyautogui.click(int(location.left + location.width / 2), int(location.top + location.height / 2))
            log.info(
                f'Click ({int(location.left + location.width / 2)}, {int(location.top + location.height / 2)}) {image}')
            return location
        except Exception as e:
            time.sleep(1)
            log.debug(repr(e))

    log.debug('Found ' + image + ' at:' + repr(location))


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.DEBUG)
h.setFormatter(formatter)
log.addHandler(h)

log.warning(pyautogui.position())

# python should default to where the script lives
log.warning('ROOT: ' + os.getcwd())
