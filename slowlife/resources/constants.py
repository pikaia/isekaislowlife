APP_TITLE = 'BlueStacks App Player'

# global toggles
LOG_PAUSES = False
HIGHLIGHT = False
LOG_IMAGE = '../log/error.png'

COLLECT_GOLD = True
RANDOM_REQUESTS = True
KITCHEN = True
ROAMING = True
SCHOOL = False
STAGE = False
FOUNTAIN = True
BANQUET = False
DONATE = True

# Main script for collecting gold, roaming, random requests, inn serve,
MAIN_MENU = '../resources/mainmenu/'
MM_HOME = '../resources/mainmenu/home.png'
MM_VILLAGE = '../resources/mainmenu/village.png'

# Farmstead
FARMSTEAD = '../resources/mainmenu/village/farmstead.png'

# Banquet
ENTER_BANQUET = '../resources/mainmenu/village/drakenberg/enter_banquet.png'
ATTEND = '../resources/mainmenu/village/drakenberg/banquet/attend.png'
ATTEND_PARTY = '../resources/mainmenu/village/drakenberg/banquet/attend_party.png'
TAKE_SIT = '../resources/mainmenu/village/drakenberg/banquet/sit.png'

# Stage
MM_STAGE = '../resources/mainmenu/stage.png'
STAGE_FULLAUTO = '../resources/mainmenu/stage/fullauto.png'
STAGE_START = '../resources/mainmenu/stage/start.png'

# Fountain of wishes
MM_FOUNTAIN = '../resources/mainmenu/fountain_of_wishes.png'
FOUNTAIN_10 = '../resources/mainmenu/fountain_of_wishes/fountain10.png'
FOUNTAIN_1 = '../resources/mainmenu/fountain_of_wishes/fountain1.png'

MM_DRAKENBERG_TRADINGPOST = '../resources/mainmenu/village/drakenberg/enter_trading_post.png'
TRADINGPOST_GOLD1 = '../resources/mainmenu/village/drakenberg/trading_post/gold2.png'
TRADINGPOST_GOLD2 = '../resources/mainmenu/village/drakenberg/trading_post/gold1.png'
TRADINGPOST_BACK = '../resources/mainmenu/village/drakenberg/trading_post/back.png'

ENTER_ROAMING = '../resources/mainmenu/village/drakenberg/roaming.png'
ROAMING_GO = '../resources/mainmenu/village/drakenberg/roaming/go.png'
ROAMING_OK = '../resources/mainmenu/village/drakenberg/roaming/ok.png'
ROAMING_CANCEL = '../resources/mainmenu/village/drakenberg/roaming/cancel.png'
ROAMING_BACK = '../resources/mainmenu/village/drakenberg/roaming/back.png'

ENTER_SCHOOL = '../resources/mainmenu/village/enter_school.png'
SCHOOL_EDUCATE = '../resources/mainmenu/village/school/educate.png'
SCHOOL_BACK = '../resources/mainmenu/village/school/back.png'

ENTER_FISHING = '../resources/mainmenu/village/enter_fishing.png'
FISHING_COLLECT_BAIT = '../resources/mainmenu/village/fish/collect_bait.png'

VILLAGE_SCHOOL = '../resources/mainmenu/village/school.png'
ENTER_KITCHEN1 = '../resources/mainmenu/village/enter_kitchen1.png'
ENTER_KITCHEN2 = '../resources/mainmenu/village/enter_kitchen2.png'
KITCHEN_SERVE = '../resources/mainmenu/village/kitchen/serve.png'
KITCHEN_BACK = '../resources/mainmenu/village/kitchen/back.png'
KITCHEN_OK = '../resources/mainmenu/village/kitchen/ok.png'
KITCHEN_ORDER_JEWELS = '../resources/mainmenu/village/kitchen/order_jewels.png'
KITCHEN_CANCEL = '../resources/mainmenu/village/kitchen/cancel.png'
KITCHEN_GUESTS_AVAILABLE = '../resources/mainmenu/village/kitchen/guests_available.png'

ENTER_GUILD = '../resources/mainmenu/village/drakenberg/enter_guild.png'
ENTER_DONATION = '../resources/mainmenu/village/drakenberg/guild/donation.png'
DONATED = '../resources/mainmenu/village/drakenberg/guild/donation/donated.png'
BASIC_DONATION = '../resources/mainmenu/village/drakenberg/guild/donation/basic_donation.png'
DONATION = '../resources/mainmenu/village/drakenberg/guild/donation.png'
GUILD_CANCEL = '../resources/mainmenu/village/drakenberg/guild/cancel.png'
GUILD_HANDLE = '../resources/mainmenu/village/drakenberg/guild/handle.png'
GUILD_REQUESTS = '../resources/mainmenu/village/drakenberg/guild/random_requests.png'
GUILD_BACK = '../resources/mainmenu/village/drakenberg/guild/back.png'

DRAKENBERG_STAGE = '../resources/mainmenu/village/drakenberg/stage.png'
STAGE_CHALLENGE = '../resources/mainmenu/village/drakenberg/stage/challenge.png'
CHALLENGE_EMPTY = '../resources/mainmenu/village/drakenberg/stage/challenge/items_empty.png'
CHALLENGE_GOLD = '../resources/mainmenu/village/drakenberg/stage/challenge/gold_motivation.png'
CHALLENGE_ITEM = '../resources/mainmenu/village/drakenberg/stage/challenge/item_motivation.png'
CHALLENGE_NEGOTIATE = '../resources/mainmenu/village/drakenberg/stage/challenge/negotiate.png'
CHALLENGE_CONTINUE = '../resources/mainmenu/village/drakenberg/stage/challenge/tap_to_continue.png'

STAGE_GO = '../resources/mainmenu/village/drakenberg/stage/go.png'
EVENTS_CONTINUE = '../resources/mainmenu/village/drakenberg/stage/events/tap_to_continue.png'
STAGE_EVENTS_X = '../resources/mainmenu/village/drakenberg/stage/events_x.png'
STAGE_EVENTS_Y = '../resources/mainmenu/village/drakenberg/stage/events_y.png'
STAGE_AUTOHANDLE = '../resources/mainmenu/village/drakenberg/stage/events/autohandle.png'

# shared by all capture modules
CAPTURE_FULL_APP = '../resources/ss/data/source/building/full_app.png'
CAPTURE_MINI_APP = '../resources/ss/data/source/building/mini_app.png'

BUILDINGS = ['inn', 'apothecary', 'workshop', 'scroll shop', 'spring resort', 'central station', 'patisserie',
             'archery range', 'clinic', 'market street', 'bank', 'tailor shop', 'sports park', 'museum', 'theatre']

# Files used to drive capture
SOURCE_BUILDING_FOLDER = '../resources/ss/data/source/building'
SOURCE_BUILDING_EARNINGS = SOURCE_BUILDING_FOLDER + '/earnings.png'
SOURCE_BUILDING_NEXT = SOURCE_BUILDING_FOLDER + '/next.png'

# Images generated
CAPTURE_BUILDING_FOLDER = '../resources/ss/data/generated/building'

KITCHEN_STATIONS = ['oven', 'staple counter', 'big cooking pot', 'meat counter', 'frying pan', 'hydroponic tank',
                    'fermenting vat', 'fish tank', 'sushi counter', 'dungeon entrance']

# Files used to drive capture
SOURCE_KITCHEN_FOLDER = '../resources/ss/data/source/kitchen'
SOURCE_KITCHEN_NEXT = SOURCE_KITCHEN_FOLDER + '/next.png'

# Images generated
CAPTURE_KITCHEN_FOLDER = '../resources/ss/data/generated/kitchen'

CAPTURE_FISHES_FOLDER = '../resources/ss/data/generated/fishes'
FISHES = ['axolotol',
          'pirarucu',
          'gold pirarucu',
          'star anglerfish',
          'drakenburg monster',
          'sperm whale',
          'giant squid',
          'helicoprion',
          'smooth hammerhead',
          'mosasaurs',
          'megakarp',
          'aligator snapping turtle',
          'hermit crab',
          'piranhape',
          'giant catfish',
          'colorful bubble puffer',
          'anglerfish',
          'nubibranch',
          'bubble globefish',
          'marlin',
          'megalodon',
          'dumbo octopus',
          'mola mola',
          'angelfish',
          'bubble puffer',
          'sun carp',
          'turtoise',
          'betta',
          'piranha',
          'elecrtic eel',
          'bigmouth buffalo',
          'dorado',
          'lightning lionfish',
          'tuna',
          'turritosis dohrnii',
          'striped seahorse',
          'clownfish',
          'mahi-mahi',
          'redeye bass',
          'lobster',
          'horned frog',
          'flower crab',
          'sturgeon',
          'spotted gar',
          'longnose gar',
          'rainbow trout',
          'giant oarfish',
          'sardine',
          'turritopsis',
          'lionfish',
          'aquafrog',
          'snakehead',
          'carp',
          'oyster',
          'guppy',
          'ayu sweetfish',
          'blue sweetfish',
          'sea anemone',
          'tubuca arcuata',
          'starfish']
