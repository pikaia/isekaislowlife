import time
from datetime import timedelta

import pyautogui as pag
import pygetwindow as paw

from slowlife.common.utils import log, click
from slowlife.resources.constants import CAPTURE_FULL_APP, CAPTURE_MINI_APP, SOURCE_BUILDING_EARNINGS, \
    SOURCE_BUILDING_NEXT, CAPTURE_BUILDING_FOLDER, APP_TITLE, BUILDINGS

# highlight the matches on screen is slow. 2 mins vs 38s without.
HIGHLIGHT = False

# Get the coordinates of the window
app = paw.getWindowsWithTitle(APP_TITLE)[0]

# Whole app window
screenshot = pag.screenshot(region=(app.left, app.top, app.width, app.height), imageFilename=CAPTURE_FULL_APP)

# Minus caption on top and bottom
mini_region = (app.left, app.top + 60, app.right - app.left, app.bottom - app.top - 70 - 60)
mini_screenshot = pag.screenshot(region=mini_region, imageFilename=CAPTURE_MINI_APP)

# Assume we start with Inn having focus.
start = time.time()
for bldg in BUILDINGS:
    # Capture building summary (earnings rate, employee count, hiring cost, earnings rate, operating fellows, level
    # Save each building in resources/ss/data/generated/buildings
    pag.screenshot(region=mini_region,
                   imageFilename=f'{CAPTURE_BUILDING_FOLDER}/{bldg}_operation.png'.replace(' ', '_'))

    # Display earnings breakout
    click(SOURCE_BUILDING_EARNINGS, _confidence=0.7, _highlight=HIGHLIGHT)
    # Save each buildings in resources/ss/data/generated/buildings
    pag.screenshot(region=mini_region, imageFilename=f'{CAPTURE_BUILDING_FOLDER}/{bldg}.png'.replace(' ', '_'))
    # Dismiss screen
    pag.click(app.right - 10, app.bottom - app.top - 70 - 60 - 10)
    # Click on arrow to go to next buildings
    click(SOURCE_BUILDING_NEXT, _confidence=0.7, _highlight=HIGHLIGHT)

elapsed = time.time() - start
log.info(f'# buildings = {len(BUILDINGS)}. Time taken = {str(timedelta(seconds=elapsed))}')
