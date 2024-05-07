import time
from datetime import timedelta

import pyautogui as pag
from pyautogui import ImageNotFoundException

from slowlife.common.utils import (log,
                                   click,
                                   log_sleep,
                                   start,
                                   Point,
                                   cloneposition,
                                   click_list,
                                   scroll_screen,
                                   click_image,
                                   match_image,
                                   wait_for_image,
                                   highlightimage)
from slowlife.resources.constants import (HIGHLIGHT_MATCH,
                                          MM_DRAKENBERG,
                                          COLLECT_COLD,
                                          MM_DRAKENBERG_TRADINGPOST,
                                          TRADINGPOST_GOLD1,
                                          TRADINGPOST_GOLD2,
                                          TRADINGPOST_BACK,
                                          RANDOM_REQUESTS,
                                          DRAKENBERG_GUILD, GUILD_REQUESTS,
                                          GUILD_HANDLE,
                                          GUILD_BACK,
                                          ROAMING,
                                          ENTER_ROAMING,
                                          ROAMING_GO,
                                          ROAMING_OK,
                                          ROAMING_BACK,
                                          ENTER_KITCHEN,
                                          MM_VILLAGE,
                                          ENTER_FISHING,
                                          FISHING_COLLECT_BAIT,
                                          KITCHEN_SERVE,
                                          KITCHEN_BACK,
                                          ROAMING_CANCEL,
                                          DRAKENBERG_STAGE, STAGE_GO,
                                          STAGE_CHALLENGE,
                                          STAGE_EVENTS_X,
                                          STAGE_EVENTS_Y,
                                          STAGE_AUTOHANDLE,
                                          EVENTS_CONTINUE,
                                          CHALLENGE_EMPTY,
                                          CHALLENGE_GOLD,
                                          CHALLENGE_NEGOTIATE,
                                          CHALLENGE_CONTINUE,
                                          CHALLENGE_ITEM,
                                          KITCHEN_ORDER_JEWELS,
                                          KITCHEN_OK,
                                          KITCHEN_GUESTS_AVAILABLE,
                                          GUILD_CANCEL,
                                          KITCHEN_CANCEL,
                                          VILLAGE_SCHOOL,
                                          SCHOOL_BACK,
                                          SCHOOL_EDUCATE,
                                          SCHOOL_BELOW_PUPILS,
                                          MM_HOME,
                                          APP_TITLE)


# to start:
# 1. start on any screen with main menu below.
# 2. if trading pot gold is maxed out, clear it first.
# 3. in the village make sure inn and fish are on the screen.
def collect_trading_post_gold(maxtimes=30):
    # Save commonly needed positions.
    click(MM_HOME, confidence=0.6, _click_image=False, _highlight_image=HIGHLIGHT_MATCH)
    # Back button is in same position on different screens
    cloneposition(MM_HOME, 'BACK')
    cloneposition(MM_HOME, 'NOTHING', dx=3)
    click(MM_DRAKENBERG, _click_image=False, _highlight_image=HIGHLIGHT_MATCH)
    # village is to the right of home.
    click(MM_HOME, _derive={'target_image': MM_VILLAGE, 'dx': 1}, _click_image=False, _highlight_image=HIGHLIGHT_MATCH)

    for x in range(0, maxtimes):
        if COLLECT_COLD:
            # assume main menu is displayed.
            log.info(f'Collecting gold {x}/{maxtimes}...')
            click(MM_DRAKENBERG, _highlight_image=HIGHLIGHT_MATCH)
            click(MM_DRAKENBERG_TRADINGPOST, _highlight_image=HIGHLIGHT_MATCH)

            # Need higher confidence to match small image(?)
            # Also it may be one of 2 possible images.
            click_list([TRADINGPOST_GOLD1, TRADINGPOST_GOLD2], title=APP_TITLE, confidence=0.48)
            click(TRADINGPOST_BACK, confidence=0.6, _highlight_image=HIGHLIGHT_MATCH)
            click(MM_HOME, confidence=0.6, _highlight_image=HIGHLIGHT_MATCH)

        # Guild random requests
        # 10 mins to generate a free try. Each gold loop with just gold is 26 seconds. 24 = 10*60/26
        if RANDOM_REQUESTS and (x % 24 == 0):
            log.info('Random requests...')
            click(MM_DRAKENBERG, confidence=0.6, _highlight_image=HIGHLIGHT_MATCH)
            scroll_screen('left', 1)
            log_sleep('RANDOM_REQUESTS1', 0.5)
            click(DRAKENBERG_GUILD, _highlight_image=HIGHLIGHT_MATCH)
            click(GUILD_REQUESTS, _highlight_image=HIGHLIGHT_MATCH)
            click(GUILD_HANDLE, _highlight_image=HIGHLIGHT_MATCH)
            click(MM_DRAKENBERG, _highlight_image=HIGHLIGHT_MATCH)
            click(GUILD_BACK, confidence=0.9)

        # Roam if possible. Free try every 9 mins. 21 = 9*60/26
        if ROAMING and x % 21 == 0:
            scroll_screen('right', 1)
            pag.sleep(1)
            click(ENTER_ROAMING, _highlight_image=HIGHLIGHT_MATCH)
            # Give time for screen to refresh
            log_sleep('ROAMING', 0.5)
            click(ROAMING_GO, _highlight_image=HIGHLIGHT_MATCH)
            log_sleep('ROAMING', 1)

            # roaming has outcomes when u click on GO
            # 1. roaming not available: go -> error dialogue -> click go again to dismiss -> back
            # 2. roaming available:     go -> ok diagloue -> click ok -> back
            roaming_ok = None
            try:
                roaming_ok = pag.locateOnWindow(ROAMING_OK, APP_TITLE, grayscale=True, confidence=0.9)
                pag.click(roaming_ok)
            except ImageNotFoundException as e:
                # When this is no roaming available, a dialog appears
                # click anywhere to dismiss it.
                click(ROAMING_GO, _highlight_image=HIGHLIGHT_MATCH)

            # Click on back to continue
            click(ROAMING_BACK, _highlight_image=HIGHLIGHT_MATCH)

        # serve in inn. Free try every 20 mins. 47 = 20*60/26
        # if ENTER_KITCHEN and (x % 47 == 0):
        if ENTER_KITCHEN:
            log.info('Enter village...')
            # Enter village
            log_sleep('Village', 1)
            click(MM_VILLAGE, confidence=0.45, _highlight_image=HIGHLIGHT_MATCH)

            # Collect fishing bait
            log.info('Collect bait...')
            click(ENTER_FISHING, _highlight_image=HIGHLIGHT_MATCH)
            click(FISHING_COLLECT_BAIT, _highlight_image=HIGHLIGHT_MATCH)
            # Dismiss any popup
            click('NOTHING', _highlight_image=HIGHLIGHT_MATCH)

            click('BACK', _highlight_image=HIGHLIGHT_MATCH)

            # Enter kitchen
            log.info('Enter Inn...')
            log_sleep('KITCHEN', 1)
            click(ENTER_KITCHEN, _highlight_image=HIGHLIGHT_MATCH)
            # Press serve button.
            click(KITCHEN_SERVE, _highlight_image=HIGHLIGHT_MATCH)
            # calc where to click to dismiss dialog.
            click(KITCHEN_SERVE, _highlight_image=HIGHLIGHT_MATCH, _derive={'target_image': 'empty area', 'dx': -1},
                  _click_image=False)
            # If success, click serve again to dismiss.
            # If failed, click serve again to dismiss error.
            click('empty area', _highlight_image=HIGHLIGHT_MATCH)
            click('empty area', _highlight_image=HIGHLIGHT_MATCH)
            # Back out of inn
            click(KITCHEN_BACK, _highlight_image=HIGHLIGHT_MATCH)

        # give time for gold to replenish
        log_sleep('LAST_LOOP', 7)

    elapsed = time.time() - start
    log.info(f'Time taken = {str(timedelta(seconds=elapsed))}')


# Assume your are in drakenberg screen.
def run_roaming():
    click_image(ENTER_ROAMING)
    pag.sleep(1)
    click_image(ROAMING_GO)
    pag.sleep(1.5)
    location = match_image(ROAMING_CANCEL, confidence=0.6)
    if location is None:
        #  ROAMING CANCEL not found, click on OK
        location = match_image(ROAMING_OK)
        pag.click(location)
    else:
        # ROAMING CANCEL found. click it.
        pag.click(location)
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
            pag.click(gomode)
        else:
            challengemode = match_image(STAGE_CHALLENGE)
            if challengemode is not None:
                pag.click(challengemode)

        # clear events. The events icon seems hard to locate directly. Colors?
        xtemp = pag.locateOnScreen(STAGE_EVENTS_X, grayscale=True, confidence=0.5)
        highlightimage('eventx', xtemp)
        ytemp = pag.locateOnScreen(STAGE_EVENTS_Y, grayscale=True, confidence=0.5)
        highlightimage('eventy', ytemp)
        log.info(f'Events is at {xtemp.left}, {ytemp.top}')
        highlightimage('events', (50, 50, xtemp.left, ytemp.top))
        pag.click(xtemp.left, ytemp.top)
        click_image(STAGE_AUTOHANDLE)
        click_image(EVENTS_CONTINUE)

        # challenge
        click_image(STAGE_CHALLENGE)

        # harmless to overmotivate
        if pag.locateOnScreen(CHALLENGE_EMPTY, grayscale=True, confidence=0.5):
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
        wait_for_image(TRADINGPOST_GOLD1)
        # pause for gold to replenish
        pag.sleep(6)
        wait_for_image(TRADINGPOST_BACK)


def run_kitchen():
    # add check for location.

    # start on the home screen
    click_image(MM_HOME, grayscale=True, confidence=0.6)

    # goto village
    click_image(MM_VILLAGE)

    scroll_screen('right', 2)

    # enter kitchen and serve
    while not match_image(ENTER_KITCHEN):
        scroll_screen('left', 1)
    click_image(ENTER_KITCHEN)

    # if there are jewels collect them
    if wait_for_image(KITCHEN_ORDER_JEWELS):
        click_image(KITCHEN_ORDER_JEWELS)
        click_image(KITCHEN_OK)

    # if guests available in queue, serve
    while not match_image(KITCHEN_GUESTS_AVAILABLE):
        pag.sleep(1)

    click_image(KITCHEN_SERVE)

    pag.press('escape')


def run_guild():
    # start on the home screen
    click_image(MM_HOME)
    click_image(MM_DRAKENBERG)
    scroll_screen('right', 1)
    click_image(DRAKENBERG_GUILD)
    click_image(GUILD_REQUESTS)
    click_image(GUILD_HANDLE)
    # let requests finish
    pag.sleep(2)
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
    click_image(ENTER_KITCHEN)

    # if guests available in queue, serve
    if wait_for_image(KITCHEN_GUESTS_AVAILABLE):
        click_image(KITCHEN_SERVE)

        # sometimes dialog doesn't popup. Bluestacks bz?
        if wait_for_image(KITCHEN_SERVE):
            # if the match above is wrong, a dialog will pop up after a little pause.
            pag.sleep(1.5)
            # cancel pic is centered above it, so we click on the background
            click_image(KITCHEN_CANCEL, grayscale=False)

    # if there are jewels collect them
    if wait_for_image(KITCHEN_ORDER_JEWELS):
        click_image(KITCHEN_ORDER_JEWELS)
        click_image(KITCHEN_OK)
    pag.press('escape')

    # assume screen if positioned correctly on the leftmost.
    # to see the school move screen left.
    scroll_screen('left', 1)

    # school
    click_image(VILLAGE_SCHOOL)
    # First pupil is above back button
    back = pag.locateOnScreen(SCHOOL_BACK)
    pag.click(back.left + int(back.width / 2), back.top - back.height)
    click_image(SCHOOL_EDUCATE)

    # home = pag.locateOnScreen(MM_HOME, grayscale=True, confidence=0.5) log.info(f'Drag from {home.left, home.top -
    # 6 * home.height} to {home.left + 6 * home.width, home.top - 6 * home.height}') pag.sleep(1) pag.moveTo(
    # home.left, home.top - 6 * home.height) pag.mouseDown(button='left') pag.dragTo(home.left + 6 * home.width,
    # home.top - 6 * home.height,1, button='left')


def run_school():
    # add check for location.
    if match_image(ENTER_KITCHEN):
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
        pupils.append(Point(pupil_x + below_5pupils.width / 5 * i, pupil_y))

    # Click on pupil and educate
    for j in range(0, 3):
        pag.click(pupils[j].x, pupils[j].y)
        click_image(SCHOOL_EDUCATE)


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

    pag.sleep(3)
