LANG_CODE_TO_DISPLAY_NAME = {
    # European
    'en': "English",

    # Indo-Aryan
    ## Indic-scripts
    'as' : "Assamese - অসমীয়া",
    'bn' : "Bengali - বাংলা",
    'gom': "Goan Konkani - कोंकणी",
    'gu' : "Gujarati - ગુજરાતી",
    'hi' : "Hindi - हिंदी",
    'mai': "Maithili - मैथिली",
    'mr': "Marathi - मराठी",
    'ne': "Nepali - नेपाली",
    'or': "Oriya - ଓଡ଼ିଆ",
    'pa': "Panjabi - ਪੰਜਾਬੀ",
    'sa': "Sanskrit - संस्कृतम्",
    'si': "Sinhala - සිංහල",
    ## Perso-Arabic scripts
    'ks': "Kashmiri - كٲشُر",
    'sd': "Sindhi - سنڌي",
    'ur': "Urdu - اُردُو",

    # Dravidian
    'kn': "Kannada - ಕನ್ನಡ",
    'ml': "Malayalam - മലയാളം",
    'ta': "Tamil - தமிழ்",
    'te': "Telugu - తెలుగు",
    
    # Tibeto-Burman
    'brx': "Boro - बड़ो",
    'mni': "Manipuri - ꯃꯤꯇꯩꯂꯣꯟ",

    # Misc
    'en' : "English",
}

RTL_LANG_CODES = {
    'dv',  # "Dhivehi - ދިވެހި"
    'ks',  # "Kashmiri - كٲشُر"
    'pnb', # "Punjabi (Western) - پن٘جابی"
    'sd',  # "Sindhi - سنڌي"
    'skr', # "Saraiki - سرائیکی"
    'ur',  # "Urdu - اُردُو"
}

LANG_CODE_TO_SCRIPT_CODE = {

    # Indo-Aryan
    "as"   : "Beng",
    "bn"   : "Beng",
    "doi"  : "Deva",
    "dv"   : "Thaa",
    "gom"  : "Deva",
    "gu"   : "Gujr",
    "hi"   : "Deva",
    "ks"   : "Arab",
    "mai"  : "Deva",
    "mr"   : "Deva",
    "ne"   : "Deva",
    "or"   : "Orya",
    "pa"   : "Guru",
    "pnb"  : "Arab",
    "sa"   : "Deva",
    "sd"   : "Arab",
    "sd_IN": "Deva",
    "si"   : "Sinh",
    "skr"  : "Arab",
    "ur"   : "Arab",

    # Dravidian
    "kn"   : "Knda",
    "ml"   : "Mlym",
    "ta"   : "Taml",
    "te"   : "Telu",

    # Tibeto-Burman
    "brx"  : "Deva",
    "mni"  : "Mtei",

    # Munda
    "sat"  : "Olck",

    # Misc
    "en"   : "Latn",
}

SCRIPT_CODE_TO_UNICODE_CHARS_RANGE_STR = {
    # ISO 15924 codes for script names

    # North Indic
    "Beng": "\u0980-\u09FF",
    "Deva": "\u0900-\u097F",
    "Gujr": "\u0A80-\u0AFF",
    "Guru": "\u0A00-\u0A7F",
    "Orya": "\u0B00-\u0B7F",

    # South Indic
    "Knda": "\u0C80-\u0CFF",
    "Mlym": "\u0D00-\u0D7F",
    "Taml": "\u0B80-\u0BFF",
    "Telu": "\u0C00-\u0C7F",
    "Sinh": "\u0D80-\u0DFF",

    # Tibetic
    "Mtei": "\uABC0-\uABFF",

    # Misc
    "Arab": "\u0600-\u06FF\u0750-\u077F\u0870-\u089F\u08A0-\u08FF",
    "Latn": "\u0041-\u005A\u0061-\u007A", # includes only basic/unaccented Roman
    "Olck": "\u1C50-\u1C7F",
    "Thaa": "\u0780-\u07BF",
}

INDIC_TO_LATIN_PUNCT = {
    '।': '.',
    '॥': "..",

    # Arabic
    '۔': '.',
    '؟': '?',
    '،': ',',
    '؛': ';',
    '۝': "..",
}

INDIC_TO_LATIN_PUNCT_TRANSLATOR = str.maketrans(INDIC_TO_LATIN_PUNCT)


# To replace last N occurences of a substring in a string
# Src: https://stackoverflow.com/questions/2556108/
def rreplace(text, find_pattern, replace_pattern, match_count=1):
    splits = text.rsplit(find_pattern, match_count)
    return replace_pattern.join(splits)
