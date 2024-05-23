import time
from datetime import timedelta

import pyautogui as pag

from slowlife.common.utils import (log,
                                   click,
                                   log_sleep,
                                   start,
                                   cloneposition,
                                   click_list)

from slowlife.resources.constants import (APP_TITLE,

                                          COLLECT_GOLD, BANQUET, ROAMING, FOUNTAIN, KITCHEN, SCHOOL, DONATE, STAGE,

                                          MM_HOME, MM_VILLAGE, MM_STAGE, MM_DRAKENBERG,

                                          HOME_FOUNTAIN,

                                          VILLAGE_KITCHEN1, VILLAGE_KITCHEN2, VILLAGE_FISHING, VILLAGE_FARMSTEAD,
                                          VILLAGE_SCHOOL,

                                          DRAKENBERG_TRADINGPOST, DRAKENBERG_GUILD, DRAKENBERG_ROAMING,
                                          DRAKENBERG_BANQUET,

                                          TRADINGPOST_GOLD1, TRADINGPOST_GOLD2,

                                          GUILD_REQUESTS, GUILD_HANDLE,

                                          RANDOM_REQUESTS,

                                          ROAMING_GO, ROAMING_OK, ROAMING_USE, ROAMING_NO_STAMINA,

                                          STAGE_FULLAUTO, STAGE_START,

                                          FISHING_COLLECT_BAIT,

                                          FOUNTAIN_1,

                                          KITCHEN_SERVE, KITCHEN_ORDER_JEWELS,

                                          SCHOOL_BACK, SCHOOL_EDUCATE,

                                          BANQUET_ATTEND, BANQUET_ATTEND_PARTY, BANQUET_TAKE_SIT,

                                          GUILD_DONATION, DONATION_BASIC_DONATION, DONATION_DONATED, BANQUET_MONEY_FULL
                                          )


# to start:
# 1. start on any screen with main menu below.
# 2. if trading pot gold is maxed out, clear it first.
# 3. in the village make sure inn and fish are on the screen.
def collect_trading_post_gold(maxtimes=30):
    # Limit donation to 4 times.
    donations_done: bool = False

    # Limit banquet to 4 times.
    banquet_done: bool = False

    # Save fixed positions.
    click(MM_HOME, confidence=0.6, _clicks=0, _highlight=True)

    # Back button is in same position on different screens
    cloneposition(MM_HOME, 'BACK', _highlight=True)
    cloneposition(MM_HOME, MM_VILLAGE, dx=1, _highlight=True)
    cloneposition(MM_HOME, 'NOTHING', dx=3, _highlight=True)
    cloneposition(MM_HOME, MM_STAGE, dx=3, _highlight=True)
    cloneposition(MM_HOME, MM_DRAKENBERG, dx=4, _highlight=False)

    # Register other Drakenberg locations
    click(MM_DRAKENBERG, _highlight=True)
    click(DRAKENBERG_TRADINGPOST, confidence=0.6, _clicks=0, _highlight=True)
    click(DRAKENBERG_BANQUET, _clicks=0, _highlight=True)
    click(DRAKENBERG_ROAMING, _clicks=0, _highlight=True)
    click(DRAKENBERG_GUILD, _clicks=0, _highlight=True)

    for x in range(0, maxtimes):
        do_collect_gold(maxtimes, x)

        # Check for Banquets.
        if BANQUET: banquet_done = do_banquet(banquet_done)

        click(MM_HOME)

        click(MM_DRAKENBERG)

        donations_done = do_guild(donations_done)

        # Roam if possible. Free try every 9 mins. 21 = 9*60/26
        do_roaming()

        # serve in inn. Free try every 20 mins. 47 = 20*60/26
        # if ENTER_KITCHEN and (x % 47 == 0):
        if KITCHEN:
            do_farmstead()

            # serve in inn. Free try every 20 mins. 47 = 20*60/26
            # if ENTER_KITCHEN and (x % 47 == 0):
            do_school()

            do_collect_bait()

            # Back out of inn
            # click(KITCHEN_BACK)
        # give time for staging to run and gold to accumulate
        pag.sleep(3)
        click(MM_HOME, _clicks=2, _pause=2)
        pag.sleep(4)

        do_fountain()

        do_stage(x)

    elapsed = time.time() - start
    log.info(f'Time taken = {str(timedelta(seconds=elapsed))}')


# We must be in Drakenberg with Trading Post visible.
def do_collect_gold(maxtimes, x):
    if COLLECT_GOLD:
        # assume main menu is displayed.
        # On the left 'Post' is visible, one the right 'Guild'
        log.info(f'Collecting gold {x}/{maxtimes}...')
        click(MM_DRAKENBERG)
        click(DRAKENBERG_TRADINGPOST)

        # Need higher confidence to match small image(?)
        # Also it may be one of 2 possible images.
        click_list([TRADINGPOST_GOLD1, TRADINGPOST_GOLD2], title=APP_TITLE, confidence=0.48)
        click('BACK')


# We must be on the main page with village button below.
def do_farmstead():
    log.info('Enter village...')
    # Enter village
    log_sleep('Village', 1)
    click(MM_VILLAGE, confidence=0.45)
    # Get some gold from Farmstead
    click(VILLAGE_FARMSTEAD, confidence=0.45, _clicks=20)


# We must be in Drakenberg
def do_roaming():
    if ROAMING:
        pag.sleep(1)
        click(DRAKENBERG_ROAMING)
        # Give time for screen to refresh
        log_sleep('ROAMING', 0.5)
        click(ROAMING_GO)
        log_sleep('ROAMING', 1)

        # roaming has outcomes when u click on GO
        # 1. roaming not available: go -> No stamina -> click go again to dismiss -> back to go
        # 2. roaming available:     go -> ok dialogue -> click ok -> back
        # click('../resources/mainmenu/village/drakenberg/roaming/select.png', _clicks=0)
        try:
            pag.locateOnWindow(ROAMING_NO_STAMINA, APP_TITLE)
            # When this is no roaming available, a dialog appears
            # click anywhere (e.g. GO) to dismiss it.
            click(ROAMING_GO)
        except pag.ImageNotFoundException:
            log.info('No stamina dialogue not found. Checking for Roaming OK.')
            pag.sleep(1)
            try:
                roaming_ok = pag.locateOnWindow(ROAMING_OK, APP_TITLE, grayscale=True, confidence=0.9)
                pag.click(roaming_ok)
            except pag.ImageNotFoundException:
                log.info('Roaming ok button not found. Check for use button.')
                pag.sleep(1)
                try:
                    roaming_use = pag.locateOnWindow(ROAMING_USE, APP_TITLE, grayscale=True, confidence=0.9)
                    pag.click(roaming_use)
                except pag.ImageNotFoundException:
                    log.error('Unexpected path not currently supported')
                    raise NotImplementedError('Unexpected popup. Needs to handle this case.')

        # Click on back to continue
        pag.sleep(1)
        click('BACK')
        pag.sleep(1)


# We must be in Drakenberg
def do_guild(donations_done: bool) -> bool:
    # 10 mins to generate a free try. Each gold loop with just gold is 26 seconds. 24 = 10*60/26
    if RANDOM_REQUESTS:
        log.info('Donations and Random requests...')
        # scroll_screen('left', 1)

        # Try to donate.
        if DONATE and not donations_done:
            log_sleep('RANDOM_REQUESTS1', 0.5)
            click(DRAKENBERG_GUILD)
            click(GUILD_DONATION)
            try:
                pag.locateOnWindow(image=DONATION_DONATED, title=APP_TITLE, confidence=0.6, grayscale=True)
                donations_done = True
                log.info('Max donations reached. Skip donations.')
            except pag.ImageNotFoundException:
                log.info('Donations not finished yet.')
                donations_done = False

            click(DONATION_BASIC_DONATION, _derive={'target_image': 'MAKE_BASIC_DONATION', 'dx': 1})
            # dismiss congratulation screen
            click('MAKE_BASIC_DONATION')

            # Exit donation screen
            click('BACK')
            pag.sleep(1)

            click(GUILD_REQUESTS)
            click(GUILD_HANDLE)
            click(MM_DRAKENBERG)
            click('BACK')

            return donations_done


# We must be in village
def do_school():
    if SCHOOL:
        log.info('Enter school...')
        click(VILLAGE_SCHOOL)

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


# We must be in village
def do_collect_bait():
    # Collect fishing bait
    log.info('Collect bait...')
    click(VILLAGE_FISHING)
    click(FISHING_COLLECT_BAIT)
    # Dismiss any popup
    click('NOTHING')
    click('BACK')
    # Enter kitchen
    log.info('Enter Inn...')
    log_sleep('KITCHEN', 1)
    click_list([VILLAGE_KITCHEN1, VILLAGE_KITCHEN2], title=APP_TITLE, confidence=0.48)
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


# We must be in Drakenberg
def do_banquet(banquet_done: bool) -> bool:
    if not banquet_done:
        log_sleep('Pause for banquet to be visible', 1)
        click(DRAKENBERG_BANQUET)
        click(BANQUET_ATTEND, confidence=0.6)
        banquet_attend_party = click(BANQUET_ATTEND_PARTY, confidence=0.7, match_optional=True)
        if banquet_attend_party is None:
            # Dismiss dialogue
            click('BACK')
            banquet_done = False
        else:
            # click twice. money gifts full will pop up.
            pag.sleep(0.5)
            click(BANQUET_TAKE_SIT, confidence=0.6, _clicks=2)
            try:
                banquet_money_full = pag.locateOnWindow(BANQUET_MONEY_FULL, APP_TITLE, confidence=0.9)
                banquet_done = True
            except pag.ImageNotFoundException:
                log.info('Choose a gift dialogue not found. It implies we are able to seat and thus not done yet.')
                banquet_done = False
            click('BACK')
        # Leave Banquet
        click('BACK')
    return banquet_done


# We must be in Home
def do_fountain():
    if FOUNTAIN:
        # Fountain
        # Home screen has sight delay.
        click(HOME_FOUNTAIN, _pause=2)
        # click(FOUNTAIN_10)
        # click(MM_FOUNTAIN, confidence=0.6)
        # click(FOUNTAIN_10, confidence=0.6)
        # Back is located in same spot on most screens
        # click('BACK')
        click(FOUNTAIN_1)
        # Back is located in same spot on most screens.
        # Second click to leave fountain
        click('BACK', _clicks=2, _pause=1)


# Main menu must be visible at bottom of screen
def do_stage(x):
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


# Select the function based on the user input
while True:
    # Get the user input
    # number = int(
    #     input("Select a function (0 roam, 1 Gold, 2 Stage, 3 guild, 4 move right, 5 grind, 6 kitchen, 7 school): "))
    collect_trading_post_gold(3000)
    exit()
