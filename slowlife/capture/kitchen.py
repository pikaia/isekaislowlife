import pyautogui as pag
import pygetwindow as paw

from slowlife.common.utils import log, click, elapsed_time
from slowlife.resources.constants import CAPTURE_FULL_APP, CAPTURE_MINI_APP, \
    CAPTURE_KITCHEN_FOLDER, APP_TITLE, KITCHEN_STATIONS

# highlight the matches on screen is slow. 2 mins vs 38s without.
HIGHLIGHT = True

# Get the coordinates of the window
app = paw.getWindowsWithTitle(APP_TITLE)[0]

# Whole app window
screenshot = pag.screenshot(region=(app.left, app.top, app.width, app.height), imageFilename=CAPTURE_FULL_APP)

# Minus caption on top and bottom
mini_region = (app.left + 50, app.top + 200, app.width - 100, app.bottom - app.top - 70 - 300)
mini_screenshot = pag.screenshot(region=mini_region, imageFilename=CAPTURE_MINI_APP)
log.info(f'Saved mini screenshot to {CAPTURE_MINI_APP}...')

# Assume we start with Inn having focus.
for bldg in KITCHEN_STATIONS:
    # Capture kitchen summary (earnings rate, employee count, hiring cost, earnings rate, operating fellows, level
    # Save each kitchen in resources/ss/data/generated/kitchens
    pag.screenshot(region=mini_region,
                   imageFilename=f'{CAPTURE_KITCHEN_FOLDER}/{bldg}.png'.replace(' ', '_'))

    # Click on arrow to go to next kitchens in the middle of the right edge
    pag.click(x=mini_region[0] + mini_region[2], y=mini_region[1] + mini_region[3] / 2)
    pag.sleep(1)

elapsed_time('Kitchen Stations', KITCHEN_STATIONS)
