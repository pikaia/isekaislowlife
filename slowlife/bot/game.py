import time
from datetime import timedelta

import pyautogui as pag

from slowlife.common.utils import (log,
                                   click,
                                   log_sleep,
                                   start,
                                   cloneposition,
                                   click_list,
                                   add_loc, choose_path, highlight, displayed, locate_all_on_window)

from slowlife.resources.constants import (APP_TITLE,

                                          COLLECT_GOLD, BANQUET, ROAMING, FOUNTAIN, KITCHEN, SCHOOL, DONATE, STAGE,
                                          AUTO_GRADUATE,

                                          MM_HOME, MM_VILLAGE, MM_STAGE, MM_DRAKENBERG,

                                          HOME_FOUNTAIN,

                                          VILLAGE_KITCHEN1, VILLAGE_KITCHEN2, VILLAGE_FISHING, VILLAGE_FARMSTEAD,
                                          VILLAGE_SCHOOL,

                                          DRAKENBERG_TRADINGPOST, DRAKENBERG_GUILD, DRAKENBERG_ROAMING,
                                          DRAKENBERG_BANQUET, BANQUET_NONE_HOSTED, BANQUET_ALREADY_ATTENDED,

                                          TRADINGPOST_GOLD1, TRADINGPOST_GOLD2,

                                          GUILD_REQUESTS, GUILD_HANDLE,

                                          RANDOM_REQUESTS,

                                          ROAMING_GO, ROAMING_OK, ROAMING_USE, ROAMING_NO_STAMINA,

                                          STAGE_FULLAUTO, STAGE_START,

                                          FISHING_COLLECT_BAIT,

                                          FOUNTAIN_1,

                                          KITCHEN_SERVE, KITCHEN_ORDER_JEWELS1, KITCHEN_ORDER_JEWELS2,
                                          KITCHEN_USE_INN_PAMPHLET,

                                          SCHOOL_BACK, SCHOOL_EDUCATE, SCHOOL_USE_ITEM,
                                          SCHOOL_GRADUATE, GRADUATE_OK, GRADUATE_CONGRATS_OK, GRADUATE_FORM_UNION,

                                          BANQUET_ATTEND, BANQUET_ATTEND_PARTY, BANQUET_TAKE_SEAT,

                                          GUILD_DONATION, DONATION_BASIC_DONATION, DONATION_DONATED, BANQUET_MONEY_FULL,
                                          DONATION_OPENED, DONATION_CLOSED,

                                          ROAMING_SKIP, ROAMING_TREAT, VILLAGE_GARDEN2, VILLAGE_GARDEN1,

                                          GARDEN_QUICK_HARVEST, GARDEN_QUICK_SOW, GARDEN_CHEST, GARDEN_ORDERS_FILLED,
                                          GARDEN_CAVE,

                                          ORDERS_DELIVER, ORDERS_LEVEL, GARDEN_ASSIGN, GARDEN_QUICK_ASSIGN,
                                          GARDEN_CONFIRM, ROAMING_ANNE_SKIP, ROAMING_ANNE, TAP_TO_CONTINUE,
                                          ROAMING_BACK, ROAMING_SUSIE, SELECT_SADAKO, SUSIE_TAP_TO_CONTINUE,
                                          ROAMING_REIR, REIR_NO_THANKS, PLANT_ORDER_NOTICE, GARDEN_ORDER, HOME_FAMILY,
                                          FAMILY_AUTO_DATE, FAMILY_GO_EDUCATE, SCHOOL_NAME, NAME_OK, SCHOOL_GO,
                                          SCHOOL_OK, BANQUET_HAS_ENDED, OUT_OF_EDUCATION_POINTS
                                          )

# Limit donation to 4 times.
donations_done: bool = False

# Limit banquet to 4 times.
banquet_done: bool = False

# Limit banquet to 4 times.
school_initialized: bool = False


# to start:
# 1. start on any screen with main menu below.
# 2. if trading pot gold is maxed out, clear it first.
# 3. in the village make sure inn and fish are on the screen.
def collect_trading_post_gold(maxtimes: int = 30):
    register_locations()

    for x in range(0, maxtimes):
        do_collect_gold(maxtimes, x)

        # Check for Banquets.
        if BANQUET: do_banquet()

        click(MM_HOME)

        click(MM_DRAKENBERG)

        do_guild()

        # Roam if possible. Free try every 9 mins. 21 = 9*60/26
        do_roaming()

        # serve in inn. Free try every 20 mins. 47 = 20*60/26
        # if ENTER_KITCHEN and (x % 47 == 0):
        if KITCHEN:
            do_farmstead()

            do_magic_farm()

            # serve in inn. Free try every 20 mins. 47 = 20*60/26
            # if ENTER_KITCHEN and (x % 47 == 0):
            do_school()

            do_collect_bait()

            do_kitchen()

        # give time for staging to run and gold to accumulate
        pag.sleep(3)
        click(MM_HOME, _clicks=2, _pause=2)
        pag.sleep(4)

        do_fountain()

        do_stage(x)

    elapsed = time.time() - start
    log.info(f'Time taken = {str(timedelta(seconds=elapsed))}')


def register_locations():
    # Save fixed positions.
    click(MM_HOME, confidence=0.6, _clicks=0, _highlight=False)
    # Back button is in same position on different screens
    cloneposition(MM_HOME, 'BACK', _highlight=False)
    cloneposition(MM_HOME, MM_VILLAGE, dx=1, _highlight=False)
    cloneposition(MM_HOME, 'NOTHING', dx=3, _highlight=False)
    cloneposition(MM_HOME, MM_STAGE, dx=3, _highlight=False)
    cloneposition(MM_HOME, MM_DRAKENBERG, dx=4, _highlight=False)
    # Register other Drakenberg locations
    click(MM_DRAKENBERG, _highlight=False)
    click(DRAKENBERG_TRADINGPOST, confidence=0.6, _clicks=0, _highlight=False)
    click(DRAKENBERG_BANQUET, _clicks=0, _highlight=False)
    click(DRAKENBERG_ROAMING, _clicks=0, _highlight=False)
    click(DRAKENBERG_GUILD, _clicks=0, _highlight=False)


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
    log_sleep(MM_VILLAGE, 1)
    click(MM_VILLAGE, confidence=0.45)
    # Get some gold from Farmstead
    click(VILLAGE_FARMSTEAD, confidence=0.45, _clicks=50, _interval=0.1)


def do_magic_farm() -> None:
    # magic garden
    click_list([VILLAGE_GARDEN1, VILLAGE_GARDEN2])
    try:
        quick_harvest = pag.locateOnWindow(GARDEN_QUICK_HARVEST, APP_TITLE, grayscale=True, confidence=0.8)
        pag.click(quick_harvest)
        pag.sleep(1)

        # Ignore notice
        if displayed(PLANT_ORDER_NOTICE):
            # Need high confidence to identify right image.
            click(GARDEN_ORDER, confidence=0.95, _highlight=True)

        # Click on all deliver buttons. This requires 2 checks.
        # 1. Click all visible deliver buttons.
        done = 'ok'
        while done is None:
            try:
                # connect
                deliver = pag.locateOnWindow(ORDERS_DELIVER, APP_TITLE, grayscale=True, confidence=0.8)

                log.warn('Delivered order')
                pag.click(deliver)
                pag.click(deliver)
                pag.sleep(1)
            except pag.ImageNotFoundException:
                break

        # 2. Check the last order below. Drag screeen up a little.
        orders_level = pag.locateOnWindow(ORDERS_LEVEL, APP_TITLE, grayscale=True, confidence=0.8)
        x, y = pag.center(orders_level)
        pag.mouseDown(x, y)
        pag.moveTo(x, y - 100, duration=0.5)
        pag.mouseUp()

        try:
            deliver = pag.locateOnWindow(ORDERS_DELIVER, APP_TITLE, grayscale=True, confidence=0.8)
            log.warn('Delivered order')
            pag.click(deliver)
            pag.click(deliver)
            pag.sleep(1)
        except pag.ImageNotFoundException:
            # Return to village
            click('BACK')
            return

        # Handle caves.
        while displayed(GARDEN_CAVE):
            log.info('Quick assign a cave')
            click(GARDEN_CAVE)
            click(GARDEN_ASSIGN, confidence=0.8)
            click(GARDEN_QUICK_ASSIGN, confidence=0.8)
            click(GARDEN_CONFIRM, confidence=0.8)
            click('DISMISS')

        # Handle chests.
        while displayed(GARDEN_CHEST, confidence=0.8):
            log.info('Clear a chest')
            click(GARDEN_CHEST, confidence=0.8)
            click(GARDEN_ASSIGN, confidence=0.8)
            click(GARDEN_QUICK_ASSIGN, confidence=0.8)
            click(GARDEN_CONFIRM, confidence=0.8)
            click('DISMISS')

        try:
            garden_quick_sow = pag.locateOnWindow(GARDEN_QUICK_SOW, APP_TITLE, grayscale=True, confidence=0.8)
            log.warning('Sowing...')
            pag.click(garden_quick_sow)
        except pag.ImageNotFoundException:
            # no harvest available. exit.
            log.warning('No sowing needed. Skipping')
            # Return to village
            click('BACK')
            return

        click(GARDEN_ORDERS_FILLED)

    except pag.ImageNotFoundException:
        log.info('No plants to harvest. Skipping.')

    # Return to village
    click('BACK')


# We must be in Drakenberg
def do_roaming():
    if ROAMING:
        pag.sleep(1)
        click(DRAKENBERG_ROAMING)
        # Give time for screen to refresh
        log_sleep(DRAKENBERG_ROAMING, 0.5)
        click(ROAMING_GO)
        log_sleep(DRAKENBERG_ROAMING, 1)

        # roaming has outcomes when u click on GO
        # 1. roaming not available: go -> No stamina -> click go again to dismiss -> back to go
        # 2. roaming available:     go -> ok dialogue -> click ok -> back
        # click('../resources/mainmenu/village/drakenberg/roaming/select.png', _clicks=0)

        # choose_path(test_image1=ROAMING_NO_STAMINA, image_ok_click1=ROAMING_GO, imageok_click1='BACK')

        try:
            pag.locateOnWindow(ROAMING_NO_STAMINA, APP_TITLE, grayscale=True, confidence=0.9)
            log.warning('No stamina available. Skipping.')
            # When this is no roaming available, a dialog appears
            # click anywhere (e.g. GO) to dismiss it.
            click(ROAMING_GO)
            # Click on back to continue
            pag.sleep(1)
            click('BACK')
            pag.sleep(1)
            return
        except pag.ImageNotFoundException:
            log.info('No stamina dialogue not found. Checking for Roaming OK.')
            pag.sleep(1)

        # choose_path(test_image1=ROAMING_OK, ROAMING_OK, 'BACK')

        # Anne.
        if displayed(ROAMING_ANNE, confidence=0.8):
            click(ROAMING_ANNE_SKIP, confidence=0.9)
            click(TAP_TO_CONTINUE, confidence=0.9)
            click(ROAMING_BACK, confidence=0.8)
            return

        # susie
        if displayed(ROAMING_SUSIE, confidence=0.8):
            click(ROAMING_ANNE_SKIP, confidence=0.9)
            click(SELECT_SADAKO)
            click(ROAMING_TREAT, confidence=0.8)
            click(ROAMING_ANNE_SKIP, confidence=0.9)
            click(SUSIE_TAP_TO_CONTINUE, confidence=0.9)
            click(ROAMING_BACK, confidence=0.8)
            return
        # reir
        if displayed(ROAMING_REIR, confidence=0.8):
            click(ROAMING_ANNE_SKIP, confidence=0.8)
            click(REIR_NO_THANKS, confidence=0.8)
            click(SUSIE_TAP_TO_CONTINUE, confidence=0.9)
            click(ROAMING_BACK, confidence=0.8)
            return

        try:
            roaming_ok = pag.locateOnWindow(ROAMING_OK, APP_TITLE, grayscale=True, confidence=0.9)
            pag.click(roaming_ok)
        except pag.ImageNotFoundException:
            log.info('Roaming ok button not found. Check for use button.')
            pag.sleep(1)
            try:
                roaming_use = pag.locateOnWindow(ROAMING_USE, APP_TITLE, grayscale=True, confidence=0.9)
                log.warning('Using one stamina...')
                pag.click(roaming_use)
            except pag.ImageNotFoundException:
                # Check for cases where we need to select from family
                try:
                    roaming_ok = pag.locateOnWindow(ROAMING_OK, APP_TITLE, grayscale=True, confidence=0.9)
                    pag.click(roaming_ok)
                except pag.ImageNotFoundException:
                    log.info('Roaming ok button not found. Check for skip button.')
                    pag.sleep(1)
                    try:
                        # from Go
                        # choose_family: Always choose Sadako
                        # Treat
                        # Confirm: Click above to dismiss
                        # Congrats: select below to dismiss
                        # Go
                        roaming_skip = pag.locateOnWindow(ROAMING_SKIP, APP_TITLE, grayscale=True, confidence=0.9)
                        pag.click(roaming_skip)
                        click(ROAMING_SELECT)
                        click(ROAMING_TREAT)
                        click(ROAMING_SKIP)
                        click('BACK')
                    except pag.ImageNotFoundException:
                        log.error('Unexpected path not currently supported')
                        raise NotImplementedError('Unexpected popup. Needs to handle this case.')

        # click(ROAMING_SKIP, _clicks=1, _highlight=True)
        # click(ROAMING_SELECT, _clicks=1, _highlight=True)
        # click(ROAMING_TREAT, _clicks=1, _highlight=True)
        # click(ROAMING_SKIP, _clicks=1, _highlight=True)
        # click(BACK, _clicks=1, _highlight=True)

        # Click on back to continue
        pag.sleep(1)
        click('BACK')
        pag.sleep(1)


# We must be in Drakenberg
def do_guild() -> None:
    global donations_done
    if donations_done:
        log.warning('Donations done. Skipping')
        return
    # 10 mins to generate a free try. Each gold loop with just gold is 26 seconds. 24 = 10*60/26
    if RANDOM_REQUESTS:
        log.info('Donations and Random requests...')
        # scroll_screen('left', 1)

        # Try to donate.
        if DONATE:
            log_sleep('RANDOM_REQUESTS1', 0.5)
            click(DRAKENBERG_GUILD)
            click(GUILD_DONATION)
            try:
                pag.locateOnWindow(image=DONATION_DONATED, title=APP_TITLE, confidence=0.6, grayscale=True)
                log.warning('Max donations reached. Skip donations.')
                # Turn off going forward
                donations_done = True
            except pag.ImageNotFoundException:
                log.info('Donations not finished yet.')
            if not donations_done:
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

            return


# We must be in village
def do_school():
    global school_initialized

    if SCHOOL:
        log.info('Enter school...')
        click(VILLAGE_SCHOOL, confidence=0.9)

        # Students are 1 row above the back button
        if not school_initialized:
            click(SCHOOL_BACK, confidence=0.9, _clicks=0)
            cloneposition(SCHOOL_BACK, 'STUDENT1', dx=0, dy=-1)
            cloneposition('STUDENT1', 'STUDENT2', dx=1, dy=0)
            cloneposition('STUDENT1', 'STUDENT3', dx=2, dy=0)
            cloneposition('STUDENT1', 'STUDENT4', dx=3, dy=0)
            cloneposition('STUDENT1', 'STUDENT5', dx=4, dy=0)
            school_initialized = True

        for student in ['STUDENT1', 'STUDENT2', 'STUDENT3', 'STUDENT4', 'STUDENT5']:
            click(student)
            pag.sleep(0.5)

            # TODO pag matches both name and go. dont use until we have a workaround.
            # New student
            if displayed(SCHOOL_GO, confidence=0.8):
                continue
                # click(SCHOOL_GO, confidence=0.8)
                # click(SCHOOL_OK, confidence=0.8)
                # click(HOME_FAMILY)
                # click(FAMILY_AUTO_DATE)
                # click('BACK')
                # click(FAMILY_GO_EDUCATE)
                # pag.sleep(1.5)

            if displayed(SCHOOL_NAME, confidence=0.8):
                continue
                # click(SCHOOL_NAME, confidence=0.8)
                # click(NAME_OK, confidence=0.8)
                # click(SCHOOL_EDUCATE)
                # click('BACK')

            # Skip if student is about to graduate.
            try:
                pag.locateOnWindow(SCHOOL_EDUCATE, APP_TITLE, grayscale=True, confidence=0.7)
                click(SCHOOL_EDUCATE)
                if displayed(OUT_OF_EDUCATION_POINTS):
                    click('BACK')
                    continue
                try:
                    # When use focus candy appear when we click again too soon.
                    # Skip it.
                    pag.locateOnWindow(SCHOOL_USE_ITEM, APP_TITLE, grayscale=True, confidence=0.9)
                    # click anywhere (e.g. GO) to dismiss it.
                    click(SCHOOL_BACK)
                except pag.ImageNotFoundException:
                    log.info('Use accumulated education tokens...')
                    pag.sleep(2)
                pag.sleep(1)
            except pag.ImageNotFoundException:
                # No Educate button found. Must be abt to graduate. Skip student
                log.warning(f'Skip {student}. Leave graduation process to manual intervention.')
                if AUTO_GRADUATE:
                    click(SCHOOL_GRADUATE)
                    click(GRADUATE_OK)
                    click(GRADUATE_CONGRATS_OK)
                continue

        click('BACK')


# We must be in village
def do_collect_bait():
    # Collect fishing bait
    log.info('Collect bait...')
    click(VILLAGE_FISHING)
    click(FISHING_COLLECT_BAIT)
    # Dismiss any popup
    click('NOTHING')
    click('BACK')


def do_kitchen():
    # Enter kitchen
    log.info('Enter Inn...')
    log_sleep('KITCHEN', 1)
    click_list([VILLAGE_KITCHEN1, VILLAGE_KITCHEN2], title=APP_TITLE, confidence=0.48)
    # Press serve button
    click(KITCHEN_SERVE)
    try:
        # Click use to use 1 inn pamphlet
        kitchen_use = pag.locateOnWindow(KITCHEN_USE_INN_PAMPHLET, APP_TITLE, confidence=0.65)
        log.warning('Using 1 inn pamphlet...')
        pag.click(kitchen_use)
    except pag.ImageNotFoundException:
        log.info('Use button not found. It implies no in pamphlets available.')
        # calc where to click to dismiss dialog.
        click(KITCHEN_SERVE, _derive={'target_image': 'empty area', 'dx': -1}, _clicks=1)
        # If success, click next to serve again to dismiss.
        # If failed, click next to click serve again to dismiss error.
        # click('empty area')
        click('empty area')
    # clear jewels
    # pag.sleep(7)
    click_list([KITCHEN_ORDER_JEWELS1, KITCHEN_ORDER_JEWELS2], title=APP_TITLE, confidence=0.9)
    click('BACK')


# We must be in Drakenberg
def do_banquet() -> None:
    global banquet_done
    if banquet_done:
        log.warning('Banquets done. Skipping.')
        return

    log_sleep('Pause for banquet to be visible', 1)
    click(DRAKENBERG_BANQUET)
    click(BANQUET_ATTEND, confidence=0.6)
    cloneposition(BANQUET_ATTEND, 'DISMISS', dx=-1, dy=1)
    pag.sleep(0.5)

    if displayed(image=BANQUET_NONE_HOSTED, confidence=0.9):
        log.warning('No banquets being hosted currently. Skip.')
    else:
        if displayed(image=BANQUET_ALREADY_ATTENDED, confidence=0.95):
            log.warning('No new banquets being hosted currently. Skip.')
        elif displayed(image=BANQUET_HAS_ENDED, confidence=0.8):
            log.warning('Banquet has ended. Skip.')
        else:
            banquet_attend_party = pag.locateOnWindow(BANQUET_ATTEND_PARTY, APP_TITLE, confidence=0.95)
            add_loc(BANQUET_ATTEND_PARTY, banquet_attend_party)
            click(BANQUET_ATTEND_PARTY)
            # click twice. money gifts full will pop up.
            pag.sleep(1)
            click(BANQUET_TAKE_SEAT, confidence=0.65, _clicks=2)
            try:
                pag.locateOnWindow(BANQUET_MONEY_FULL, APP_TITLE, confidence=0.7)
                log.warning('Banquets done. Skip going forward.')
                banquet_done = True
            except pag.ImageNotFoundException:
                log.info('Choose a gift dialogue not found. It implies we are able to seat and thus not done yet.')
                # click anywhere to dismiss
                click(BANQUET_TAKE_SEAT)

    # click anywhere to dismiss none hosted dialogue
    click('DISMISS')
    # Leave Banquet
    click('BACK')


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
# try:
#     donation_opened = locate_all_on_window(DONATION_OPENED, APP_TITLE, confidence=0.9)
#     log.info(donation_opened)
#     highlight('donation_opened', donation_opened)
#     log.warning('No new banquets being hosted currently. Skip.')
#     # click anywhere to dismiss none hosted dialogue
#     click('DISMISS')
#     # Leave Banquet
#     click('BACK')
# except pag.ImageNotFoundException:
#     log.info('No found')

# log.info(displayed(image=BANQUET_ALREADY_ATTENDED, confidence=0.95))
# register_locations()
# while True:
#     do_banquet()


while True:
    # school_go = pag.locateOnWindow(SCHOOL_NAME, APP_TITLE, grayscale=True, confidence=0.83)
    # highlight('school_go', school_go)
    # if displayed(SCHOOL_GO, confidence=0.9):
    #     log.info("school go")
    try:
        # from Go
        collect_trading_post_gold(3000)
        # choose_family: Always choose Sadako
        # Treat
        # Confirm: Click above to dismiss
        # Congrats: select below to dismiss
        # Go
        # Need to isolate individual cases. [Anne] skip -> [congrats] dismiss
        # click(ROAMING_SELECT)
        # click(ROAMING_TREAT)
        # click(ROAMING_SKIP)
    except pag.ImageNotFoundException:
        log.error('Unexpected path not currently supported')
        raise NotImplementedError('Unexpected popup. Needs to handle this case.')

    collect_trading_post_gold(3000)
    exit()
    # try:
    #     banquet_already_attended = pag.locateOnWindow(BANQUET_ALREADY_ATTENDED, APP_TITLE, confidence=0.9)
    #     highlight('banquet_already_attended', banquet_already_attended)
    #     log.warning('No new banquets being hosted currently. Skip.')
    #     # click anywhere to dismiss none hosted dialogue
    #     click('DISMISS')
    #     # Leave Banquet
    #     click('BACK')
    # except pag.ImageNotFoundException:
    #     log.info('No found')
    # log.info('Enter Magic Garden...')
    # log_sleep('KITCHEN', 1)
    # # click_list([VILLAGE_GARDEN1, VILLAGE_GARDEN2], title=APP_TITLE, confidence=0.48, _highlight=True)
    # # click(GARDEN_QUICK_HARVEST)
    # # click(GARDEN_QUICK_SOW)
    # # click('BACK')
    # Graduate
    # click_list([SCHOOL_EDUCATE, SCHOOL_GRADUATE], title=APP_TITLE)
    # click(GRADUATE_OK, _highlight=True)
    # click(GRADUATE_FORM_UNION, _highlight=True, confidence=0.8)
