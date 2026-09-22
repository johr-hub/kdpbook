"""
KDP Activity Book Generator v3.4 (With Mazes & 120 Unique Sub-Themes)
File: app.py
"""

import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import random
import io

# ============================================================
# 1. PAGE SETUP & UNIVERSAL COORDINATES (ZERO OVERLAP)
# ============================================================
PAGE_W, PAGE_H = letter

TITLE_Y = PAGE_H - 0.65 * inch       # 10.35 in
SUBTITLE_Y = PAGE_H - 1.00 * inch    # 10.00 in
GRID_TOP = PAGE_H - 1.50 * inch      # 9.50 in (0.50 in safe gap below subtitle)
MARGIN_X = 0.75 * inch               # Safe KDP border
FOOTER_Y = 0.42 * inch

# ============================================================
# 2. BESTSELLING SUB-THEMES DATABASE (120 UNIQUE SUB-TOPICS)
# ============================================================
THEME_SUBTHEMES = {
    "Travel & Wonders": [
        ("European Capitals", ["PARIS", "LONDON", "ROME", "MADRID", "BERLIN", "ATHENS", "VIENNA", "DUBLIN", "LISBON", "WARSAW", "OSLO", "PRAGUE", "BRUSSELS", "HELSINKI"]),
        ("At The Airport", ["LUGGAGE", "BOARDING", "TERMINAL", "PASSPORT", "RUNWAY", "SECURITY", "PILOT", "TICKET", "BAGGAGE", "DEPARTURE", "GATE", "AIRLINE", "CUSTOMS", "CHECKIN"]),
        ("World Wonders", ["PYRAMIDS", "COLOSSEUM", "TAJMAHAL", "PETRA", "STONEHENGE", "GREATWALL", "ACROPOLIS", "BIGBEN", "ANGKORWAT", "STATUE", "CITADEL", "TEMPLE"]),
        ("Tropical Islands", ["PARADISE", "PALMTREE", "COCONUT", "SUNGLASSES", "RESORT", "HAMMOCK", "REEF", "LAGOON", "BREEZE", "CABANA", "SANDBAR", "HIBISCUS", "TURQUOISE"]),
        ("Cruise Vacation", ["STATEROOM", "PROMENADE", "CAPTAIN", "EXCURSION", "BUFFET", "PORTHOLE", "ANCHOR", "SAILING", "LIDO", "BALLROOM", "SHUFFLEBOARD", "DECKCHAIR"]),
        ("National Parks", ["YELLOWSTONE", "YOSEMITE", "GRANDCANYON", "ZION", "GLACIER", "ACADIA", "SMOKIES", "EVERGLADES", "OLYMPIC", "REDWOOD", "ARCHES", "SEQUOIA"]),
        ("Mountain Adventures", ["CAMPFIRE", "BACKPACK", "SUMMIT", "HIKING", "TRAIL", "COMPASS", "CANTEEN", "LANTERN", "ALPINE", "PEAK", "VALLEY", "PINES", "BOOTS"]),
        ("Famous Global Cities", ["TOKYO", "SYDNEY", "DUBAI", "CAIRO", "VENICE", "BANGKOK", "TORONTO", "SINGAPORE", "ISTANBUL", "BARCELONA", "CHICAGO", "SEATTLE", "BOSTON"]),
        ("Scenic Train Rides", ["LOCOMOTIVE", "SLEEPER", "CONDUCTOR", "RAILS", "STATION", "WHISTLE", "JOURNEY", "PASSENGER", "SCENIC", "CABOOSE", "DININGCAR", "CROSSING"]),
        ("A Day at the Beach", ["SANDCASTLE", "SEASHELL", "SURFBOARD", "UMBRELLA", "LIFEGUARD", "OCEAN", "SUNSCREEN", "TIDE", "BOARDWALK", "SUNBATHING", "SANDBAR", "WAVES"]),
        ("Ancient Civilizations", ["PHARAOH", "GLADIATOR", "TEMPLE", "EMPIRE", "MONUMENT", "SCRIBE", "ARTIFACT", "DYNASTY", "RUINS", "HIEROGLYPH", "MOSAIC", "CHARIOT"]),
        ("Road Trip Wonders", ["HIGHWAY", "BILLBOARD", "MAP", "MOTEL", "RESTSTOP", "SCENICVIEW", "SUNSET", "CONVERTIBLE", "CROSSROADS", "LANDMARK", "DETOUR", "GASSTATION"]),
        ("World Famous Museums", ["LOUVRE", "VATICAN", "METROPOLITAN", "SMITHSONIAN", "HERMITAGE", "GALLERY", "EXHIBIT", "SCULPTURE", "PORTRAIT", "CURATOR", "MASTERPIECE", "PRADO", "UFFIZI"]),
        ("African Safari", ["ELEPHANT", "GIRAFFE", "LION", "ZEBRA", "CHEETAH", "SAVANNA", "SAFARI", "RHINOCEROS", "LEOPARD", "GAZELLE", "WATERHOLE", "ANTELOPE"]),
        ("Famous Rivers & Lakes", ["AMAZON", "NILE", "DANUBE", "MISSISSIPPI", "RHINE", "VOLGA", "COLORADO", "SEINE", "THAMES", "VICTORIA", "GENEVA", "SUPERIOR"]),
        ("Historic Castles", ["WINDSOR", "VERSAILLES", "EDINBURGH", "TOWER", "RAMPART", "MOAT", "COURTYARD", "FORTRESS", "DRAWBRIDGE", "TURRET", "DUNGEON", "BASTION"]),
        ("Winter Ski Resort", ["SNOWBOARD", "CHAIRLIFT", "CHALET", "SLOPES", "CABIN", "GONDOLA", "GOGGLES", "POWDER", "FIREPLACE", "GLOVES", "BLIZZARD", "LODGE"]),
        ("World Cuisine Travel", ["PASTA", "CROISSANT", "GELATO", "SUSHI", "TAPAS", "PAELLA", "FONDUE", "CREPES", "BAKERY", "VINEYARD", "BISTRO", "GOURMET", "TRUFFLE"]),
        ("Island Hopping", ["FERRY", "ANCHOR", "ATOLL", "LIGHTHOUSE", "CATAMARAN", "HARBOR", "DOCK", "COVE", "MARINA", "SEAGULL", "CORAL", "DRIFTWOOD"]),
        ("Desert Expedition", ["DUNES", "CAMEL", "OASIS", "CARAVAN", "MIRAGE", "NOMAD", "CANYON", "SANDSTORM", "CACTUS", "SUNRISE", "BEDOUIN", "DESERTSTARS"]),
        ("Asian Wonders", ["PAGODA", "LANTERN", "RICKSHAW", "LOTUS", "MONSOON", "BAMBOO", "SHRINE", "FUJI", "KIMONO", "DRAGON", "CHOPSTICKS", "SILKROAD"]),
        ("Australian Outback", ["KANGAROO", "KOALA", "BOOMERANG", "REEF", "BILLABONG", "SYDNEY", "DINGO", "PLATYPUS", "EUCALYPTUS", "WALLABY", "CANYON", "TASMANIA", "PERTH"]),
        ("South American Jewels", ["ANDES", "TANGO", "CARNIVAL", "RAINFOREST", "IGUAZU", "GALAPAGOS", "COFFEE", "LLAMA", "SAMBA", "PATAGONIA", "AMAZONAS", "LIMA", "RIO", "BOGOTA"]),
        ("Great Waterfalls", ["NIAGARA", "VICTORIA", "ANGEL", "IGUAZU", "YOSEMITE", "GULLFOSS", "CASCADE", "PLUNGE", "MIST", "RAINBOW", "GORGE", "TORRENT"]),
        ("Famous Bridges", ["GOLDENGATE", "BROOKLYN", "TOWERBRIDGE", "SYDNEYHARBOUR", "RIALTO", "PONTEVECCHIO", "SUSPENSION", "ARCHWAY", "CABLES", "SPAN", "BOSPHORUS", "MACKINAC"]),
        ("Famous Monuments", ["LIBERTY", "CHRISTREDEEMER", "MOUNTMORE", "SPHINX", "ARCDE", "MONUMENT", "OBELISK", "COLOSSUS", "MEMORIAL", "PILLAR", "ACROPOLIS", "STONEHENGE"]),
        ("Packing Essentials", ["SUITCASE", "PASSPORT", "SUNSCREEN", "CAMERA", "CHARGER", "TOILETRIES", "SNEAKERS", "SUNGLASSES", "ADAPTER", "GUIDEBOOK", "JOURNAL", "BACKPACK"]),
        ("Luxury Hotel Stay", ["PENTHOUSE", "CONCIERGE", "BELLHOP", "BALCONY", "SUITE", "SPA", "JACUZZI", "ROBES", "ROOMSERVICE", "CHAMPAGNE", "SLIPPERS", "MINIBAR", "VALET"]),
        ("Walking City Tours", ["COBBLESTONE", "SQUARE", "FOUNTAIN", "CAFES", "MONUMENT", "GUIDE", "ALLEYWAY", "CLOCKTOWER", "DISTRICT", "AVENUE", "PROMENADE", "MARKET"]),
        ("Souvenir Shopping", ["POSTCARD", "MAGNET", "KEYCHAIN", "TRINKET", "CERAMIC", "CRAFTS", "KEEPSAKE", "ORNAMENT", "BAZAAR", "CURIO", "BADGE", "FIGURINE", "CALENDAR"]),
        ("Street Bazaars", ["SPICES", "TEXTILES", "CARPETS", "LANTERNS", "JEWELRY", "BRASSWARE", "INCENSE", "POTTERY", "HERBS", "ANTIQUE", "BARTER", "SILK", "LEATHER"]),
        ("Theme Park Adventures", ["ROLLERCOASTER", "CAROUSEL", "COTTONCANDY", "FIREWORKS", "PARADE", "TICKETS", "SOUVENIRS", "FERRISWHEEL", "FUNHOUSE", "LOGFLUME", "PRETZEL", "COASTER"]),
        ("Mediterranean Coast", ["RIVIERA", "YACHT", "VILLAS", "OLIVES", "SEASIDE", "CYPRESS", "BREEZE", "CLIFFS", "FISHERMEN", "TERRACE", "SUNSHINE", "CAPRI", "SANTORINI"]),
        ("Caribbean Cruise", ["BAHAMAS", "TURQUOISE", "CALYPSO", "REGGAE", "SNORKEL", "STINGRAY", "CORAL", "PIRATES", "ISLANDS", "SAILING", "COCONUT", "JAMAICA", "ARUBA"]),
        ("Scandinavian Fjords", ["VIKING", "WATERFALL", "AURORA", "GLACIER", "FERRY", "CLIFFSIDE", "PEAKS", "KAYAK", "FOREST", "MIDNIGHT", "HERRING", "BERGEN", "OSLO"]),
        ("Rainforest Trek", ["CANOPY", "JUNGLE", "TOUCAN", "JAGUAR", "FERNS", "ORCHIDS", "WATERFALL", "VINES", "MACAW", "FROGS", "TROPICAL", "PARROT", "MOSS"]),
        ("Starlit Camping", ["TENT", "FIREFLY", "MARSHMALLOW", "ROASTING", "CONSTELLATION", "SLEEPINGBAG", "WOODS", "CRICKETS", "MOONLIGHT", "CANTEEN", "PINEWOOD", "TWILIGHT"]),
        ("Historic Harbor Towns", ["WHARF", "SCHOONER", "COBBLESTONE", "MAST", "ANCHORAGE", "FOGHORN", "SEAFOOD", "TAVERN", "BUOY", "MERCHANT", "PILINGS", "SAILOR"]),
        ("Wine Country Tour", ["VINEYARD", "BARRELS", "CELLAR", "GRAPEVINE", "TASTING", "ESTATE", "SOMMELIER", "HARVEST", "OAKCASKS", "VINTAGE", "MERLOT", "BORDEAUX"]),
        ("Volcanoes & Geysers", ["CRATER", "LAVA", "MAGMA", "STEAM", "HOTSPRINGS", "OBSIDIAN", "CALDERA", "GEYSER", "ASHES", "MINERALS", "ERUPTION", "SULFUR", "BASALT"]),
        ("Coral Reef Diving", ["ANEMONE", "CLOWNFISH", "MANTA", "FLIPPERS", "SNORKEL", "DIVEMASK", "CORAL", "SEATURTLE", "SHIPWRECK", "BUBBLES", "BARRACUDA", "DEPTHS"]),
        ("Sacred Pilgrimages", ["CAMINO", "SANCTUARY", "BASILICA", "CATHEDRAL", "PILGRIM", "SHRINE", "JOURNEY", "DEVOTION", "STATION", "PRAYER", "CHURCH", "ALTAR"]),
        ("Canyons & Gorges", ["REDROCKS", "PLATEAU", "STRATA", "RIVERBED", "OVERLOOK", "FORMATION", "SANDSTONE", "BUTTE", "MESAS", "EROSION", "RAVINE", "CLIFFS"]),
        ("Grand Plazas", ["PIAZZA", "PALACE", "COLONNADE", "STATUES", "BELLTOWER", "ARCADES", "CAFELIFE", "PIGEONS", "STREETLAMP", "BOULEVARD", "CAFE", "BALCONY"]),
        ("Scenic Byways", ["MOUNTAINPASS", "CLIFFDRIVE", "COASTALROAD", "TURNOUT", "SWITCHBACK", "PANORAMA", "TUNNEL", "HORIZON", "BRIDGES", "FREEWAY", "VISTA", "EXPANSE"]),
        ("Alpine Lakes", ["MIRRORWATER", "PINEFOREST", "PEAKS", "ROWBOAT", "CANOE", "CABIN", "SHORELINE", "TROUT", "REFLECTIONS", "CRISP", "CLEARWATER", "PEBBLES"]),
        ("World Currency & Coins", ["PASSPORT", "VISA", "EXCHANGE", "STAMP", "CUSTOMS", "CURRENCY", "EMBASSY", "BANKNOTE", "DUTYFREE", "ENTRY", "STERLING", "FRANC"]),
        ("Botanical Gardens", ["CONSERVATORY", "ORCHIDS", "WATERLILIES", "PERGOLA", "FOUNTAINS", "TOPIARY", "BONSAI", "FERNERY", "ARBORETUM", "BAMBOO", "HYDRANGEA"]),
        ("Lighthouse Trail", ["BEACON", "LANTERN", "COASTLINE", "ROCKS", "FOGHORN", "KEEPERS", "TIDALPOOL", "HEADLAND", "BREAKWATER", "SHORE", "SEAWALL", "GULLS"]),
        ("Northern Lights Wonder", ["AURORA", "BOREALIS", "GLOW", "NIGHTSKY", "ARCTIC", "IGLOO", "SNOWSHOES", "HUSKY", "TUNDRA", "STELLARS", "GLIMMER", "FROST"])
    ],
    "Nostalgia & Heritage": [
        ("The Old Schoolhouse", ["CHALKBOARD", "DESK", "RECESS", "LUNCHBOX", "BELL", "INKWELL", "SLATE", "TEACHER", "PLAYGROUND", "BLACKBOARD", "RULER", "CRAYONS"]),
        ("Corner Soda Fountain", ["JUKEBOX", "MILKSHAKE", "BURGER", "BOOTH", "COUNTER", "FLOAT", "MALT", "COIN", "STRAW", "CHERRY", "SUNDAE", "BANANA"]),
        ("Grandma's Kitchen", ["BAKING", "COOKIES", "ROLLINGPIN", "FLOUR", "CINNAMON", "OVEN", "HOMEMADE", "APRON", "RECIPE", "PIE", "PANTRY", "SUGAR"]),
        ("Front Porch Evenings", ["ROCKINGCHAIR", "CRICKETS", "BREEZE", "LEMONADE", "TWILIGHT", "FIREFLIES", "NEIGHBORS", "SWING", "SUNSET", "WHISPER", "FIREFLY"]),
        ("Vintage Radio Shows", ["DRAMA", "COMEDY", "BROADCAST", "DIAL", "MICROPHONE", "ACTORS", "MYSTERY", "STATIC", "THEATER", "ANTENNA", "SERIAL", "NARRATOR"]),
        ("Childhood Games", ["MARBLES", "JUMPROPE", "HOPSCOTCH", "SPINNINGTOP", "KITE", "ROLLERSKATES", "REDROVER", "TAG", "HIDEANDSEEK", "JACKS", "KICKBALL"]),
        ("Classic Vinyl Records", ["NEEDLE", "TURNTABLE", "ALBUM", "SLEEVE", "GROOVE", "STEREO", "SPINNING", "HI-FI", "COLLECTION", "TRACKS", "LP", "JUKEBOX"]),
        ("The Drive-In Theater", ["SCREEN", "POPCORN", "SPEAKER", "INTERMISSION", "DUSK", "WINDOW", "CARS", "CARTOON", "DOUBLEFEATURE", "SNACKBAR", "HEADLIGHTS"]),
        ("Sunday Family Dinner", ["POTROAST", "GRAVY", "CASSEROLE", "TABLECLOTH", "PLATTER", "PRAYER", "LAUGHTER", "GATHERING", "BLESSING", "SERVE", "BISCUITS", "HAM"]),
        ("County Fair & Parades", ["CAROUSEL", "FERRISWHEEL", "COTTONCANDY", "RIBBONS", "LIVESTOCK", "BALLOONS", "TICKETS", "BAND", "TRACTOR", "CONTEST", "PRIZE"]),
        ("The Old Hardware Store", ["HAMMER", "NAILS", "WOODENKEG", "TWINE", "OILCAN", "WRENCH", "PAINT", "SAWDUST", "SCREWS", "ANVIL", "TOOLBOX", "PLIERS", "LEVEL"]),
        ("Vintage Barbershop", ["CHAIR", "RAZOR", "STRAP", "POMADE", "SCISSORS", "MIRROR", "SHAVECREAM", "HOTCLOTH", "TALC", "TONIC", "POLE", "COMB"]),
        ("Rotary Phones & Letters", ["DIAL", "RECEIVER", "STAMP", "ENVELOPE", "POSTMAN", "INKPEN", "STATIONERY", "MAILBOX", "CALLER", "CORD", "OPERATOR"]),
        ("Classic Board Games", ["CHECKERS", "CHESS", "DOMINOES", "SCRABBLE", "CLUE", "CARDS", "DICE", "TOKENS", "SPINNER", "VICTORY", "BATTLESHIP"]),
        ("Quilting & Sewing", ["NEEDLE", "THIMBLE", "PATCHWORK", "STITCH", "FABRIC", "PATTERN", "BOBBIN", "SCISSORS", "COTTON", "BEE", "QUILT", "SPOOL", "YARN"]),
        ("Ice Cream Truck Days", ["POPSICLE", "SANDWICH", "FUDGEBAR", "BELLS", "MELT", "CONE", "VANILLA", "CHOCOLATE", "SUMMERTIME", "COINS", "CORNETTO"]),
        ("The Old Swimming Hole", ["ROPE", "SWING", "CREEK", "SPLASH", "RIVERBANK", "SUNSHINE", "CANOE", "WILLOW", "DIVE", "SWIMSUIT", "DIVINGBOARD"]),
        ("Fourth of July Parade", ["FIREWORKS", "FLAGS", "MARCHINGBAND", "PICNIC", "SPARKLERS", "PATRIOTIC", "ANTHEM", "BBQ", "STREAMERS", "BANNER", "BRASSBAND", "CHEERS"]),
        ("Main Street Shops", ["BAKERY", "PHARMACY", "COBBLER", "HABERDASHER", "MILLINER", "FLORIST", "BUTCHER", "BOOKSHOP", "AWNING", "DRUGSTORE", "GENERAL"]),
        ("Family Photo Album", ["SEPIA", "POLAROID", "SCRAPBOOK", "PORTRAIT", "CAMERA", "FLASHBULB", "SMILE", "GENERATIONS", "KEEPSAKE", "CAMERAFILM", "BLACKWHITE"])
    ],
    "Gardening & Nature": [
        ("Spring Flower Garden", ["TULIP", "DAFFODIL", "CROCUS", "HYACINTH", "BLOSSOM", "PETALS", "LILY", "SNOWDROP", "IRIS", "PEONY", "ANEMONE", "PRIMROSE"]),
        ("The Vegetable Patch", ["TOMATO", "CARROT", "LETTUCE", "CUCUMBER", "RADISH", "BEANS", "PEAS", "PEPPER", "ZUCCHINI", "ONION", "SPINACH", "SQUASH"]),
        ("Garden Tools & Care", ["TROWEL", "SHOVEL", "PRUNERS", "RAKE", "WATERINGCAN", "WHEELBARROW", "GLOVES", "SHEARS", "HOE", "SPADE", "HOSE", "KNEELER"]),
        ("Backyard Songbirds", ["ROBIN", "CARDINAL", "BLUEBIRD", "SPARROW", "FINCH", "CHICKADEE", "HUMMINGBIRD", "NUTHATCH", "WREN", "ORIOLE", "SWALLOW", "WARBLER", "MOCKINGBIRD"]),
        ("Fragrant Herbs", ["BASIL", "ROSEMARY", "THYME", "LAVENDER", "MINT", "OREGANO", "SAGE", "PARSLEY", "CHIVES", "DILL", "CORIANDER", "TARRAGON"]),
        ("Bees & Pollinators", ["HONEYBEE", "BUMBLEBEE", "BUTTERFLY", "NECTAR", "POLLEN", "HIVE", "HONEYCOMB", "QUEEN", "SWARM", "BLOSSOM", "HOVERFLY", "BLOSSOMS"]),
        ("Fruit Orchard Harvest", ["APPLE", "PEACH", "CHERRY", "PEAR", "PLUM", "APRICOT", "ORCHARD", "LADDER", "BASKET", "BRANCH", "BLOSSOM", "SWEET"]),
        ("Majestic Woodland Trees", ["OAK", "MAPLE", "PINE", "BIRCH", "WILLOW", "CEDAR", "ELM", "ASH", "REDWOOD", "CYPRESS", "POPLAR", "BEECH"]),
        ("Garden Butterflies", ["MONARCH", "SWALLOWTAIL", "PAINTEDLADY", "CHRYSALIS", "WINGS", "CATERPILLAR", "NECTAR", "FLUTTER", "SILK", "SWALLOW", "VICEROY"]),
        ("Greenhouse Wonders", ["TERRARIUM", "SEEDLINGS", "POTTING", "BENCHES", "PROPAGATE", "MOISTURE", "HUMIDITY", "PLANTERS", "FERNS", "CLOCHE", "MISTING"])
    ],
    "Bible & Faith (Top Seller)": [
        ("Patriarchs of Faith", ["ABRAHAM", "ISAAC", "JACOB", "JOSEPH", "MOSES", "NOAH", "DAVID", "SOLOMON", "SAMUEL", "JOSHUA", "ELIJAH", "DANIEL"]),
        ("Fruits of the Spirit", ["LOVE", "JOY", "PEACE", "PATIENCE", "KINDNESS", "GOODNESS", "FAITHFULNESS", "GENTLENESS", "SELFCONTROL", "HARMONY", "DEVOTION"]),
        ("Beloved Hymns", ["AMAZINGGRACE", "HOWGREAT", "BLESSED", "HOLY", "SAVIOR", "REDEEMER", "PRAISE", "ROCKOFAGES", "HALLELUJAH", "HYMNAL", "HELEADS", "ABIDE"]),
        ("Places in Holy Land", ["JERUSALEM", "BETHLEHEM", "GALILEE", "NAZARETH", "JORDAN", "JERICHO", "CARMEL", "HEBRON", "BETHEL", "SINAI", "DEADSEA"]),
        ("Twelve Apostles", ["PETER", "ANDREW", "JAMES", "JOHN", "PHILIP", "MATTHEW", "THOMAS", "BARTHOLOMEW", "SIMON", "THADDEUS", "JUDAS", "MATTHIAS"]),
        ("Parables of Wisdom", ["SOWER", "TALENTS", "LOSTSHEEP", "PRODIGAL", "MUSTARDSEED", "GOODSAMARITAN", "LEAVEN", "PEARL", "VINEYARD", "WISEMAN", "GOODTREE"]),
        ("Scriptural Virtues", ["CHARITY", "MERCY", "HUMILITY", "COURAGE", "HONOR", "RIGHTEOUS", "FORGIVENESS", "TRUTH", "DEVOTION", "PURITY", "GRACE"]),
        ("Books of Wisdom", ["GENESIS", "PSALMS", "PROVERBS", "ECCLESIASTES", "ISAIAH", "MATTHEW", "ROMANS", "CORINTHIANS", "REVELATION", "JOB", "DANIEL"]),
        ("Angels & Messengers", ["GABRIEL", "MICHAEL", "CHERUBIM", "SERAPHIM", "HEAVENLY", "WINGS", "GLORY", "TRUMPET", "CHARIOT", "GUARDIAN", "SERAPH"]),
        ("Words of Comfort", ["SANCTUARY", "SHEPHERD", "REFUGE", "FORTRESS", "SALVATION", "EVERLASTING", "COVENANT", "ANOINTED", "LIGHT", "PROMISE", "HOPE"])
    ],
    "Holidays & Seasons (Etsy Bestseller)": [
        ("Christmas Morning", ["SANTA", "SLEIGH", "REINDEER", "WREATH", "ORNAMENT", "STOCKING", "CAROLS", "MISTLETOE", "TINSEL", "CHIMNEY", "RIBBON", "HOLLY", "PRESENT"]),
        ("Thanksgiving Feast", ["TURKEY", "STUFFING", "CRANBERRY", "HARVEST", "GRATITUDE", "PUMPKIN", "CASSEROLE", "GRAVY", "CORNUCOPIA", "DINNER", "ROAST", "AUTUMN"]),
        ("Autumn Harvest", ["PUMPKIN", "CORNSTALK", "APPLES", "CIDER", "ACORN", "SCARECROW", "FOLIAGE", "SWEATER", "HAYRIDE", "BONFIRE", "CRISP", "LEAVES"]),
        ("Winter Wonderland", ["SNOWFLAKE", "BLIZZARD", "ICICLE", "MITTENS", "SCARF", "FIREPLACE", "SLEDDING", "COCOA", "FROSTY", "BOOTS", "SNOWMAN", "ICE"]),
        ("Spring Renewal", ["BLOSSOM", "SEEDLINGS", "SHOWERS", "RAINBOW", "MEADOW", "TULIPS", "ROBINS", "BREEZE", "SUNSHINE", "GREENERY", "SPROUTS", "DAFFODILS"]),
        ("Summer Sunshine", ["SUNSCREEN", "SUNGLASSES", "SEASHELL", "WATERMELON", "LEMONADE", "CAMPING", "FIREFLY", "PICNIC", "BARBECUE", "BEACH", "BREEZE", "POOL"]),
        ("Easter Traditions", ["BUNNY", "BASKET", "TULIPS", "SPRING", "CHOCOLATE", "PARADE", "BONNET", "LILIES", "SUNDAY", "EGGS", "PASTEL", "BLESSING"]),
        ("Halloween Spooky", ["PUMPKIN", "COSTUME", "LANTERN", "CANDY", "GOBLIN", "GHOST", "MIDNIGHT", "SHADOWS", "SPIDERWEB", "BROOMSTICK", "AUTUMN", "TREAT"]),
        ("New Year Celebration", ["CONFETTI", "MIDNIGHT", "COUNTDOWN", "RESOLUTION", "FIREWORKS", "TOAST", "CELEBRATION", "BALLOONS", "CALENDAR", "PARTY", "CHEERS", "CLOCK"]),
        ("Valentine Romance", ["CANDY", "ROSES", "CUPID", "SWEETHEART", "CHOCOLATE", "BOUQUET", "AFFECTION", "CARDS", "RIBBONS", "ROMANCE", "HEARTS", "SMILE"])
    ],
    "Bakery, Coffee & Comfort Food": [
        ("The Morning Cafe", ["ESPRESSO", "CAPPUCCINO", "ROAST", "BARISTA", "STEAM", "MUG", "AROMA", "BEANS", "LATTE", "FROTH", "CARAMEL", "BLEND", "MOCHA"]),
        ("Fresh Bread Bakery", ["BAGUETTE", "SOURDOUGH", "CIABATTA", "BRIOCHE", "CRUST", "LOAF", "FLOUR", "YEAST", "KNEAD", "OVEN", "RYE", "WHEAT"]),
        ("Sweet Bakery Treats", ["CROISSANT", "DANISH", "CINNAMON", "ECLAIR", "SCONE", "MUFFIN", "DOUGHNUT", "TART", "PASTRIES", "PUFF", "SUGAR", "VANILLA"]),
        ("Homestyle Pies & Cakes", ["APPLEPIE", "BLUEBERRY", "CHEESECAKE", "CARROTCAKE", "FUDGE", "FROSTING", "LAYERS", "CRUMBLE", "SPICE", "CRUST", "CHERRY", "SLICE"]),
        ("Italian Comfort Kitchen", ["LASAGNA", "SPAGHETTI", "RAVIOLI", "RISOTTO", "PARMESAN", "BASIL", "TOMATO", "GARLIC", "MARINARA", "MEATBALL", "OLIVEOIL", "PASTA"]),
        ("Warm Soups & Stews", ["CHOWDER", "BISQUE", "BROTH", "VEGETABLE", "NOODLE", "POTATO", "CARROT", "SIMMER", "LENTIL", "STEAM", "BOWLS", "CRACKERS"]),
        ("Sunday Country Breakfast", ["PANCAKES", "WAFFLES", "BACON", "OMELET", "MAPLE", "SYRUP", "SAUSAGE", "TOAST", "BUTTER", "HASHBROWNS", "BISCUITS", "EGGS"]),
        ("Old-Fashioned Ice Cream", ["CHOCOLATE", "VANILLA", "STRAWBERRY", "SUNDAE", "CARAMEL", "SPRINKLES", "WAFFLECONE", "CHERRY", "SCOOP", "FUDGE", "PARLOR", "CREAM"]),
        ("Cozy Tea Room", ["CHAMOMILE", "EARLGREY", "DARJEELING", "HONEY", "TEAPOT", "KETTLE", "SAUCER", "INFUSER", "HERBAL", "LEMON", "BISCUITS", "SCONES"]),
        ("Chocolate Confections", ["TRUFFLE", "COCOA", "PRALINE", "CARAMEL", "BONBON", "GANACHE", "MOUSSE", "DARK", "MILK", "BITTERSWEET", "VELVET", "MELT"])
    ],
    "Classic Cars": [
        ("American Muscle", ["MUSTANG", "CORVETTE", "CAMARO", "CHARGER", "CHALLENGER", "GTO", "CHEVELLE", "BARRACUDA", "ROADRUNNER", "FIREBIRD", "TRANSAM", "DAYTONA"]),
        ("1950s Cruisers", ["BELAIR", "ELDORADO", "THUNDERBIRD", "DESOTO", "HUDSON", "BUICK", "ROADMASTER", "PACKARD", "CHROME", "WHITEWALLS", "CHEVROLET", "STUDEBAKER"]),
        ("Under the Hood", ["CARBURETOR", "RADIATOR", "PISTON", "CRANKSHAFT", "ALTERNATOR", "SPARKPLUG", "MANIFOLD", "CAMSHAFT", "BATTERY", "DISTRIBUTOR", "FLYWHEEL", "VALVES"]),
        ("Classic Body Styles", ["CONVERTIBLE", "HARDTOP", "SEDAN", "COUPE", "STATIONWAGON", "ROADSTER", "FASTBACK", "CABRIOLET", "PICKUP", "WOODY", "T-TOP", "PANELVAN"]),
        ("At The Drag Strip", ["STARTLINE", "BURNOUT", "CHECKERED", "QUARTERMILE", "SPEEDWAY", "TACHOMETER", "HEADER", "SLICKS", "TROPHY", "SLIPSTREAM", "GREENLIGHT"])
    ],
    "Animals & Pets": [
        ("Beloved Dog Breeds", ["GOLDEN", "RETRIEVER", "BEAGLE", "POODLE", "LABRADOR", "SHEPHERD", "BULLDOG", "COLLIE", "SPANIEL", "DACHSHUND", "BOXER", "PUG"]),
        ("Playful Cats", ["WHISKERS", "PURRING", "CALICO", "SIAMESE", "TABBY", "PAWPRINTS", "KITTEN", "SCRATCHPOST", "YARN", "CATNIP", "NAPTIME", "FEATHER", "BOX"]),
        ("Farm Animals", ["ROOSTER", "STALLION", "LAMB", "PIGLET", "CALF", "GOAT", "DUCKLING", "DONKEY", "TURKEY", "BARN", "PASTURE", "COLT", "HEIFER"]),
        ("Ocean Dwellers", ["DOLPHIN", "SEATURTLE", "HUMPBACK", "SEAHORSE", "CLOWNFISH", "MANATEE", "OCTOPUS", "STARFISH", "STINGRAY", "CORAL", "JELLYFISH", "SEALION"]),
        ("Woodland Wildlife", ["DEER", "CHIPMUNK", "SQUIRREL", "BEAVER", "RACCOON", "BADGER", "FOX", "OWL", "WOODPECKER", "PORCUPINE", "MOOSE", "OTTER"])
    ]
}

PROVERBS = [
    ("A stitch in time saves ______.", "NINE"),
    ("Actions speak louder than ______.", "WORDS"),
    ("All that glitters is not ______.", "GOLD"),
    ("An apple a day keeps the doctor ______.", "AWAY"),
    ("Better late than ______.", "NEVER"),
    ("Birds of a feather flock ______.", "TOGETHER"),
    ("Don't count your chickens before they ______.", "HATCH"),
    ("Every cloud has a silver ______.", "LINING"),
    ("Honesty is the best ______.", "POLICY"),
    ("Laughter is the best ______.", "MEDICINE"),
    ("Practice makes ______.", "PERFECT"),
    ("The early bird catches the ______.", "WORM"),
    ("Two heads are better than ______.", "ONE"),
    ("Where there's a will, there's a ______.", "WAY"),
    ("A penny saved is a penny ______.", "EARNED"),
    ("Don't put all your eggs in one ______.", "BASKET"),
    ("Home is where the heart ______.", "IS"),
    ("Look before you ______.", "LEAP"),
    ("Rome was not built in a ______.", "DAY"),
    ("Slow and steady wins the ______.", "RACE"),
    ("You can't judge a book by its ______.", "COVER"),
    ("When in Rome, do as the Romans ______.", "DO"),
    ("Too many cooks spoil the ______.", "BROTH"),
    ("There is no place like ______.", "HOME"),
    ("The grass is always greener on the other ______.", "SIDE"),
    ("Strike while the iron is ______.", "HOT"),
    ("Out of sight, out of ______.", "MIND"),
    ("No news is good ______.", "NEWS"),
    ("A friend in need is a friend ______.", "INDEED"),
    ("Beauty is in the eye of the ______.", "BEHOLDER")
]

SCRAMBLE_WORDS_POOL = [
    "GARDEN", "FLOWER", "RADIO", "CAMERA", "FAMILY", "HOLIDAY", "COFFEE",
    "MUSIC", "TRAVEL", "MEMORY", "SUMMER", "DINNER", "FRIEND", "SPRING",
    "WINTER", "AUTUMN", "NATURE", "SUNDAY", "PICNIC", "RECORD", "SCHOOL",
    "CASTLE", "ISLAND", "SUNSHINE", "STREAM", "VALLEY", "FOREST", "MEADOW",
    "COTTAGE", "HARBOR", "SUNSET", "MORNING", "TEAPOT", "LANTERN", "GUITAR",
    "SILVER", "BLANKET", "CANDLE", "BRIDGE", "BREEZE", "CHERRY", "BUTTER",
    "PARADE", "LANTERN", "FIREPLACE", "CAROUSEL", "BALLOON", "VILLAGE", "QUILT",
    "BLOSSOM", "ORCHARD", "PLANTER", "COMPASS", "SEASIDE", "HORIZON", "MEADOW"
]

# ============================================================
# 3. GENERATION ENGINES (WORD SEARCH, SUDOKU, MAZE, ETC.)
# ============================================================
def get_puzzle_subtheme(theme_choice, puzzle_index):
    """Retrieve a unique named subtheme and words for each puzzle."""
    if theme_choice == "All Themes (Mix)":
        all_subs = []
        for cat_list in THEME_SUBTHEMES.values():
            all_subs.extend(cat_list)
        return all_subs[(puzzle_index - 1) % len(all_subs)]
    else:
        cat_list = THEME_SUBTHEMES.get(theme_choice, list(THEME_SUBTHEMES.values())[0])
        return cat_list[(puzzle_index - 1) % len(cat_list)]

def can_place(grid, grid_size, word, row, col, dr, dc):
    for i, char in enumerate(word):
        r, c = row + dr * i, col + dc * i
        if not (0 <= r < grid_size and 0 <= c < grid_size): return False
        if grid[r][c] not in ("", char): return False
    return True

def generate_word_search(words_pool, dementia_mode=False):
    grid_size = 10 if dementia_mode else 15
    max_words = 8 if dementia_mode else min(14, len(words_pool))
    directions = [(0, 1), (1, 0)] if dementia_mode else [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]

    words = list(dict.fromkeys(words_pool))
    if dementia_mode:
        words = [w for w in words if len(w) <= 8]
    if len(words) > max_words:
        words = random.sample(words, max_words)
    words = sorted(words, key=len, reverse=True)

    for _ in range(1500):
        grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
        placements = []
        success = True

        for word in words:
            candidates = []
            for row in range(grid_size):
                for col in range(grid_size):
                    for dr, dc in directions:
                        if can_place(grid, grid_size, word, row, col, dr, dc):
                            overlap = sum(grid[row + dr * i][col + dc * i] == char for i, char in enumerate(word))
                            candidates.append((overlap, random.random(), row, col, dr, dc))
            if not candidates:
                success = False
                break
            candidates.sort(reverse=True)
            best = candidates[:min(30, len(candidates))]
            _, _, row, col, dr, dc = random.choice(best)
            for i, char in enumerate(word):
                grid[row + dr * i][col + dc * i] = char
            placements.append((word, row, col, dr, dc))

        if success:
            for r in range(grid_size):
                for c in range(grid_size):
                    if not grid[r][c]:
                        grid[r][c] = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            return grid, placements, grid_size
    raise RuntimeError("Word Search generation failed")

def generate_number_search():
    grid_size = 12
    directions = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0)]
    numbers = ["".join(str(random.randint(1, 9)) for _ in range(5)) for _ in range(10)]
    numbers = list(dict.fromkeys(numbers))

    for _ in range(1500):
        grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
        placements = []
        success = True
        for num in numbers:
            candidates = []
            for row in range(grid_size):
                for col in range(grid_size):
                    for dr, dc in directions:
                        if can_place(grid, grid_size, num, row, col, dr, dc):
                            candidates.append((random.random(), row, col, dr, dc))
            if not candidates:
                success = False
                break
            _, row, col, dr, dc = random.choice(candidates)
            for i, digit in enumerate(num):
                grid[row + dr * i][col + dc * i] = digit
            placements.append((num, row, col, dr, dc))
        if success:
            for r in range(grid_size):
                for c in range(grid_size):
                    if not grid[r][c]:
                        grid[r][c] = str(random.randint(0, 9))
            return grid, placements, grid_size
    raise RuntimeError("Number search generation failed")

def generate_sudoku(difficulty="easy"):
    base, side = 3, 9
    pattern = lambda r, c: (base * (r % base) + r // base + c) % side
    rows = [g * base + x for g in random.sample(range(base), base) for x in random.sample(range(base), base)]
    cols = [g * base + x for g in random.sample(range(base), base) for x in random.sample(range(base), base)]
    nums = random.sample(range(1, 10), 9)

    solved = [[nums[pattern(r, c)] for c in cols] for r in rows]
    puzzle = [row[:] for row in solved]

    removals = {"easy": 36, "medium": 46, "hard": 54}.get(difficulty.lower(), 36)
    cells = [(r, c) for r in range(9) for c in range(9)]
    for r, c in random.sample(cells, removals):
        puzzle[r][c] = 0
    return puzzle, solved

def generate_maze(width=15, height=15):
    """Generate a clean DFS-backtracked maze with guaranteed single solution path."""
    maze = [[[True, True, True, True] for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]
    stack = [(0, 0)]
    visited[0][0] = True
    directions = [(-1, 0, 0, 2), (0, 1, 1, 3), (1, 0, 2, 0), (0, -1, 3, 1)]

    while stack:
        r, c = stack[-1]
        unvisited = []
        for dr, dc, wall_curr, wall_next in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and not visited[nr][nc]:
                unvisited.append((nr, nc, wall_curr, wall_next))
        if unvisited:
            nr, nc, wall_curr, wall_next = random.choice(unvisited)
            maze[r][c][wall_curr] = False
            maze[nr][nc][wall_next] = False
            visited[nr][nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()

    maze[0][0][0] = False
    maze[height - 1][width - 1][2] = False
    return maze

def solve_maze(maze, width=15, height=15):
    """Solve the maze via BFS to produce the exact answer path."""
    queue = [[(0, 0)]]
    visited = {(0, 0)}
    directions = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)]

    while queue:
        path = queue.pop(0)
        r, c = path[-1]
        if r == height - 1 and c == width - 1:
            return path
        for dr, dc, wall_idx in directions:
            if not maze[r][c][wall_idx]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(path + [(nr, nc)])
    return []

def scramble_word(word):
    chars = list(word)
    for _ in range(50):
        random.shuffle(chars)
        res = "".join(chars)
        if res != word: return res
    return word[::-1]

def make_missing_vowels(word):
    vowels = "AEIOU"
    return " ".join("_" if c in vowels else c for c in word)

# ============================================================
# 4. DRAWING HELPERS (GUARANTEED ZERO OVERLAP COORDINATES)
# ============================================================
def start_page(c, page_number, title, subtitle, book_title):
    c.setFont("Helvetica-Bold", 19)
    c.drawCentredString(PAGE_W / 2, TITLE_Y, title)
    if subtitle:
        c.setFont("Helvetica", 11)
        c.drawCentredString(PAGE_W / 2, SUBTITLE_Y, subtitle)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(PAGE_W / 2, FOOTER_Y, f"{book_title}  •  Page {page_number}")

def draw_dedication(c, page_number, book_title):
    start_page(c, page_number, "", "", book_title)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 2.8 * inch, "THIS BOOK BELONGS TO:")
    c.setLineWidth(1.5)
    c.line(1.5 * inch, PAGE_H - 3.4 * inch, PAGE_W - 1.5 * inch, PAGE_H - 3.4 * inch)

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 4.4 * inch, "A SPECIAL GIFT FROM:")
    c.line(1.5 * inch, PAGE_H - 5.0 * inch, PAGE_W - 1.5 * inch, PAGE_H - 5.0 * inch)

    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 6.0 * inch, "DATE: __________________________")

def draw_cover(c, page_number, book_title, subtitle="LARGE PRINT ACTIVITY BOOK"):
    start_page(c, page_number, book_title.upper(), subtitle, book_title)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0.8 * inch, "Brain Games & Activities")
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0.2 * inch, "Relaxing Puzzles to Stimulate Memory & Focus")
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 - 0.3 * inch, "Word Search • Sudoku • Mazes • Scramble • Proverbs • Missing Vowels")

def draw_section_divider(c, page_number, title, subtitle, book_title):
    start_page(c, page_number, title.upper(), subtitle, book_title)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 + 0.2 * inch, title)
    c.setFont("Helvetica", 12)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2 - 0.25 * inch, subtitle)

# ----------------- WORD SEARCH & NUMBER SEARCH -----------------
def draw_search_page(c, page_number, pnum, sub_title, grid, placements, grid_size, book_title, is_number=False):
    title = f"NUMBER SEARCH {pnum:02d}" if is_number else f"WORD SEARCH {pnum:02d}"
    start_page(c, page_number, title, sub_title.upper(), book_title)

    size = 5.85 * inch
    bottom = GRID_TOP - size
    left = (PAGE_W - size) / 2
    cell = size / grid_size

    c.setLineWidth(0.65)
    c.rect(left, bottom, size, size)
    for i in range(1, grid_size):
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)

    c.setFont("Helvetica-Bold", 16 if grid_size <= 10 else 12)
    for r in range(grid_size):
        for col in range(grid_size):
            c.drawCentredString(left + col * cell + cell / 2, bottom + (grid_size - 1 - r) * cell + cell / 2 - 4.5, grid[r][col])

    list_header_y = bottom - 0.38 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left, list_header_y, "NUMBERS TO FIND:" if is_number else "FIND THESE WORDS:")

    c.setFont("Helvetica", 10.5)
    items = sorted([item[0] for item in placements])
    columns = [left, left + 2.10 * inch, left + 4.20 * inch]
    for i, itm in enumerate(items):
        col_x = columns[min(i // 5, 2)]
        row_y = list_header_y - 0.32 * inch - (i % 5) * 0.27 * inch
        c.drawString(col_x, row_y, itm)

def draw_search_answer(c, page_number, pnum, sub_title, grid, placements, grid_size, book_title, is_number=False):
    title = f"ANSWER: NUMBER SEARCH {pnum:02d}" if is_number else f"ANSWER: WORD SEARCH {pnum:02d}"
    start_page(c, page_number, title, sub_title.upper(), book_title)

    size = 5.85 * inch
    bottom = GRID_TOP - size
    left = (PAGE_W - size) / 2
    cell = size / grid_size

    c.setLineWidth(0.5)
    c.rect(left, bottom, size, size)
    for i in range(1, grid_size):
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)

    c.saveState()
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(cell * 0.72)
    c.setLineCap(1)
    for itm, r, col, dr, dc in placements:
        er, ec = r + dr * (len(itm) - 1), col + dc * (len(itm) - 1)
        c.line(left + col * cell + cell / 2, bottom + (grid_size - 1 - r) * cell + cell / 2,
               left + ec * cell + cell / 2, bottom + (grid_size - 1 - er) * cell + cell / 2)
    c.restoreState()

    c.setFont("Helvetica-Bold", 14 if grid_size <= 10 else 11)
    for r in range(grid_size):
        for col in range(grid_size):
            c.drawCentredString(left + col * cell + cell / 2, bottom + (grid_size - 1 - r) * cell + cell / 2 - 4, grid[r][col])

    c.setFont("Helvetica", 9.5)
    c.drawCentredString(PAGE_W / 2, bottom - 0.40 * inch, "Highlighted strips indicate location and direction of items.")

# ----------------- MAZE PUZZLES (NEW!) -----------------
def draw_maze_page(c, page_number, pnum, maze, width, height, book_title):
    start_page(c, page_number, f"MAZE PUZZLE {pnum:02d}", "NAVIGATE FROM START TO FINISH", book_title)

    size = 5.85 * inch
    bottom = GRID_TOP - size
    left = (PAGE_W - size) / 2
    cell = size / width

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left + 2, GRID_TOP + 6, "START ↓")
    c.drawRightString(left + size - 2, bottom - 16, "FINISH ↓")

    c.setLineWidth(1.4)
    c.setLineCap(1)
    for r in range(height):
        for col in range(width):
            x1 = left + col * cell
            y1 = bottom + (height - 1 - r) * cell
            x2 = x1 + cell
            y2 = y1 + cell
            walls = maze[r][col]
            if walls[0]: c.line(x1, y2, x2, y2)
            if walls[1]: c.line(x2, y1, x2, y2)
            if walls[2]: c.line(x1, y1, x2, y1)
            if walls[3]: c.line(x1, y1, x1, y2)

    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, bottom - 0.45 * inch, "Find your way through the maze from START to FINISH.")

def draw_maze_answer(c, page_number, pnum, maze, path, width, height, book_title):
    start_page(c, page_number, f"ANSWER KEY: MAZE {pnum:02d}", "SOLVED PATH", book_title)

    size = 5.85 * inch
    bottom = GRID_TOP - size
    left = (PAGE_W - size) / 2
    cell = size / width

    # Draw solution path line
    c.saveState()
    c.setStrokeColorRGB(0.55, 0.55, 0.55)
    c.setLineWidth(cell * 0.35)
    c.setLineCap(1)
    c.setLineJoin(1)
    p = c.beginPath()
    p.moveTo(left + cell / 2, GRID_TOP + 4)
    for r, col in path:
        cx = left + col * cell + cell / 2
        cy = bottom + (height - 1 - r) * cell + cell / 2
        p.lineTo(cx, cy)
    p.lineTo(left + (width - 1) * cell + cell / 2, bottom - 4)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

    # Draw walls
    c.setLineWidth(1.4)
    c.setLineCap(1)
    for r in range(height):
        for col in range(width):
            x1 = left + col * cell
            y1 = bottom + (height - 1 - r) * cell
            x2 = x1 + cell
            y2 = y1 + cell
            walls = maze[r][col]
            if walls[0]: c.line(x1, y2, x2, y2)
            if walls[1]: c.line(x2, y1, x2, y2)
            if walls[2]: c.line(x1, y1, x2, y1)
            if walls[3]: c.line(x1, y1, x1, y2)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left + 2, GRID_TOP + 6, "START")
    c.drawRightString(left + size - 2, bottom - 16, "FINISH")

    c.setFont("Helvetica", 9.5)
    c.drawCentredString(PAGE_W / 2, bottom - 0.45 * inch, "Completed path shown from START to FINISH.")

# ----------------- SUDOKU -----------------
def draw_sudoku_page(c, page_number, pnum, puzzle, diff, book_title):
    start_page(c, page_number, f"SUDOKU {pnum:02d}", f"{diff.upper()} • LARGE PRINT", book_title)
    size = 5.85 * inch
    bottom = GRID_TOP - size
    left = (PAGE_W - size) / 2
    cell = size / 9

    c.setLineWidth(1.4)
    c.rect(left, bottom, size, size)
    for i in range(1, 9):
        c.setLineWidth(1.4 if i % 3 == 0 else 0.5)
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)

    c.setFont("Helvetica-Bold", 18)
    for r in range(9):
        for col in range(9):
            if puzzle[r][col]:
                c.drawCentredString(left + col * cell + cell / 2, bottom + (8 - r) * cell + cell / 2 - 6, str(puzzle[r][col]))

    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, bottom - 0.50 * inch, "Fill every row, column, and 3×3 box with numbers 1–9.")

def draw_sudoku_answer(c, page_number, pnum, sol, book_title):
    start_page(c, page_number, f"ANSWER KEY: SUDOKU {pnum:02d}", "COMPLETED SOLUTION", book_title)
    size = 5.85 * inch
    bottom = GRID_TOP - size
    left = (PAGE_W - size) / 2
    cell = size / 9

    c.setLineWidth(1.0)
    c.rect(left, bottom, size, size)
    for i in range(1, 9):
        c.setLineWidth(1.4 if i % 3 == 0 else 0.5)
        c.line(left + i * cell, bottom, left + i * cell, bottom + size)
        c.line(left, bottom + i * cell, left + size, bottom + i * cell)

    c.setFont("Helvetica-Bold", 14)
    for r in range(9):
        for col in range(9):
            c.drawCentredString(left + col * cell + cell / 2, bottom + (8 - r) * cell + cell / 2 - 5, str(sol[r][col]))

# ----------------- WORD SCRAMBLE -----------------
def draw_scramble_page(c, page_number, pnum, words, book_title):
    start_page(c, page_number, f"WORD SCRAMBLE {pnum:02d}", "UNSCRAMBLE EACH WORD", book_title)
    y = GRID_TOP - 0.10 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Unscramble the letters to find the word:")
    y -= 0.50 * inch
    c.setFont("Helvetica", 14)
    for idx, w in enumerate(words):
        c.drawString(MARGIN_X + 0.25 * inch, y, f"{idx + 1}.   {scramble_word(w)}")
        c.line(MARGIN_X + 2.5 * inch, y - 2, PAGE_W - MARGIN_X - 0.5 * inch, y - 2)
        y -= 0.50 * inch

def draw_scramble_answer(c, page_number, pnum, words, book_title):
    start_page(c, page_number, f"ANSWER KEY: SCRAMBLE {pnum:02d}", "SOLUTIONS", book_title)
    y = GRID_TOP - 0.10 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Unscrambled Solutions:")
    y -= 0.50 * inch
    c.setFont("Helvetica", 13)
    for idx, w in enumerate(words):
        c.drawString(MARGIN_X + 0.25 * inch, y, f"{idx + 1}.   {w}")
        y -= 0.45 * inch

# ----------------- PROVERBS -----------------
def draw_proverbs_page(c, page_number, pnum, proverbs, book_title):
    start_page(c, page_number, f"FAMILIAR SAYINGS {pnum:02d}", "FINISH THE PROVERB", book_title)
    y = GRID_TOP - 0.10 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Fill in the missing word to complete each saying:")
    y -= 0.55 * inch
    c.setFont("Helvetica", 13.5)
    for idx, (q, _) in enumerate(proverbs):
        c.drawString(MARGIN_X + 0.2 * inch, y, f"{idx + 1}.  {q}")
        y -= 0.58 * inch

def draw_proverbs_answer(c, page_number, pnum, proverbs, book_title):
    start_page(c, page_number, f"ANSWER: SAYINGS {pnum:02d}", "SOLUTIONS", book_title)
    y = GRID_TOP - 0.10 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Completed Proverb Answers:")
    y -= 0.55 * inch
    c.setFont("Helvetica", 13)
    for idx, (q, a) in enumerate(proverbs):
        filled = q.replace("______", f"[{a}]")
        c.drawString(MARGIN_X + 0.2 * inch, y, f"{idx + 1}.  {filled}")
        y -= 0.55 * inch

# ----------------- MISSING VOWELS -----------------
def draw_vowels_page(c, page_number, pnum, words, book_title):
    start_page(c, page_number, f"MISSING VOWELS {pnum:02d}", "FILL IN A, E, I, O, U", book_title)
    y = GRID_TOP - 0.10 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Fill in the missing vowels (A, E, I, O, U) to complete the word:")
    y -= 0.55 * inch
    c.setFont("Helvetica-Bold", 16)
    for idx, w in enumerate(words):
        masked = make_missing_vowels(w)
        c.drawString(MARGIN_X + 0.3 * inch, y, f"{idx + 1}.   {masked}")
        c.line(MARGIN_X + 3.0 * inch, y - 2, PAGE_W - MARGIN_X - 0.5 * inch, y - 2)
        y -= 0.50 * inch

def draw_vowels_answer(c, page_number, pnum, words, book_title):
    start_page(c, page_number, f"ANSWER: MISSING VOWELS {pnum:02d}", "SOLUTIONS", book_title)
    y = GRID_TOP - 0.10 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_X, y, "Completed Words:")
    y -= 0.55 * inch
    c.setFont("Helvetica", 13)
    for idx, w in enumerate(words):
        c.drawString(MARGIN_X + 0.3 * inch, y, f"{idx + 1}.   {w}")
        y -= 0.45 * inch

# ============================================================
# 5. STREAMLIT INTERFACE (V3.4 FULL MULTI-PUZZLE SUITE)
# ============================================================
st.set_page_config(page_title="KDP Senior Activity Book Creator", page_icon="📖", layout="centered")

st.title("📖 KDP Activity Book Generator v3.4")
st.write("Amazon KDP Bestselling Activity Books — Word Search, Sudoku, Mazes, Scramble, Proverbs & More!")

with st.sidebar:
    st.header("⚙️ Book Configuration")
    book_title = st.text_input("Book Title", value="Ultimate Senior Activity Book")
    
    audience_mode = st.radio(
        "Audience / Print Style",
        options=["Standard Large Print (Seniors)", "Gentle Dementia & Memory Care Mode (Extra Large, Simpler Mazes)"]
    )
    is_dementia = "Dementia" in audience_mode

    theme_choice = st.selectbox(
        "Book Main Theme",
        options=list(THEME_SUBTHEMES.keys()) + ["All Themes (Mix)"],
        index=0
    )

    puzzle_selection = st.multiselect(
        "Select Puzzle Types to Include:",
        options=["Word Search", "Maze Puzzle", "Sudoku", "Word Scramble", "Finish The Saying (Proverbs)", "Missing Vowels", "Number Search"],
        default=["Word Search", "Maze Puzzle", "Sudoku", "Word Scramble", "Finish The Saying (Proverbs)", "Missing Vowels"]
    )

    num_puzzles = st.select_slider(
        "Total Number of Puzzles (Book Size)",
        options=[25, 50, 75, 100, 150, 200],
        value=50,
        help="Answer Keys के साथ कुल किताब के पेज लगभग इसके दोगुने होंगे।"
    )

    difficulty = st.selectbox("Sudoku Difficulty", ["easy", "medium", "hard"], index=0)
    include_dedication = st.checkbox("Include 'This Book Belongs To' Dedication Page", value=True)
    include_answers = st.checkbox("Include Complete Answer Keys at End", value=True)

# Generate Logic
if st.button("🚀 Generate KDP-Ready PDF Book", type="primary"):
    if not puzzle_selection:
        st.error("कृपया कम से कम एक प्रकार की पहेली (Puzzle Type) अवश्य चुनें!")
    else:
        with st.spinner("Generating publication-ready KDP PDF with Mazes & 120 unique sub-topics..."):
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)
            c.setTitle(book_title)

            page_num = 1
            draw_cover(c, page_num, book_title, "MEMORY & RELAXATION EDITION" if is_dementia else "LARGE PRINT SENIOR PUZZLE BOOK")

            if include_dedication:
                page_num += 1
                c.showPage()
                draw_dedication(c, page_num, book_title)

            answer_callbacks = []

            for i in range(1, num_puzzles + 1):
                ptype = puzzle_selection[(i - 1) % len(puzzle_selection)]
                page_num += 1
                c.showPage()

                sub_title, sub_words = get_puzzle_subtheme(theme_choice, i)

                if ptype == "Word Search":
                    grid, placements, gsize = generate_word_search(sub_words, dementia_mode=is_dementia)
                    draw_search_page(c, page_num, i, sub_title, grid, placements, gsize, book_title, is_number=False)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, stitle=sub_title, gr=grid, pl=placements, gs=gsize:
                                draw_search_answer(cv, pn, idx, stitle, gr, pl, gs, book_title, is_number=False)
                        )
                elif ptype == "Maze Puzzle":
                    m_dim = 10 if is_dementia else 15
                    m_grid = generate_maze(m_dim, m_dim)
                    m_path = solve_maze(m_grid, m_dim, m_dim)
                    draw_maze_page(c, page_num, i, m_grid, m_dim, m_dim, book_title)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, mg=m_grid, mp=m_path, md=m_dim:
                                draw_maze_answer(cv, pn, idx, mg, mp, md, md, book_title)
                        )
                elif ptype == "Number Search":
                    grid, placements, gsize = generate_number_search()
                    draw_search_page(c, page_num, i, f"Puzzle {i:02d}", grid, placements, gsize, book_title, is_number=True)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, gr=grid, pl=placements, gs=gsize:
                                draw_search_answer(cv, pn, idx, f"Puzzle {idx:02d}", gr, pl, gs, book_title, is_number=True)
                        )
                elif ptype == "Sudoku":
                    puz, sol = generate_sudoku(difficulty)
                    draw_sudoku_page(c, page_num, i, puz, difficulty, book_title)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, s=sol:
                                draw_sudoku_answer(cv, pn, idx, s, book_title)
                        )
                elif ptype == "Word Scramble":
                    sample = random.sample(SCRAMBLE_WORDS_POOL, min(10, len(SCRAMBLE_WORDS_POOL)))
                    draw_scramble_page(c, page_num, i, sample, book_title)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, w=sample:
                                draw_scramble_answer(cv, pn, idx, w, book_title)
                        )
                elif ptype == "Finish The Saying (Proverbs)":
                    sample = random.sample(PROVERBS, min(8, len(PROVERBS)))
                    draw_proverbs_page(c, page_num, i, sample, book_title)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, pr=sample:
                                draw_proverbs_answer(cv, pn, idx, pr, book_title)
                        )
                elif ptype == "Missing Vowels":
                    sample = random.sample(sub_words, min(10, len(sub_words)))
                    draw_vowels_page(c, page_num, i, sample, book_title)
                    if include_answers:
                        answer_callbacks.append(
                            lambda cv, pn, idx=i, w=sample:
                                draw_vowels_answer(cv, pn, idx, w, book_title)
                        )

            if include_answers and answer_callbacks:
                page_num += 1
                c.showPage()
                draw_section_divider(c, page_num, "Solutions & Answers", "Complete answer keys for all puzzles", book_title)
                for cb in answer_callbacks:
                    page_num += 1
                    c.showPage()
                    cb(c, page_num)

            c.save()
            pdf_buffer.seek(0)

            st.success(f"🎉 शानदार! {page_num} पेजों की पूरी KDP बुक तैयार है (Mazes + 120 Unique Sub-Themes)!")
            st.download_button(
                label=f"📥 Download Complete PDF ({page_num} Pages)",
                data=pdf_buffer,
                file_name=f"{book_title.replace(' ', '_')}_{num_puzzles}_puzzles.pdf",
                mime="application/pdf"
            )
