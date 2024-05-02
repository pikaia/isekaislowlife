import logging.handlers
import os
import sys
import time
from datetime import timedelta

import numpy as np
import pyautogui
import wx
from tkinter import *

APP_TITLE = 'BlueStacks App Player'
MAIN_MENU = 'resources/mainmenu/'
MM_HOME = 'resources/mainmenu/home.png'
MM_VILLAGE = 'resources/mainmenu/village.png'
MM_DRAKENBERG = 'resources/mainmenu/drakenberg.png'
MM_DRAKENBERG_ALT = 'resources/mainmenu/drakenberg_sm.png'

MM_DRAKENBERG_TRADINGPOST = 'resources/mainmenu/village/drakenberg/enter_trading_post.png'
TRADINGPOST_GOLD = 'resources/mainmenu/village/drakenberg/trading_post/gold.png'
TRADINGPOST_BACK = 'resources/mainmenu/village/drakenberg/trading_post/back.png'

DRAKENBERG_ROAMING = 'resources/mainmenu/village/drakenberg/roaming.png'
ROAMING_GO = 'resources/mainmenu/village/drakenberg/roaming/go.png'
ROAMING_OK = 'resources/mainmenu/village/drakenberg/roaming/ok.png'
ROAMING_CANCEL = 'resources/mainmenu/village/drakenberg/roaming/cancel.png'
ROAMING_BACK = 'resources/mainmenu/village/drakenberg/roaming/back.png'

SCHOOL_EDUCATE = 'resources/mainmenu/village/school/educate.png'
SCHOOL_BELOW_PUPILS = 'resources/mainmenu/village/school/below_pupils.png'
SCHOOL_BACK = 'resources/mainmenu/village/school/back.png'

VILLAGE_SCHOOL = 'resources/mainmenu/village/school.png'
VILLAGE_KITCHEN = 'resources/mainmenu/village/enter_kitchen.png'
KITCHEN_SERVE = 'resources/mainmenu/village/kitchen/serve.png'
KITCHEN_OK = 'resources/mainmenu/village/kitchen/ok.png'
KITCHEN_ORDER_JEWELS = 'resources/mainmenu/village/kitchen/order_jewels.png'
KITCHEN_CANCEL = 'resources/mainmenu/village/kitchen/cancel.png'
KITCHEN_GUESTS_AVAILABLE = 'resources/mainmenu/village/kitchen/guests_available.png'

DRAKENBERG_GUILD = 'resources/mainmenu/village/drakenberg/enter_guild.png'
GUILD_CANCEL = 'resources/mainmenu/village/drakenberg/guild/cancel.png'
GUILD_HANDLE = 'resources/mainmenu/village/drakenberg/guild/handle.png'
GUILD_REQUESTS = 'resources/mainmenu/village/drakenberg/guild/random_requests.png'

DRAKENBERG_STAGE = 'resources/mainmenu/village/drakenberg/stage.png'
STAGE_CHALLENGE = 'resources/mainmenu/village/drakenberg/stage/challenge.png'
CHALLENGE_EMPTY = 'resources/mainmenu/village/drakenberg/stage/challenge/items_empty.png'
CHALLENGE_GOLD = 'resources/mainmenu/village/drakenberg/stage/challenge/gold_motivation.png'
CHALLENGE_ITEM = 'resources/mainmenu/village/drakenberg/stage/challenge/item_motivation.png'
CHALLENGE_NEGOTIATE = 'resources/mainmenu/village/drakenberg/stage/challenge/negotiate.png'
CHALLENGE_CONTINUE = 'resources/mainmenu/village/drakenberg/stage/challenge/tap_to_continue.png'

STAGE_GO = 'resources/mainmenu/village/drakenberg/stage/go.png'
EVENTS_CONTINUE = 'resources/mainmenu/village/drakenberg/stage/events/tap_to_continue.png'
STAGE_EVENTS_X = 'resources/mainmenu/village/drakenberg/stage/events_x.png'
STAGE_EVENTS_Y = 'resources/mainmenu/village/drakenberg/stage/events_y.png'
STAGE_AUTOHANDLE = 'resources/mainmenu/village/drakenberg/stage/events/autohandle.png'


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


# start on the Drakenberg screen
def collect_trading_post_gold(maxtimes=30):
    # assume main menu is displayed.
    for x in range(1, maxtimes):
        start = time.time()
        log.info(f'Collecting gold {x}/{maxtimes}...')

        click_image(MM_DRAKENBERG)

        # Enter trading post
        click_image(MM_DRAKENBERG_TRADINGPOST)
        time.sleep(1)

        # Need higher confidence to match small image(?)
        gold = pyautogui.locateOnWindow(TRADINGPOST_GOLD, APP_TITLE,
                                          grayscale=True, confidence=0.7)
        # Give time for screen to refresh
        time.sleep(1)
        highlightSection(os.path.basename(TRADINGPOST_GOLD), gold)
        pyautogui.click(gold)

        click_image(TRADINGPOST_BACK, grayscale=False, confidence=0.6)
        click_image(MM_HOME, grayscale=False, confidence=0.6)
        # give time for gold to replenish
        time.sleep(7)

        elapsed = time.time() - start
        log.info(f'Time taken = {str(timedelta(seconds=elapsed))}')


# Assume your are in drakenberg screen.
def run_roaming():
    click_image(DRAKENBERG_ROAMING)
    time.sleep(1)
    click_image(ROAMING_GO)
    time.sleep(1.5)
    location = match_image(ROAMING_CANCEL, confidence=0.6)
    if location is None:
        #  ROAMING CANCEL not found, click on OK
        location = match_image(ROAMING_OK)
        pyautogui.click(location)
    else:
        # ROAMING CANCEL found. click it.
        pyautogui.click(location)
    # Get out of roaming
    click_image(ROAMING_BACK, confidence=0.6)


def run_stage():
    # start on the Drakenberg screen

    # add check for location.

    log.info('Running stage...')
    click_image(DRAKENBERG_STAGE)

    for x in range(1, 100):
        # if game is in challenge mode, skip stage
        gomode = match_image(STAGE_GO)
        if gomode is not None:
            pyautogui.click(gomode)
        else:
            challengemode = match_image(STAGE_CHALLENGE)
            if challengemode is not None:
                pyautogui.click(challengemode)

        # clear events. The events icon seems hard to locate directly. Colors?
        xtemp = pyautogui.locateOnScreen(STAGE_EVENTS_X, grayscale=True, confidence=0.5)
        highlightSection('eventx', xtemp)
        ytemp = pyautogui.locateOnScreen(STAGE_EVENTS_Y, grayscale=True, confidence=0.5)
        highlightSection('eventy', ytemp)
        log.info(f'Events is at {xtemp.left}, {ytemp.top}')
        highlightSection('events', (50, 50, xtemp.left, ytemp.top))
        pyautogui.click(xtemp.left, ytemp.top)
        click_image(STAGE_AUTOHANDLE)
        click_image(EVENTS_CONTINUE)

        # challenge
        click_image(STAGE_CHALLENGE)

        # harmless to overmotivate
        if pyautogui.locateOnScreen(CHALLENGE_EMPTY, grayscale=True, confidence=0.5):
            for y in range(1, 3):
                click_image(CHALLENGE_GOLD)
        else:
            for y in range(1, 3):
                click_image(CHALLENGE_ITEM)

        # negotiate and continue
        click_image(CHALLENGE_NEGOTIATE)
        click_image(CHALLENGE_CONTINUE)

    # MAIN
    for x in range(1, 100):
        print('Collecting gold {}.'.format(x))
        wait_for_image(MM_DRAKENBERG_TRADINGPOST)
        wait_for_image(TRADINGPOST_GOLD)
        # pause for gold to replenish
        time.sleep(6)
        wait_for_image(TRADINGPOST_BACK)


def scroll_screen(direction, times):
    if direction == 'left':
        for i in range(times):
            try:
                home = pyautogui.locateOnScreen(MM_HOME)
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
                home = pyautogui.locateOnScreen(MM_HOME)
                # 1.5 home above button

                # to drag screen right, move the mouse to the right and drag it left horizontally
                pyautogui.mouseDown(home.left + home.width * 6, home.top - home.height * 6)
                time.sleep(0.5)
                # 5 homes to right. duration is needed
                pyautogui.dragTo(home.left, home.top - home.height * 6, duration=0.5)
                time.sleep(0.5)
            except Exception as e:
                log.error(f'Expecting to see Home button on the bottom: {e}')


def run_kitchen():
    # add check for location.

    # start on the home screen
    click_image(MM_HOME, grayscale=True, confidence=0.6)

    # goto village
    click_image(MM_VILLAGE)

    scroll_screen('right', 2)

    # enter kitchen and serve
    while not match_image(VILLAGE_KITCHEN):
        scroll_screen('left', 1)
    click_image(VILLAGE_KITCHEN)

    # if there are jewels collect them
    if wait_for_image(KITCHEN_ORDER_JEWELS):
        click_image(KITCHEN_ORDER_JEWELS)
        click_image(KITCHEN_OK)

    # if guests available in queue, serve
    while not match_image(KITCHEN_GUESTS_AVAILABLE):
        time.sleep(1)

    click_image(KITCHEN_SERVE)

    pyautogui.press('escape')


def run_guild():
    # start on the home screen
    click_image(MM_HOME)
    click_image(MM_DRAKENBERG)
    scroll_screen('right', 1)
    click_image(DRAKENBERG_GUILD)
    click_image(GUILD_REQUESTS)
    click_image(GUILD_HANDLE)
    # let requests finish
    time.sleep(2)
    click_image(GUILD_CANCEL)


def grind():
    # add check for location.

    # start on the home screen
    click_image(MM_HOME)

    # collect some gold
    # collect_trading_post_gold(maxtimes=10)

    # STAGE
    run_stage()

    # goto village
    click_image(MM_VILLAGE)

    # enter kitchen and serve
    click_image(VILLAGE_KITCHEN)

    # if guests available in queue, serve
    if wait_for_image(KITCHEN_GUESTS_AVAILABLE):
        click_image(KITCHEN_SERVE)

        # sometimes dialog doesn't popup. Bluestacks bz?
        if wait_for_image(KITCHEN_SERVE):
            # if the match above is wrong, a dialog will pop up after a little pause.
            time.sleep(1.5)
            # cancel pic is centered above it, so we click on the background
            click_image(KITCHEN_CANCEL, grayscale=False)

    # if there are jewels collect them
    if wait_for_image(KITCHEN_ORDER_JEWELS):
        click_image(KITCHEN_ORDER_JEWELS)
        click_image(KITCHEN_OK)
    pyautogui.press('escape')

    # assume screen if positioned correctly on the leftmost.
    # to see the school move screen left.
    scroll_screen('left', 1)

    # school
    click_image(VILLAGE_SCHOOL)
    # First pupil is above back button
    back = pyautogui.locateOnScreen(SCHOOL_BACK)
    pyautogui.click(back.left + int(back.width / 2), back.top - back.height)
    click_image(SCHOOL_EDUCATE)

    # home = pyautogui.locateOnScreen(MM_HOME, grayscale=True, confidence=0.5)
    # log.info(f'Drag from {home.left, home.top - 6 * home.height} to {home.left + 6 * home.width, home.top - 6 * home.height}')
    # time.sleep(1)
    # pyautogui.moveTo(home.left, home.top - 6 * home.height)
    # pyautogui.mouseDown(button='left')
    # pyautogui.dragTo(home.left + 6 * home.width, home.top - 6 * home.height,1, button='left')


def run_school():
    # add check for location.
    if match_image(VILLAGE_KITCHEN):
        scroll_screen('right', 1)
    click_image(VILLAGE_SCHOOL)
    # start on the home screen
    click_image(MM_HOME)

    # students are between educate and back buttons
    educate_btn = match_image(SCHOOL_EDUCATE)
    back_btn = match_image(SCHOOL_BACK)

    if educate_btn is None or back_btn is None:
        log.error('Unable to find Educate or Back button. Stopping...')
        exit()
    pupil_y = educate_btn.top + educate_btn.height + (educate_btn.top + educate_btn.height - back_btn.top) / 2
    pupil_x = back_btn.left + back_btn.width
    pupils = []
    below_5pupils = match_image(SCHOOL_BELOW_PUPILS)
    for i in range(0, 4):
        pupils.append(Point2D(pupil_x + below_5pupils.width / 5 * i, pupil_y))

    # Click on pupil and educate
    for j in range(0, 3):
        pyautogui.click(pupils[j].x, pupils[j].y)
        click_image(SCHOOL_EDUCATE)


def test():
    loc = pyautogui.locateOnScreen(KITCHEN_GUESTS_AVAILABLE, grayscale=True,
                                   confidence=0.8)

    log.debug(loc)
    pyautogui.moveTo(loc.left, loc.top)
    time.sleep(1.5)


# Select the function based on the user input
while True:
    # Get the user input
    # number = int(
    #     input("Select a function (0 roam, 1 Gold, 2 Stage, 3 guild, 4 move right, 5 grind, 6 kitchen, 7 school): "))
    number = 1
    if number == 0:
        run_roaming()
    if number == 1:
        collect_trading_post_gold(3000)
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
