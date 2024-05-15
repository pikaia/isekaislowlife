import time
from datetime import timedelta

import pyautogui as pag
from pyautogui import ImageNotFoundException

from slowlife.common.utils import (log,
                                   click,
                                   log_sleep,
                                   start,
                                   cloneposition,
                                   click_list)
from slowlife.resources.constants import (HIGHLIGHT,
                                          MM_DRAKENBERG,
                                          COLLECT_GOLD,
                                          MM_DRAKENBERG_TRADINGPOST,
                                          TRADINGPOST_GOLD1,
                                          TRADINGPOST_GOLD2,
                                          TRADINGPOST_BACK,
                                          RANDOM_REQUESTS,
                                          ENTER_GUILD, GUILD_REQUESTS,
                                          GUILD_HANDLE,
                                          GUILD_BACK,
                                          ROAMING,
                                          ENTER_ROAMING,
                                          ROAMING_GO,
                                          ROAMING_OK,
                                          ROAMING_BACK,
                                          ENTER_KITCHEN1,
                                          ENTER_KITCHEN2,
                                          MM_VILLAGE,
                                          ENTER_FISHING,
                                          FISHING_COLLECT_BAIT,
                                          KITCHEN_SERVE,
                                          KITCHEN_BACK,
                                          KITCHEN_ORDER_JEWELS,
                                          SCHOOL_BACK,
                                          SCHOOL_EDUCATE,
                                          MM_HOME,
                                          APP_TITLE,
                                          KITCHEN,
                                          SCHOOL,
                                          ENTER_SCHOOL)


# to start:
# 1. start on any screen with main menu below.
# 2. if trading pot gold is maxed out, clear it first.
# 3. in the village make sure inn and fish are on the screen.
def collect_trading_post_gold(maxtimes=30):
    # Save commonly needed positions.
    click(MM_HOME, confidence=0.6, _click=False, _highlight=HIGHLIGHT)
    # Back button is in same position on different screens
    cloneposition(MM_HOME, 'BACK')
    cloneposition(MM_HOME, 'NOTHING', dx=3)
    click(MM_DRAKENBERG, _click=False, _highlight=HIGHLIGHT)
    # village is to the right of home.
    click(MM_HOME, _derive={'target_image': MM_VILLAGE, 'dx': 1}, _click=False, _highlight=HIGHLIGHT)
    pag.sleep(2)

    for x in range(0, maxtimes):
        if COLLECT_GOLD:
            # assume main menu is displayed.
            # On the left 'Post' is visible, one the right Guil'
            log.info(f'Collecting gold {x}/{maxtimes}...')
            click(MM_DRAKENBERG, _highlight=HIGHLIGHT)
            click(MM_DRAKENBERG_TRADINGPOST, _highlight=HIGHLIGHT)

            # Need higher confidence to match small image(?)
            # Also it may be one of 2 possible images.
            click_list([TRADINGPOST_GOLD1, TRADINGPOST_GOLD2], title=APP_TITLE, confidence=0.48,
                       _highlight=HIGHLIGHT)
            click(TRADINGPOST_BACK, confidence=0.6, _highlight=HIGHLIGHT)
            click(MM_HOME, confidence=0.6, _highlight=HIGHLIGHT)

        # Guild random requests
        # 10 mins to generate a free try. Each gold loop with just gold is 26 seconds. 24 = 10*60/26
        if RANDOM_REQUESTS:
            log.info('Random requests...')
            click(MM_DRAKENBERG, confidence=0.6, _highlight=HIGHLIGHT)
            # scroll_screen('left', 1)
            log_sleep('RANDOM_REQUESTS1', 0.5)
            click(ENTER_GUILD, _highlight=HIGHLIGHT)
            click(GUILD_REQUESTS, _highlight=HIGHLIGHT)
            click(GUILD_HANDLE, _highlight=HIGHLIGHT)
            click(MM_DRAKENBERG, _highlight=HIGHLIGHT)
            click(GUILD_BACK, confidence=0.85, _highlight=HIGHLIGHT)

        # Roam if possible. Free try every 9 mins. 21 = 9*60/26
        if ROAMING:
            # scroll_screen('right', 1)
            pag.sleep(1)
            click(ENTER_ROAMING, _highlight=HIGHLIGHT)
            # Give time for screen to refresh
            log_sleep('ROAMING', 0.5)
            click(ROAMING_GO, _highlight=HIGHLIGHT)
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
                click(ROAMING_GO, _highlight=HIGHLIGHT)
                # Sometimes when we roam we get a dialog box.
                click(ROAMING_OK, _highlight=HIGHLIGHT, match_optional=True)

            # Click on back to continue
            click(ROAMING_BACK, _highlight=HIGHLIGHT)

        # serve in inn. Free try every 20 mins. 47 = 20*60/26
        # if ENTER_KITCHEN and (x % 47 == 0):
        if KITCHEN:
            log.info('Enter village...')
            # Enter village
            log_sleep('Village', 1)
            click(MM_VILLAGE, confidence=0.45, _highlight=HIGHLIGHT)

            # serve in inn. Free try every 20 mins. 47 = 20*60/26
            # if ENTER_KITCHEN and (x % 47 == 0):
            if SCHOOL:
                log.info('Enter school...')
                click(ENTER_SCHOOL, _highlight=HIGHLIGHT)

                click(SCHOOL_BACK, _highlight=HIGHLIGHT, _click=False, confidence=0.7)
                # Students are 1 row above the back button
                cloneposition(SCHOOL_BACK, 'STUDENT1', dx=0, dy=-1)
                cloneposition('STUDENT1', 'STUDENT2', dx=1, dy=0)
                cloneposition('STUDENT1', 'STUDENT3', dx=2, dy=0)
                cloneposition('STUDENT1', 'STUDENT4', dx=3, dy=0)
                cloneposition('STUDENT1', 'STUDENT5', dx=4, dy=0)

                click('STUDENT1')
                click(SCHOOL_EDUCATE)
                pag.sleep(1)
                click('STUDENT2')
                click(SCHOOL_EDUCATE)
                pag.sleep(1)
                click('STUDENT3')
                click(SCHOOL_EDUCATE)
                pag.sleep(1)
                click('STUDENT4')
                click(SCHOOL_EDUCATE)
                pag.sleep(1)
                click('STUDENT5')
                click(SCHOOL_EDUCATE)
                pag.sleep(1)

            # Collect fishing bait
            log.info('Collect bait...')
            click(ENTER_FISHING, _highlight=HIGHLIGHT)
            click(FISHING_COLLECT_BAIT, _highlight=HIGHLIGHT)
            # Dismiss any popup
            click('NOTHING', _highlight=HIGHLIGHT)

            click('BACK', _highlight=HIGHLIGHT)

            # Enter kitchen
            log.info('Enter Inn...')
            log_sleep('KITCHEN', 1)
            click_list([ENTER_KITCHEN1, ENTER_KITCHEN2], title=APP_TITLE, confidence=0.48,
                       _highlight=HIGHLIGHT)
            # Press serve button.
            click(KITCHEN_SERVE, _highlight=HIGHLIGHT)
            # calc where to click to dismiss dialog.
            click(KITCHEN_SERVE, _highlight=HIGHLIGHT, _derive={'target_image': 'empty area', 'dx': -1},
                  _click=True)
            # If success, click next to serve again to dismiss.
            # If failed, click next to click serve again to dismiss error.
            # click('empty area', _highlight=HIGHLIGHT)
            click('empty area', _highlight=HIGHLIGHT)

            # clear jewels
            pag.sleep(7)
            click(KITCHEN_ORDER_JEWELS, _highlight=HIGHLIGHT)
            click(KITCHEN_BACK, _highlight=HIGHLIGHT)

            # Back out of inn
            # click(KITCHEN_BACK, _highlight=HIGHLIGHT)

        # give time for gold to replenish
        log_sleep('LAST_LOOP', 7)

    elapsed = time.time() - start
    log.info(f'Time taken = {str(timedelta(seconds=elapsed))}')


# Select the function based on the user input
while True:
    # Get the user input
    # number = int(
    #     input("Select a function (0 roam, 1 Gold, 2 Stage, 3 guild, 4 move right, 5 grind, 6 kitchen, 7 school): "))
    collect_trading_post_gold(3000)
    exit()
