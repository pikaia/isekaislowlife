import os
import time
from datetime import timedelta

import pyautogui

from common.utils import click_image, log, highlightSection, match_image, wait_for_image
from resources.constants import *


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
                                        grayscale=True, confidence=0.5)
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
