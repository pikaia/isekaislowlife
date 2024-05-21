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
from slowlife.resources.constants import (COLLECT_GOLD,
                                          MM_DRAKENBERG_TRADINGPOST,
                                          TRADINGPOST_GOLD1,
                                          TRADINGPOST_GOLD2,
                                          RANDOM_REQUESTS,
                                          ENTER_GUILD, GUILD_REQUESTS,
                                          GUILD_HANDLE,
                                          ROAMING,
                                          ENTER_ROAMING,
                                          ROAMING_GO,
                                          ROAMING_OK,
                                          ENTER_KITCHEN1,
                                          ENTER_KITCHEN2,
                                          MM_VILLAGE,
                                          ENTER_FISHING,
                                          FISHING_COLLECT_BAIT,
                                          KITCHEN_SERVE,
                                          KITCHEN_ORDER_JEWELS,
                                          SCHOOL_BACK,
                                          SCHOOL_EDUCATE,
                                          MM_HOME,
                                          APP_TITLE,
                                          KITCHEN,
                                          SCHOOL,
                                          ENTER_SCHOOL,
                                          STAGE,
                                          MM_STAGE,
                                          STAGE_FULLAUTO,
                                          STAGE_START,
                                          FOUNTAIN, MM_FOUNTAIN, FOUNTAIN_1,
                                          FARMSTEAD,
                                          BANQUET, ENTER_BANQUET, ATTEND, ATTEND_PARTY, TAKE_SIT,
                                          DONATE, ENTER_DONATION, BASIC_DONATION, DONATED)


# to start:
# 1. start on any screen with main menu below.
# 2. if trading pot gold is maxed out, clear it first.
# 3. in the village make sure inn and fish are on the screen.
def collect_trading_post_gold(maxtimes=30):
    # Limit donation to 4 times.
    donated_times = 0

    # 1.
    #   click('../resources/mainmenu/village/drakenberg/roaming/skip.png', _highlight=True, _clicks=1)
    #   click('../resources/mainmenu/village/drakenberg/roaming/select.png', _highlight=True, _clicks=1)
    #   empty
    #   back
    # 2.
    #   skip
    #   empty
    #   back
    # Save commonly needed positions.
    click(MM_HOME, confidence=0.6, _clicks=0)
    # Back button is in same position on different screens
    cloneposition(MM_HOME, 'BACK')
    cloneposition(MM_HOME, 'NOTHING', dx=3)
    cloneposition(MM_HOME, 'DRAKENBERG', dx=4)
    # village is to the right of home.
    click(MM_HOME, _derive={'target_image': MM_VILLAGE, 'dx': 1}, _clicks=0)
    pag.sleep(2)

    for x in range(0, maxtimes):
        if COLLECT_GOLD:
            # assume main menu is displayed.
            # On the left 'Post' is visible, one the right Guil'
            log.info(f'Collecting gold {x}/{maxtimes}...')
            click('DRAKENBERG')
            click(MM_DRAKENBERG_TRADINGPOST)

            # Need higher confidence to match small image(?)
            # Also it may be one of 2 possible images.
            click_list([TRADINGPOST_GOLD1, TRADINGPOST_GOLD2], title=APP_TITLE, confidence=0.48)
            click('BACK')

        # Check for Banquets.
        if BANQUET:
            log_sleep('Pause for banquet to be visible', 1)
            click(ENTER_BANQUET)
            click(ATTEND, confidence=0.6)
            if click(ATTEND_PARTY, confidence=0.6, match_optional=True) is None:
                # Dismiss dialogue
                click('BACK')
            else:
                click(TAKE_SIT, confidence=0.6)
                click('BACK')
            # Leave Banquet
            click('BACK')

        click(MM_HOME, confidence=0.6)

        # Guild random requests
        # 10 mins to generate a free try. Each gold loop with just gold is 26 seconds. 24 = 10*60/26
        if RANDOM_REQUESTS:
            log.info('Donations and Random requests...')
            click('DRAKENBERG', confidence=0.6)
            # scroll_screen('left', 1)
            log_sleep('RANDOM_REQUESTS1', 0.5)
            click(ENTER_GUILD)

            # Try to donate.
            if DONATE and donated_times < 4:
                click(ENTER_DONATION)
                try:
                    pag.locateOnWindow(image=DONATED, title=APP_TITLE, confidence=0.6, grayscale=True)
                    log.info('Max donations reached. Skip donations.')
                    donated_times = 5
                except pag.ImageNotFoundException as e:
                    log.info('Donations not finished yet.')
                    donated_times += 1

                if donated_times < 4:
                    click(BASIC_DONATION, _derive={'target_image': 'MAKE_BASIC_DONATION', 'dx': 1})
                    # dismiss congratulation screen
                    click('MAKE_BASIC_DONATION')

            # Exit donation screen
            click('BACK')
            pag.sleep(1)

            click(GUILD_REQUESTS)
            click(GUILD_HANDLE)
            click('DRAKENBERG')
            click('BACK')

        # Roam if possible. Free try every 9 mins. 21 = 9*60/26
        if ROAMING:
            # scroll_screen('right', 1)
            pag.sleep(1)
            click(ENTER_ROAMING)
            # Give time for screen to refresh
            log_sleep('ROAMING', 0.5)
            click(ROAMING_GO)
            log_sleep('ROAMING', 1)

            # roaming has outcomes when u click on GO
            # 1. roaming not available: go -> error dialogue -> click go again to dismiss -> back
            # 2. roaming available:     go -> ok dialogue -> click ok -> back
            # click('../resources/mainmenu/village/drakenberg/roaming/select.png', _clicks=0)
            try:
                roaming_ok = pag.locateOnWindow(ROAMING_OK, APP_TITLE, grayscale=True, confidence=0.9)
                pag.click(roaming_ok)
            except ImageNotFoundException as e:
                # When this is no roaming available, a dialog appears
                # click anywhere to dismiss it.
                click(ROAMING_GO)
                # Sometimes when we roam we get a dialog box.
                click(ROAMING_OK, match_optional=True)

            # Click on back to continue
            click('BACK')
            pag.sleep(1)

        # serve in inn. Free try every 20 mins. 47 = 20*60/26
        # if ENTER_KITCHEN and (x % 47 == 0):
        if KITCHEN:
            log.info('Enter village...')
            # Enter village
            log_sleep('Village', 1)
            click(MM_VILLAGE, confidence=0.45)

            # Get some gold from Farmstead
            click(FARMSTEAD, confidence=0.45, _clicks=20)

            # serve in inn. Free try every 20 mins. 47 = 20*60/26
            # if ENTER_KITCHEN and (x % 47 == 0):
            if SCHOOL:
                log.info('Enter school...')
                click(ENTER_SCHOOL)

                click('BACK')
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
            click(ENTER_FISHING)
            click(FISHING_COLLECT_BAIT)
            # Dismiss any popup
            click('NOTHING')

            click('BACK')

            # Enter kitchen
            log.info('Enter Inn...')
            log_sleep('KITCHEN', 1)
            click_list([ENTER_KITCHEN1, ENTER_KITCHEN2], title=APP_TITLE, confidence=0.48)
            # Press serve button.
            click(KITCHEN_SERVE)
            # calc where to click to dismiss dialog.
            click(KITCHEN_SERVE, _derive={'target_image': 'empty area', 'dx': -1}, _clicks=1)
            # If success, click next to serve again to dismiss.
            # If failed, click next to click serve again to dismiss error.
            # click('empty area')
            click('empty area')

            # clear jewels
            pag.sleep(7)
            click(KITCHEN_ORDER_JEWELS)
            click('BACK')

            # Back out of inn
            # click(KITCHEN_BACK)
        # give time for staging to run and gold to accumulate
        pag.sleep(3)
        click(MM_HOME, _clicks=2, _pause=2)
        pag.sleep(4)

        if FOUNTAIN:
            # Fountain
            # Home screen has sight delay.
            click(MM_FOUNTAIN, _pause=2)
            # click(FOUNTAIN_10)
            # click(MM_FOUNTAIN, confidence=0.6)
            # click(FOUNTAIN_10, confidence=0.6)
            # Back is located in same spot on most screens
            # click('BACK')
            click(FOUNTAIN_1)
            # Back is located in same spot on most screens.
            # Second click to leave fountain
            click('BACK', _clicks=2, _pause=1)

        if STAGE and (x + 1) % 10 == 0:
            log.info('Run stages...')
            # Enter village
            click(MM_STAGE)
            click(STAGE_FULLAUTO)
            click(STAGE_START)
            # Click to the fight of full auto to cancel.
            # give time for staging to run and gold to accumulate
            log.info('Wait 10 seconds for stage to run...')
            pag.sleep(10)
            click(STAGE_FULLAUTO, _derive={'target_image': 'CANCEL_STAGE', 'dx': 1})
            click('CANCEL_STAGE')

    elapsed = time.time() - start
    log.info(f'Time taken = {str(timedelta(seconds=elapsed))}')


# Select the function based on the user input
while True:
    # Get the user input
    # number = int(
    #     input("Select a function (0 roam, 1 Gold, 2 Stage, 3 guild, 4 move right, 5 grind, 6 kitchen, 7 school): "))
    collect_trading_post_gold(3000)
    exit()
