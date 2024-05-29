import collections
import logging.handlers
import os
import time
import typing
from datetime import timedelta
from tkinter import Tk
from typing import Optional

import pyautogui as pag
import pygetwindow
import wx
from PIL import Image
from pyscreeze import PyScreezeException

from slowlife.common.logger import CustomFormatter
from slowlife.resources.constants import APP_TITLE, MM_HOME, LOG_PAUSES, HIGHLIGHT, LOG_IMAGE, DRAKENBERG_GUILD

# Construct used types
Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# h = logging.StreamHandler(sys.stdout)
# h.setLevel(logging.DEBUG)
# h.setFormatter(formatter)
# log.addHandler(h)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())
log.addHandler(ch)
log.info(pag.position())

# python should default to where the script lives
log.info('ROOT: ' + os.getcwd())

app = pygetwindow.getWindowsWithTitle(APP_TITLE)[0]

# Init cache for locations of images on bluestacks window
LOC: typing.Dict[str, Box] = {}

# init run timer
start = time.time()


def elapsed_time(description: str, items: list):
    elapsed = time.time() - start
    log.info(f'# {description} = {len(items)}. Time taken = {str(timedelta(seconds=elapsed))}')


def log_sleep(where: str, duration: float):
    if LOG_PAUSES:
        log.info(f'{where}: Pausing for {duration} second...')
    pag.sleep(duration)


def highlight(caption: str, rect, color='red', duration=3) -> None:
    win = Tk()
    win.title = caption
    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/geometry.html
    # A geometry string has this general form: 'wxh±x±y'
    # where:
    # The w and h parts give the window width and height in pixels. They are separated by the character 'x'.
    # If the next part has the form +x, it specifies that the left side of the window should be x pixels
    # from the left side of the desktop. If it has the form -x, the right side of the window is x pixels
    # from the right side of the desktop.
    geometry = str(rect[2]) + 'x' + str(rect[3]) + '+' + str(rect[0]) + '+' + str(rect[1])
    win.geometry(geometry)
    log.debug(f'title={caption}, str = {geometry}')
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


def add_loc(key, location: Box) -> None:
    LOC[key] = location


# Copy the position of one to another.
def cloneposition(original, clone, dx: int = 0, dy: int = 0, _highlight: bool = False) -> None:
    loc = LOC[original]
    LOC[clone] = Box(loc.left + (dx * loc.width), loc.top + (dy * loc.height), loc.width, loc.height)
    log.info(
        f'Cloned {clone} from {original} @ ({int(LOC[clone].left + LOC[clone].width / 2)}, {int(LOC[clone].top + LOC[clone].height / 2)}) ')
    if _highlight:
        highlight(caption=f'{original}->{clone}', rect=LOC[clone])


# if a list is provided, locate the first match.
# When target image is provided, dx = width offset, When shifted save derived location.
# when target image is None, ignore.
# _derive is a dictionary with the key being the name of the image to derive, and the value being the offset wdx.
def click_list(aliases: list, title: str = APP_TITLE, confidence: float = 0.5, _highlight: bool = HIGHLIGHT,
               _click=True, _derive: Optional[dict] = None) -> Optional[Box]:
    for image in aliases:
        loc = click(image, title, confidence, _highlight, _click, match_optional=True)
        if loc is None:
            continue
        else:
            return loc


# When target image is provided, dx = width offset, When shifted save derived location.
# when target image is None, ignore.
# _derive is a dictionary with the key being the name of the image to derive, and the value being the offset wdx.
def click(image: str, title: str = APP_TITLE, confidence: float = 0.5, _highlight: bool = HIGHLIGHT, _pause: int = 1,
          _clicks: int = 1, _derive: Optional[typing.Dict[str, typing.Union[str, float]]] = None,
          match_optional=False, _use_cache: bool = True, _interval: float = 0.5) -> Optional[Box]:
    if _use_cache and image in LOC:
        loc = LOC.get(image)
        log.info(f'Using cached {image} @ ({int(loc.left + loc.width / 2)}, {int(loc.top + loc.height / 2)}) ')
    else:
        # if we can't find, move on to next in list.
        try:
            loc = pag.locateOnWindow(image=image, title=title, confidence=confidence, grayscale=True)
            log.info(f'Found {image} @ ({int(loc.left + loc.width / 2)}, {int(loc.top + loc.height / 2)}) ')
        except pag.ImageNotFoundException as e:
            if match_optional:
                return None
            else:
                log.error(f'Unable to find {image}...')
                # Retry on time.
                try:
                    log.error(f'Retry 1x to find {image}...')
                    log.warning('CHECK IF THE IMAGE NEEDS TO BE RECAPTURED.')
                    if image == DRAKENBERG_GUILD:
                        log.error(f'Please position Drakenberg screen so that Post and Guil are visible')
                    loc = pag.locateOnWindow(image=image, title=title, confidence=confidence, grayscale=True)
                    # on Retry highlight match
                    highlight(os.path.basename(image), loc)
                except pag.ImageNotFoundException as e:
                    # Take screenshot to clarify where we are stuck.
                    pag.screenshot(region=(app.left, app.top, app.right - app.left, app.bottom - app.top),
                                   imageFilename=LOG_IMAGE)
                    # display it.
                    img = Image.open(LOG_IMAGE)
                    img.show()
            exit(-1)

    if _clicks != 0:
        log.info(f'Click {image} @ ({int(loc.left + loc.width / 2)}, {int(loc.top + loc.height / 2)}) ')
    else:
        log.info(f'Located {image} @ ({int(loc.left + loc.width / 2)}, {int(loc.top + loc.height / 2)}) ')
    LOC[image] = loc

    if _derive is not None and _derive.get('target_image') is not None:
        if 'dx' in _derive:
            dx = _derive['dx']
        else:
            dx = 0
        if 'dy' in _derive:
            dy = _derive['dy']
        else:
            dy = 0

        loc = Box(loc.left + dx * loc.width, loc.top + dy * loc.height, loc.width, loc.height)
        LOC[_derive['target_image']] = loc

    if _highlight:
        highlight(os.path.basename(image), loc)

    if _clicks != 0:
        # when clicked, return point (left, top)
        pag.click(pag.center(loc), clicks=_clicks, interval=_interval)
    pag.sleep(_pause)

    return loc


def scroll_screen(direction, times):
    home = click(MM_HOME, confidence=0.5, _highlight=False, _clicks=False)

    if direction == 'left':
        for i in range(times):
            #  move to the right 5 homes to the right. drag it left horizontally, duration is needed
            start_box = Box(left=home.left + 20 + home.width * 6, top=home.top - home.height * 6, width=10, height=10)
            pag.mouseDown(start_box.top, start_box.left)
            highlight('start', start_box)
            # 5 homes to right. duration is needed
            stop = Box(left=home.left + 20, top=home.top - home.height * 6, width=10, height=10)
            pag.moveTo(x=stop.left, y=stop.top, duration=0.5)
            highlight('stop', stop)
    else:
        for i in range(times):
            # to drag screen right, start from the left. +5 to keep off the edge.
            start_box = Box(left=home.left + 20, top=home.top - home.height * 6, width=10, height=10)
            pag.mouseDown(start_box.top, start_box.left)
            highlight('start', start_box)
            #  move to the right 5 homes to the right. drag it left horizontally, duration is needed
            stop = Box(left=home.left + 20 + home.width * 6, top=home.top - home.height * 6, width=10, height=10)
            pag.moveTo(x=stop.left, y=stop.top, duration=0.5)
            highlight('stop', stop)

    pag.mouseUp()
    pag.sleep(2)


def choose_path(test_image1: str, image_ok1, image_ok2: str):
    try:
        pag.locateOnWindow(test_image1, APP_TITLE, grayscale=True, confidence=0.9)
        log.warning(f'test_image1 not available. Skipping.')
        # When this is no roaming available, a dialog appears
        # click anywhere (e.g. GO) to dismiss it.
        click(image_ok1)
        click(image_ok2)
    except pag.ImageNotFoundException:
        log.info('No stamina dialogue not found. Checking for Roaming OK.')
        pag.sleep(1)


def displayed(image: str, confidence: float = 0.5) -> bool:
    try:
        pag.locateOnWindow(image, APP_TITLE, confidence=confidence)
        return True
    except pag.ImageNotFoundException:
        return False


def locate_all_on_window(image, title, **kwargs):
    """
    TODO
    """
    matchingWindows = pygetwindow.getWindowsWithTitle(title)
    if len(matchingWindows) == 0:
        raise PyScreezeException('Could not find a window with %s in the title' % (title))
    elif len(matchingWindows) > 1:
        raise PyScreezeException(
            'Found multiple windows with %s in the title: %s' % (title, [str(win) for win in matchingWindows])
        )

    win = matchingWindows[0]
    win.activate()
    return pag.locateAll(image, region=(win.left, win.top, win.width, win.height), **kwargs)
