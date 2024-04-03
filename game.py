import logging.handlers
import os
import sys
import time

import numpy as np
import pyautogui
import wx
from tkinter import *

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
h = logging.StreamHandler(sys.stdout)
h.setLevel(logging.DEBUG)
h.setFormatter(formatter)
log.addHandler(h)

log.warning(pyautogui.position())
# pyautogui.LOG_SCREENSHOTS = True
# pyautogui.LOG_SCREENSHOTS_LIMIT = None

# python should default to where the script lives
log.warning('ROOT: ' + os.getcwd())


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
    log.info(f'title={title}, str = {geometry}')
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
        location = pyautogui.locateOnWindow(image, 'BlueStacks App Player', grayscale=grayscale, confidence=confidence)
        highlightSection('app', location)
        log.info(f'Found {image} at {location}')
        return location
    except Exception as e:
        log.info(f'{image} Not Found. Exception: {repr(e)}')
        return None


def wait_for_image(image):
    location = None
    x = 0
    while location is None:
        try:
            log.debug('looking for ' + image)
            location = pyautogui.locateOnWindow(image, 'BlueStacks App Player',grayscale=True, confidence=0.5)
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


def click_image(image, grayscale=True, confidence=0.5):
    location = None

    while location is None:
        try:
            log.info('Looking for ' + image)
            location = pyautogui.locateOnScreen(image, 1, grayscale=grayscale, confidence=confidence)
            # highlight(x=location.left, y=location.top, width=location.width, height=location.height)
            highlightSection(os.path.basename(image), location)
            pyautogui.click(int(location.left + location.width / 2), int(location.top + location.height / 2))
            log.debug(
                f'Found at ({int(location.left + location.width / 2)}, {int(location.top + location.height / 2)}) {image}')
        except Exception as e:
            log.info('Not Found ' + image + repr(e))
            time.sleep(1)

    log.info('Found ' + image + ' at:' + repr(location))
    time.sleep(1)


# start on the Drakenberg screen
def collect_trading_post_gold(maxtimes=30):
    # assume main menu is displayed.
    for x in range(1, maxtimes):
        log.info(f'Collecting gold {x}/{maxtimes}...')

        click_image('resources/mainmenu/drakenberg.png')

        # Enter trading post
        click_image('resources/mainmenu/village/drakenberg/enter_trading_post.png')
        time.sleep(1)

        # clicking on gold is tricky as the screen changes. Locate the fixTure next to gold
        # and navigate there
        image = 'resources/mainmenu/village/drakenberg/trading_post/gold_small.png'
        bottom = pyautogui.locateOnWindow(image, 'BlueStacks App Player',
                                          grayscale=True, confidence=0.4)
        highlightSection(os.path.basename(image), bottom)
        pyautogui.click(bottom)

        time.sleep(1)
        click_image('resources/mainmenu/village/drakenberg/trading_post/back.png', grayscale=False, confidence=0.6)
        time.sleep(1)
        click_image('resources/mainmenu/home.png', grayscale=False, confidence=0.6)
        time.sleep(7)


def run_stage():
    # start on the Drakenberg screen
    path = 'resources/mainmenu/village/drakenberg/'

    # add check for location.

    log.info('Running stage...')
    click_image(path + "stage.png")

    path = path + 'stage/'
    for x in range(1, 100):
        # if game is in challenge mode, skip stage
        gomode = match_image(path + 'go.png')
        if gomode is not None:
            pyautogui.click(gomode)
        else:
            challengemode = match_image(path + 'challenge.png')
            if challengemode is not None:
                pyautogui.click(challengemode)

        # clear events. The events icon seems hard to locate directly. Colors?
        xtemp = pyautogui.locateOnScreen(path + 'events_x.png', grayscale=True, confidence=0.5)
        highlightSection('eventx', xtemp)
        ytemp = pyautogui.locateOnScreen(path + 'events_y.png', grayscale=True, confidence=0.5)
        highlightSection('eventy', ytemp)
        log.info(f'Events is at {xtemp.left}, {ytemp.top}')
        highlightSection('events', (50, 50, xtemp.left,ytemp.top))
        pyautogui.click(xtemp.left,ytemp.top)
        click_image(path + 'events/autohandle.png')
        click_image(path + 'events/tap_to_continue.png')

        # challenge
        click_image(path + 'stage/challenge.png')

        # harmless to overmotivate
        if pyautogui.locateOnScreen(path + 'challenge/items_empty.png', grayscale=True, confidence=0.5):
            for y in range(1, 3):
                click_image(path + 'challenge/gold_motivation.png')
        else:
            for y in range(1, 3):
                click_image(path + 'challenge/item_motivation.png')

        # negotiate and continue
        click_image(path + 'challenge/negotiate.png')
        click_image(path + 'challenge/tap_to_continue.png')

    # MAIN
    for x in range(1, 100):
        print('Collecting gold {}.'.format(x))
        wait_for_image(path + 'enter_trading_post.png')
        wait_for_image(path + 'trading_post/gold.png')
        # pause for gold to replenish
        time.sleep(6)
        wait_for_image(path + 'trading_post/back.png')


def scroll_screen(direction, times):
    if direction == 'left':
        for i in range(times):
            try:
                home = pyautogui.locateOnScreen('resources/mainmenu/home.png')
                # 1.5 home above button

                # to drag screen right, move the mouse to the right and drage it left horizontally
                pyautogui.mouseDown(home.left + home.width * 6, home.top - home.height * 6)
                # 5 homes to right. duration is needed
                pyautogui.dragTo(home.left, home.top - home.height * 6, duration=0.5)
                time.sleep(2)
            except Exception as e:
                log.error(f'Expecting to see Home button on the bottom: {e}')
    else:
        for i in range(times):
            try:
                home = pyautogui.locateOnScreen('resources/mainmenu/home.png')
                # 1.5 home above button

                # to drag screen right, move the mouse to the right and drag it left horizontally
                pyautogui.mouseDown(home.left+ home.width * 6, home.top - home.height * 6)
                time.sleep(0.5)
                # 5 homes to right. duration is needed
                pyautogui.dragTo(home.left , home.top - home.height * 6, duration=0.5)
                time.sleep(0.5)
            except Exception as e:
                log.error(f'Expecting to see Home button on the bottom: {e}')


def run_kitchen():
    # add check for location.

    # start on the home screen
    click_image('resources/mainmenu/home.png', grayscale=True, confidence=0.6)

    # goto village
    click_image('resources/mainmenu/village.png')

    scroll_screen('right', 2)

    # enter kitchen and serve
    while not match_image('resources/mainmenu/village/enter_kitchen.png'):
        scroll_screen('left', 1)
    click_image('resources/mainmenu/village/enter_kitchen.png')

    # if there are jewels collect them
    if wait_for_image('resources/mainmenu/village/kitchen/order_jewels.png'):
        click_image('resources/mainmenu/village/kitchen/order_jewels.png')
        click_image('resources/mainmenu/village/kitchen/ok.png')

    # if guests available in queue, serve
    while not match_image('resources/mainmenu/village/kitchen/guests_available.png'):
        time.sleep(1)

    click_image('resources/mainmenu/village/kitchen/serve.png')

    pyautogui.press('escape')


def run_guild():
    # start on the home screen
    click_image('resources/mainmenu/home.png')
    click_image('resources/mainmenu/drakenberg.png')
    scroll_screen('right', 1)
    click_image('resources/mainmenu/village/drakenberg/enter_guild.png')
    click_image('resources/mainmenu/village/drakenberg/guild/random_requests.png')
    click_image('resources/mainmenu/village/drakenberg/guild/handle.png')
    # let requests finish
    time.sleep(2)
    click_image('resources/mainmenu/village/drakenberg/guild/cancel.png')

def grind():
    # add check for location.

    # start on the home screen
    click_image('resources/mainmenu/home.png')

    # collect some gold
    # collect_trading_post_gold(maxtimes=10)

    # STAGE
    run_stage()

    # goto village
    click_image('resources/mainmenu/village.png')

    # enter kitchen and serve
    click_image('resources/mainmenu/village/enter_kitchen.png')

    # if guests available in queue, serve
    if wait_for_image('resources/mainmenu/village/kitchen/guests_available.png'):
        click_image('resources/mainmenu/village/kitchen/serve.png')

        # sometimes dialog doesn't popup. Bluestacks bz?
        if wait_for_image('resources/mainmenu/village/kitchen/serve.png'):
            # if the match above is wrong, a dialog will pop up after a little pause.
            time.sleep(1.5)
            # cancel pic is centered above it, so we click on the background
            click_image('resources/mainmenu/village/kitchen/cancel.png', grayscale=False)

    # if there are jewels collect them
    if wait_for_image('resources/mainmenu/village/kitchen/order_jewels.png'):
        click_image('resources/mainmenu/village/kitchen/order_jewels.png')
        click_image('resources/mainmenu/village/kitchen/ok.png')
    pyautogui.press('escape')

    # assume screen if positioned correctly on the leftmost.
    # to see the school move screen left.
    scroll_screen('left', 1)

    # school
    click_image('resources/mainmenu/village/school.png')
    # First pupil is above back button
    back = pyautogui.locateOnScreen('resources/mainmenu/village/school/back.png')
    pyautogui.click(back.left + int(back.width / 2), back.top - back.height)
    click_image('resources/mainmenu/village/school/educate.png')

    # home = pyautogui.locateOnScreen('resources/mainmenu/home.png', grayscale=True, confidence=0.5)
    # log.info(f'Drag from {home.left, home.top - 6 * home.height} to {home.left + 6 * home.width, home.top - 6 * home.height}')
    # time.sleep(1)
    # pyautogui.moveTo(home.left, home.top - 6 * home.height)
    # pyautogui.mouseDown(button='left')
    # pyautogui.dragTo(home.left + 6 * home.width, home.top - 6 * home.height,1, button='left')


def run_school():
    # add check for location.
    if match_image('resources/mainmenu/village/enter_kitchen.png'):
        scroll_screen('right', 1)
    click_image('resources/mainmenu/village/school.png')
    # start on the home screen
    click_image('resources/mainmenu/home.png')

    # students are between educate and back buttons
    educate_btn = match_image('resources/mainmenu/village/school/educate.png')
    back_btn = match_image('resources/mainmenu/village/school/back.png')

    if educate_btn is None or back_btn is None:
        log.error('Unable to find Educate or Back button. Stopping...')
        exit()
    pupil_y = educate_btn.top + educate_btn.height + (educate_btn.top + educate_btn.height - back_btn.top)/2
    pupil_x = back_btn.left + back_btn.width
    pupils = []
    below_5pupils = match_image('resources/mainmenu/village/school/below_pupils.png')
    for i in range(0,4):
        pupils.append(Point2D(pupil_x+below_5pupils.width/5*i, pupil_y))

    # Click on pupil and educate
    for j in range(0,3):
        pyautogui.click(pupils[j].x, pupils[j].y)
        click_image('resources/mainmenu/village/school/educate.png')


def test():
    loc = pyautogui.locateOnScreen('resources/mainmenu/village/kitchen/guests_available.png', grayscale=True,
                                   confidence=0.8)

    log.debug(loc)
    pyautogui.moveTo(loc.left, loc.top)
    time.sleep(1.5)


# Select the function based on the user input
while True:
    # Get the user input
    number = int(input("Select a function (0 Test, 1 Gold, 2 Stage, 3 guild, 4 move right, 5 grind, 6 kitchen, 7 school): "))
    if number == 1:
        collect_trading_post_gold(300)
    elif number == 2:
        run_stage()
    elif number == 3:
        run_guild()
    elif number == 4:
        scroll_screen('right', 1)
    elif number == 5:
        grind()
    elif number == 6:
        run_kitchen()
    elif number == 7:
        run_school()
    else:
        print("Invalid input, quiting...")
        exit()

    time.sleep(3)
