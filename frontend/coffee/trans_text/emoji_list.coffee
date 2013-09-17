do ->
  emoji_list = [
    "stucco",
    "test_sprite",
    "triumph",
    "eyes",
    "crying_cat_face",
    "satisfied",
    "white_check_mark",
    "mountain_bicyclist",
    "fries",
    "cow",
    "incoming_envelope",
    "trolleybus",
    "scorpius",
    "telephone",
    "baby_chick",
    "rainbow",
    "slot_machine",
    "hotsprings",
    "honeybee",
    "telescope",
    "ant",
    "bomb",
    "white_square",
    "kissing_smiling_eyes",
    "triangular_ruler",
    "balloon",
    "vs",
    "orange_book",
    "horse_racing",
    "bear",
    "rocket",
    "arrow_down",
    "ski",
    "jp",
    "train",
    "confused",
    "sparkler",
    "relaxed",
    "bridge_at_night",
    "o2",
    "four_leaf_clover",
    "soon",
    "iphone",
    "sunny",
    "plus1",
    "u7533",
    "ideograph_advantage",
    "clock4",
    "rage4",
    "video_game",
    "x",
    "hocho",
    "santa",
    "ghost",
    "bike",
    "do_not_litter",
    "leo",
    "hear_no_evil",
    "arrow_double_down",
    "currency_exchange",
    "pill",
    "foggy",
    "+1",
    "pencil",
    "interrobang",
    "rose",
    "european_castle",
    "wedding",
    "atm",
    "art",
    "kissing_heart",
    "monkey",
    "registered",
    "cry",
    "baby_symbol",
    "ru",
    "clock9",
    "relieved",
    "four",
    "aries",
    "evergreen_tree",
    "light_rail",
    "rice_ball",
    "penguin",
    "clipboard",
    "children_crossing",
    "signal_strength",
    "imp",
    "railway_car",
    "capricorn",
    "grimacing",
    "maple_leaf",
    "lollipop",
    "postbox",
    "speedboat",
    "truck",
    "bicyclist",
    "person_with_blond_hair",
    "cake",
    "tiger2",
    "tropical_drink",
    "jeans",
    "dragon_face",
    "volcano",
    "b",
    "mans_shoe",
    "guitar",
    "arrow_up",
    "arrow_forward",
    "person_frowning",
    "zzz",
    "mahjong",
    "nail_care",
    "octocat",
    "question",
    "house_with_garden",
    "baby",
    "no_entry",
    "mag",
    "bikini",
    "sailboat",
    "grey_exclamation",
    "clock5",
    "waxing_crescent_moon",
    "vhs",
    "mountain_cableway",
    "cancer",
    "joy_cat",
    "clock930",
    "oncoming_taxi",
    "kissing_closed_eyes",
    "airplane",
    "man_with_turban",
    "heart_decoration",
    "radio_button",
    "zap",
    "hammer",
    "u5272",
    "squirrel",
    "date",
    "facepunch",
    "shirt",
    "melon",
    "umbrella",
    "sleeping",
    "five",
    "six_pointed_star",
    "cat",
    "football",
    "milky_way",
    "surfer",
    "blowfish",
    "fish",
    "one",
    "two",
    "snowflake",
    "massage",
    "sos",
    "notebook",
    "fallen_leaf",
    "swimmer",
    "honey_pot",
    "fish_cake",
    "white_flower",
    "mag_right",
    "christmas_tree",
    "scissors",
    "jack_o_lantern",
    "minidisc",
    "hand",
    "woman",
    "arrow_lower_left",
    "8ball",
    "tongue",
    "point_down",
    "camera",
    "running",
    "globe_with_meridians",
    "hash",
    "underage",
    "beetle",
    "boom",
    "clock330",
    "round_pushpin",
    "spades",
    "arrow_lower_right",
    "car",
    "koala",
    "performing_arts",
    "bow",
    "icecream",
    "bus",
    "steam_locomotive",
    "closed_book",
    "cyclone",
    "mouse",
    "ng",
    "gift_heart",
    "couple_with_heart",
    "unamused",
    "heavy_minus_sign",
    "love_letter",
    "eyeglasses",
    "heavy_plus_sign",
    "heavy_dollar_sign",
    "flashlight",
    "loudspeaker",
    "watermelon",
    "symbols",
    "school",
    "yum",
    "bride_with_veil",
    "customs",
    "arrow_heading_down",
    "pouch",
    "full_moon_with_face",
    "pencil2",
    "turtle",
    "shower",
    "outbox_tray",
    "non-potable_water",
    "chart_with_downwards_trend",
    "recycle",
    "kr",
    "space_invader",
    "no_pedestrians",
    "cherries",
    "repeat_one",
    "page_with_curl",
    "arrow_double_up",
    "purple_heart",
    "no_bell",
    "gemini",
    "clock630",
    "pisces",
    "mortar_board",
    "stuck_out_tongue",
    "black_square_button",
    "anger",
    "new",
    "a",
    "girl",
    "meat_on_bone",
    "ear",
    "baby_bottle",
    "pineapple",
    "arrow_heading_up",
    "calendar",
    "panda_face",
    "clock1230",
    "sun_with_face",
    "suspension_railway",
    "point_left",
    "white_square_button",
    "rage2",
    "boy",
    "ring",
    "blue_car",
    "first_quarter_moon",
    "hospital",
    "clap",
    "shit",
    "basketball",
    "small_orange_diamond",
    "bookmark_tabs",
    "dango",
    "suspect",
    "chicken",
    "envelope",
    "boot",
    "bulb",
    "muscle",
    "older_man",
    "cocktail",
    "mens",
    "city_sunrise",
    "red_circle",
    "water_buffalo",
    "o",
    "u7121",
    "-1",
    "mountain_railway",
    "book",
    "smirk",
    "wavy_dash",
    "candy",
    "sagittarius",
    "revolving_hearts",
    "gem",
    "sleepy",
    "two_hearts",
    "tram",
    "horse",
    "stuck_out_tongue_winking_eye",
    "grapes",
    "toilet",
    "capital_abcd",
    "tractor",
    "frog",
    "bamboo",
    "congratulations",
    "pizza",
    "fire",
    "game_die",
    "koko",
    "goat",
    "curly_loop",
    "oden",
    "star2",
    "speak_no_evil",
    "custard",
    "six",
    "ferris_wheel",
    "rabbit2",
    "corn",
    "microscope",
    "sandal",
    "mega",
    "fu",
    "wolf",
    "raised_hands",
    "page_facing_up",
    "rotating_light",
    "ship",
    "computer",
    "lock_with_ink_pen",
    "crocodile",
    "heart_eyes_cat",
    "mailbox_closed",
    "u6708",
    "dash",
    "movie_camera",
    "cn",
    "flower_playing_cards",
    "house",
    "clock2",
    "chestnut",
    "1234",
    "tangerine",
    "golf",
    "chart_with_upwards_trend",
    "neckbeard",
    "bank",
    "handbag",
    "goberserk",
    "kissing",
    "clock7",
    "sake",
    "church",
    "cactus",
    "arrow_down_small",
    "bee",
    "wave",
    "closed_lock_with_key",
    "helicopter",
    "eight_spoked_asterisk",
    "floppy_disk",
    "warning",
    "grey_question",
    "dromedary_camel",
    "herb",
    "nut_and_bolt",
    "womans_clothes",
    "kimono",
    "u5408",
    "running_shirt_with_sash",
    "restroom",
    "dolls",
    "arrow_up_down",
    "u7a7a",
    "whale",
    "wink",
    "unlock",
    "soccer",
    "file_folder",
    "repeat",
    "fireworks",
    "banana",
    "clapper",
    "fountain",
    "bar_chart",
    "yellow_heart",
    "pensive",
    "sunglasses",
    "blue_heart",
    "camel",
    "information_desk_person",
    "cool",
    "octopus",
    "smirk_cat",
    "secret",
    "boat",
    "ramen",
    "loop",
    "bullettrain_side",
    "ticket",
    "information_source",
    "last_quarter_moon",
    "virgo",
    "statue_of_liberty",
    "aquarius",
    "egg",
    "waning_crescent_moon",
    "end",
    "european_post_office",
    "eight_pointed_black_star",
    "seat",
    "whale2",
    "shipit",
    "abc",
    "cat2",
    "japan",
    "v",
    "fast_forward",
    "saxophone",
    "sparkling_heart",
    "snowman",
    "tent",
    "metro",
    "u7981",
    "closed_umbrella",
    "heavy_check_mark",
    "point_up",
    "arrows_counterclockwise",
    "poultry_leg",
    "tv",
    "thought_balloon",
    "wind_chime",
    "diamonds",
    "womans_hat",
    "hourglass_flowing_sand",
    "ophiuchus",
    "accept",
    "copyright",
    "pager",
    "dollar",
    "dizzy_face",
    "new_moon_with_face",
    "shoe",
    "phone",
    "pray",
    "cloud",
    "partly_sunny",
    "gb",
    "bread",
    "articulated_lorry",
    "pig",
    "hatching_chick",
    "new_moon",
    "smiley_cat",
    "straight_ruler",
    "mailbox_with_mail",
    "paw_prints",
    "sushi",
    "no_good",
    "clock830",
    "rooster",
    "metal",
    "smile_cat",
    "smoking",
    "monkey_face",
    "tokyo_tower",
    "wrench",
    "innocent",
    "mushroom",
    "doughnut",
    "mouse2",
    "rugby_football",
    "keycap_ten",
    "mute",
    "small_red_triangle_down",
    "persevere",
    "high_brightness",
    "headphones",
    "baggage_claim",
    "beginner",
    "tada",
    "earth_africa",
    "japanese_ogre",
    "left_luggage",
    "purse",
    "postal_horn",
    "notebook_with_decorative_cover",
    "leopard",
    "rice_cracker",
    "fire_engine",
    "train2",
    "cherry_blossom",
    "u55b6",
    "left_right_arrow",
    "musical_keyboard",
    "ear_of_rice",
    "punch",
    "feet",
    "sound",
    "ox",
    "fried_shrimp",
    "tophat",
    "pound",
    "curry",
    "low_brightness",
    "nine",
    "no_bicycles",
    "ab",
    "raised_hand",
    "fist",
    "ok_woman",
    "small_blue_diamond",
    "dog2",
    "monorail",
    "sunrise",
    "euro",
    "lock",
    "calling",
    "weary",
    "name_badge",
    "e-mail",
    "anchor",
    "crossed_flags",
    "last_quarter_moon_with_face",
    "beer",
    "fishing_pole_and_fish",
    "frowning",
    "black_circle",
    "hibiscus",
    "tropical_fish",
    "black_nib",
    "vertical_traffic_light",
    "sunrise_over_mountains",
    "snake",
    "clubs",
    "clock12",
    "man_with_gua_pi_mao",
    "leaves",
    "cd",
    "stars",
    "musical_note",
    "hankey",
    "sheep",
    "arrow_right",
    "laughing",
    "pig2",
    "white_circle",
    "post_office",
    "couplekiss",
    "poop",
    "hushed",
    "passport_control",
    "snowboarder",
    "carousel_horse",
    "small_red_triangle",
    "hotel",
    "uk",
    "pouting_cat",
    "large_blue_circle",
    "stew",
    "mailbox",
    "sweat_drops",
    "clock130",
    "arrow_upper_left",
    "ocean",
    "heavy_division_sign",
    "green_apple",
    "heavy_exclamation_mark",
    "pig_nose",
    "dragon",
    "school_satchel",
    "mount_fuji",
    "blossom",
    "tomato",
    "high_heel",
    "ok_hand",
    "seven",
    "rabbit",
    "cookie",
    "bell",
    "clock10",
    "taurus",
    "hamburger",
    "ballot_box_with_check",
    "droplet",
    "peach",
    "paperclip",
    "haircut",
    "chocolate_bar",
    "tm",
    "mask",
    "circus_tent",
    "cinema",
    "birthday",
    "princess",
    "mailbox_with_no_mail",
    "bath",
    "de",
    "sa",
    "stuck_out_tongue_closed_eyes",
    "cop",
    "blue_book",
    "flags",
    "put_litter_in_its_place",
    "100",
    "card_index",
    "shell",
    "parking",
    "seedling",
    "id",
    "clock1130",
    "ambulance",
    "eggplant",
    "tired_face",
    "triangular_flag_on_post",
    "tulip",
    "bug",
    "dolphin",
    "expressionless",
    "credit_card",
    "bullettrain_front",
    "hearts",
    "pear",
    "disappointed",
    "exclamation",
    "godmode",
    "bird",
    "deciduous_tree",
    "electric_plug",
    "checkered_flag",
    "arrow_up_small",
    "heavy_multiplication_x",
    "grin",
    "office",
    "trumpet",
    "kiss",
    "sweat_smile",
    "strawberry",
    "sob",
    "rewind",
    "vibration_mode",
    "arrow_upper_right",
    "disappointed_relieved",
    "confounded",
    "free",
    "three",
    "collision",
    "clock430",
    "inbox_tray",
    "twisted_rightwards_arrows",
    "police_car",
    "rowboat",
    "green_book",
    "open_mouth",
    "leftwards_arrow_with_hook",
    "pushpin",
    "clock230",
    "anguished",
    "smiley",
    "bookmark",
    "guardsman",
    "sunflower",
    "clock1030",
    "bouquet",
    "m",
    "hatched_chick",
    "open_file_folder",
    "large_orange_diamond",
    "clock3",
    "potable_water",
    "aerial_tramway",
    "negative_squared_cross_mark",
    "cow2",
    "tea",
    "moneybag",
    "construction_worker",
    "tiger",
    "cupid",
    "email",
    "hamster",
    "japanese_goblin",
    "point_right",
    "bangbang",
    "nose",
    "heartpulse",
    "dancer",
    "two_men_holding_hands",
    "boar",
    "chart",
    "tennis",
    "syringe",
    "sparkles",
    "abcd",
    "wine_glass",
    "bento",
    "dancers",
    "broken_heart",
    "dvd",
    "angry",
    "musical_score",
    "palm_tree",
    "money_with_wings",
    "couple",
    "key",
    "fuelpump",
    "busstop",
    "sweet_potato",
    "finnadie",
    "love_hotel",
    "traffic_light",
    "clock8",
    "roller_coaster",
    "rice_scene",
    "see_no_evil",
    "ok",
    "scream_cat",
    "crystal_ball",
    "scroll",
    "feelsgood",
    "hurtrealbad",
    "rage3",
    "on",
    "microphone",
    "beers",
    "walking",
    "watch",
    "thumbsup",
    "black_joker",
    "flushed",
    "waxing_gibbous_moon",
    "arrow_left",
    "racehorse",
    "crown",
    "earth_asia",
    "rice",
    "moyai",
    "libra",
    "diamond_shape_with_a_dot_inside",
    "radio",
    "donut",
    "video_camera",
    "factory",
    "scream",
    "runner",
    "black_square",
    "hourglass",
    "alien",
    "earth_americas",
    "clock1",
    "green_heart",
    "fearful",
    "older_woman",
    "izakaya_lantern",
    "smiling_imp",
    "neutral_face",
    "no_mouth",
    "angel",
    "first_quarter_moon_with_face",
    "yen",
    "tanabata_tree",
    "rat",
    "kissing_face",
    "u6307",
    "arrow_right_hook",
    "raising_hand",
    "full_moon",
    "oncoming_automobile",
    "trophy",
    "shaved_ice",
    "barber",
    "moon",
    "smile",
    "trident",
    "us",
    "elephant",
    "point_up_2",
    "clock530",
    "confetti_ball",
    "top",
    "fork_and_knife",
    "tshirt",
    "skull",
    "ledger",
    "clock6",
    "minibus",
    "sweat",
    "eight",
    "link",
    "fax",
    "bathtub",
    "star",
    "door",
    "arrows_clockwise",
    "u6709",
    "gift",
    "ice_cream",
    "u6e80",
    "worried",
    "snail",
    "kissing_cat",
    "lips",
    "arrow_backward",
    "department_store",
    "gun",
    "no_entry_sign",
    "astonished",
    "speaker",
    "memo",
    "taxi",
    "dog",
    "dress",
    "coffee",
    "oncoming_police_car",
    "large_blue_diamond",
    "bowling",
    "bust_in_silhouette",
    "notes",
    "convenience_store",
    "clock730",
    "bowtie",
    "rage",
    "wc",
    "clock11",
    "lemon",
    "battery",
    "mobile_phone_off",
    "it",
    "briefcase",
    "japanese_castle",
    "oncoming_bus",
    "apple",
    "wheelchair",
    "person_with_pouting_face",
    "satellite",
    "trollface",
    "ribbon",
    "fr",
    "up",
    "necktie",
    "baseball",
    "heart",
    "es",
    "speech_balloon",
    "joy",
    "part_alternation_mark",
    "womens",
    "blush",
    "telephone_receiver",
    "station",
    "dart",
    "man",
    "red_car",
    "no_mobile_phones",
    "cl",
    "busts_in_silhouette",
    "thumbsdown",
    "two_women_holding_hands",
    "alarm_clock",
    "open_hands",
    "heart_eyes",
    "family",
    "ram",
    "spaghetti",
    "newspaper",
    "zero",
    "rage1",
    "violin",
    "books",
    "waning_gibbous_moon",
    "no_smoking",
    "city_sunset",
    "dizzy",
    "cold_sweat",
    "grinning",
    "construction",
    "poodle",
    "heartbeat",
    "lipstick",
  ]
  emoji_dict = {}
  for key in emoji_list
    emoji_dict[key] = true

  window.emoji_dict = emoji_dict
