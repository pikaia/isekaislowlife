import collections
import logging.handlers
import os
import sys
import time
from datetime import timedelta
from tkinter import *
from typing import Optional, NamedTuple

import pyautogui as pag
import wx

from slowlife.resources.constants import APP_TITLE, MM_HOME, LOG_PAUSES

# Construct used types
Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.DEBUG)
h.setFormatter(formatter)
log.addHandler(h)

log.warning(pag.position())

# python should default to where the script lives
log.warning('ROOT: ' + os.getcwd())

# Init cache for locations of images on bluestacks window
LOC = {}

# init run timer
start = time.time()


def elapsed_time(description: str, items: list):
    elapsed = time.time() - start
    log.info(f'# {description} = {len(items)}. Time taken = {str(timedelta(seconds=elapsed))}')


def log_sleep(where: str, duration: float):
    if LOG_PAUSES:
        log.info(f'{where}: Pausing for {duration} second...')
    pag.sleep(duration)


def highlight(title, rect, color='red', duration=3) -> None:
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


def box_match(x, y, width, height):
    # init
    app = wx.App()
    dc = wx.ScreenDC()

    # set line and fill style
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetPen(wx.Pen((255, 0, 0), width=3, style=wx.PENSTYLE_SOLID))

    # draw (x, y, width, height)
    dc.DrawRectangle(x, y, width, height)


# Copy the position of one to another.
def cloneposition(original, other, dx: int = 0, dy: int = 0) -> None:
    loc = LOC[original]
    LOC[other] = Box(loc.left + (dx * loc.width), loc.top + (dy * loc.height), loc.width, loc.height)


# if a list is provided, locate the first match.
# When target image is provided, dx = width offset, When shifted save derived location.
# when taget image is None, ignore.
# _derive is a dictionary with the key being the name of the image to derive, and the value being the offset wdx.
def click_list(original_image_list: list, title=APP_TITLE, confidence=0.5, _highlight=True, _click=True,
               _derive: Optional[dict] = None) -> Optional[Box]:
    for original_image in original_image_list:
        loc = click(original_image, title, confidence, _highlight, _click)
        if loc is None:
            continue
        else:
            return loc


# When target image is provided, dx = width offset, When shifted save derived location.
# when taget image is None, ignore.
# _derive is a dictionary with the key being the name of the image to derive, and the value being the offset wdx.
def click(image, title=APP_TITLE, confidence=0.5, _highlight=True, _click=True,
          _derive: Optional[dict] = None) -> Optional[Box]:
    # When not clicked return box (left, top, width, height).
    if image in LOC:
        loc = LOC.get(image)
    else:
        # if we can't find, move on to next in list.
        try:
            loc = pag.locateOnWindow(image=image, title=title, confidence=confidence, grayscale=True)
        except pag.ImageNotFoundException:
            log.error(f'Cant find {image}')
            return None

    if _click:
        log.info(f'Click {image} @ ({int(loc.left + loc.width / 2)}, {int(loc.top + loc.height / 2)}) ')
    else:
        log.info(f'Located {image} @ ({int(loc.left + loc.width / 2)}, {int(loc.top + loc.height / 2)}) ')
    LOC[image] = loc

    if _derive is not None and _derive.get('target_image') is not None:
        dx = _derive['dx']
        loc = Box(loc.left + dx * loc.width, loc.top, loc.width, loc.height)
        LOC[_derive['target_image']] = loc

    if _highlight:
        highlight(os.path.basename(image), loc)

    if _click:
        # when clicked, return point (left, top)
        pag.click(pag.center(loc))
    pag.sleep(1)

    return loc


def scroll_screen(direction, times):
    home = click(MM_HOME, confidence=0.5, _highlight=False, _click=False)

    if direction == 'left':
        for i in range(times):
            #  move to the right 5 homes to the right. drag it left horizontally, duration is needed
            start = Box(left=home.left + 20 + home.width * 6, top=home.top - home.height * 6, width=10, height=10)
            pag.mouseDown(start.top, start.left)
            highlight('start', start)
            # 5 homes to right. duration is needed
            stop = Box(left=home.left + 20, top=home.top - home.height * 6, width=10, height=10)
            pag.moveTo(x=stop.left, y=stop.top, duration=0.5)
            highlight('stop', stop)
    else:
        for i in range(times):
            # to drag screen right, start from the left. +5 to keep off the edge.
            start = Box(left=home.left + 20, top=home.top - home.height * 6, width=10, height=10)
            pag.mouseDown(start.top, start.left)
            highlight('start', start)
            #  move to the right 5 homes to the right. drag it left horizontally, duration is needed
            stop = Box(left=home.left + 20 + home.width * 6, top=home.top - home.height * 6, width=10, height=10)
            pag.moveTo(x=stop.left, y=stop.top, duration=0.5)
            highlight('stop', stop)

    pag.mouseUp()
    pag.sleep(2)
