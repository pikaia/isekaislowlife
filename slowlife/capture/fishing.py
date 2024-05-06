import pyautogui as pag
import pygetwindow as paw

from slowlife.common.utils import log, elapsed_time
from slowlife.resources.constants import CAPTURE_FULL_APP, CAPTURE_MINI_APP, \
    APP_TITLE, FISHES, CAPTURE_FISHES_FOLDER

HIGHLIGHT = True

# Get the coordinates of the window
app = paw.getWindowsWithTitle(APP_TITLE)[0]

# Whole app window
screenshot = pag.screenshot(region=(app.left, app.top, app.width, app.height), imageFilename=CAPTURE_FULL_APP)

# Minus caption on top and bottom
mini_region = (app.left + 50, app.top + 60, app.width - 100, app.bottom - app.top - 120)
mini_screenshot = pag.screenshot(region=mini_region, imageFilename=CAPTURE_MINI_APP)
log.info(f'Saved mini screenshot to {CAPTURE_MINI_APP}...')

from pathlib import Path
Path(CAPTURE_FISHES_FOLDER).mkdir(parents=True, exist_ok=True)

# Assume we start with Axolotl having focus.
for fish in FISHES:
    # Capture fish
    log.info(f'Saved fish screenshot to {CAPTURE_FISHES_FOLDER}/{fish}.png...')
    pag.screenshot(region=mini_region,
                   imageFilename=f'{CAPTURE_FISHES_FOLDER}/{fish}.png'.replace(' ', '_'))

    # Click on arrow to go to next kitchens in the middle of the right edge
    pag.click(x=mini_region[0] + mini_region[2], y=mini_region[1] + mini_region[3] / 2)
    pag.sleep(1)

elapsed_time('fishes', FISHES)
