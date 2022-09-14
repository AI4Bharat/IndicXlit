import re

LANG_CODE_TO_DISPLAY_NAME = {
    # Indo-Aryan
    ## Indic-scripts
    'as' : "Assamese - অসমীয়া",
    'bn' : "Bangla - বাংলা",
    'doi': "Dogri - डोगरी",
    'gom': "Goan Konkani - कोंकणी",
    'gu' : "Gujarati - ગુજરાતી",
    'hi' : "Hindi - हिंदी",
    'mai': "Maithili - मैथिली",
    'mr' : "Marathi - मराठी",
    'ne' : "Nepali - नेपाली",
    'or' : "Oriya - ଓଡ଼ିଆ",
    'pa' : "Panjabi - ਪੰਜਾਬੀ",
    'sa' : "Sanskrit - संस्कृतम्",
    'si' : "Sinhala - සිංහල",
    ## Perso-Arabic scripts
    'ks' : "Kashmiri - كٲشُر",
    'pnb': "Panjabi (Western) - پن٘جابی",
    'sd' : "Sindhi - سنڌي",
    'skr': "Saraiki - سرائیکی",
    'ur' : "Urdu - اُردُو",
    ## Misc
    'dv' : "Dhivehi - ދިވެހި",

    # Dravidian
    'kn' : "Kannada - ಕನ್ನಡ",
    'ml' : "Malayalam - മലയാളം",
    'ta' : "Tamil - தமிழ்",
    'te' : "Telugu - తెలుగు",
    
    # Tibeto-Burman
    'brx': "Boro - बड़ो",
    'mni': "Manipuri - ꯃꯤꯇꯩꯂꯣꯟ",

    # Munda
    'sat': "Santali - ᱥᱟᱱᱛᱟᱲᱤ",

    # Misc
    'en' : "English",
}

PERSOARABIC_LANG_CODES = {
    'ks',
    'pnb',
    'sd',
    'skr',
    'ur',
}

RTL_LANG_CODES = set(PERSOARABIC_LANG_CODES)
RTL_LANG_CODES.add('dv')

# Default/Official language to script mapping
LANG_CODE_TO_SCRIPT_CODE = {

    # Indo-Aryan
    "as"   : "Beng",
    "bn"   : "Beng",
    "doi"  : "Deva",
    "dv"   : "Thaa",
    "gom"  : "Deva",
    "gu"   : "Gujr",
    "hi"   : "Deva",
    "ks"   : "Aran",
    "mai"  : "Deva",
    "mr"   : "Deva",
    "ne"   : "Deva",
    "or"   : "Orya",
    "pa"   : "Guru",
    "pnb"  : "Aran",
    "sa"   : "Deva",
    "sd"   : "Arab",
    "si"   : "Sinh",
    "skr"  : "Aran",
    "ur"   : "Aran",

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
    "Sinh": "\u0D80-\u0DFF",
    "Taml": "\u0B80-\u0BFF",
    "Telu": "\u0C00-\u0C7F",

    # Tibetic
    "Mtei": "\uABC0-\uABFF",

    # Misc
    "Arab": "\u0600-\u06FF\u0750-\u077F\u0870-\u089F\u08A0-\u08FF", # Perso-Arabic
    "Aran": "\u0600-\u06FF\u0750-\u077F\u0870-\u089F\u08A0-\u08FF", # Perso-Arabic (Nastaliq code)
    "Latn": "\u0041-\u005A\u0061-\u007A", # includes only basic/unaccented Roman
    "Olck": "\u1C50-\u1C7F",
    "Thaa": "\u0780-\u07BF",
}

INDIC_TO_LATIN_PUNCT = {
    ## List of all punctuations across languages

    # Brahmic
    '।': '.', # Nagari
    ## Archaic Indic
    '॥': "..",  # Sanskrit
    '෴': '.', # Sinhala
    ## Meetei (influenced from Burmese)
    '꫰': ',',
    '꯫': '.',

    # Ol Chiki
    '᱾': '.',
    '᱿': '..',

    # Arabic
    '۔': '.',
    '؟': '?',
    '،': ',',
    '؛': ';',
    '۝': "..",
}

INDIC_TO_LATIN_PUNCT_TRANSLATOR = str.maketrans(INDIC_TO_LATIN_PUNCT)

NON_LATIN_FULLSTOP_LANGS = {
    # Brahmic
    'as' : '।',
    'bn' : '।',
    'brx': '।',
    'doi': '।',
    'hi' : '।',
    'mai': '।',
    'mni': '꯫',
    'ne' : '।',
    'or' : '।',
    'pa' : '।',
    'sa' : '।',
    'sat': '᱾',

    # Nastaliq
    'ks' : '۔',
    'pnb': '۔',
    # 'sd' : '۔', # Sindhi uses Naskh, hence use latin
    'skr': '۔',
    'ur' : '۔',
}

ENDS_WITH_LATIN_FULLSTOP_REGEX = re.compile("(^|.*[^.])\.$")

def nativize_latin_fullstop(text, lang_code):
    if lang_code in NON_LATIN_FULLSTOP_LANGS and ENDS_WITH_LATIN_FULLSTOP_REGEX.match(text):
        return text[:-1] + NON_LATIN_FULLSTOP_LANGS[lang_code]
    return text

LATIN_TO_PERSOARABIC_PUNCTUATIONS = {
    # Except full-stop (since period-mark is ambiguous in usage, like fullforms)
    '?': '؟',
    ',': '،',
    ';': '؛',
}

LATIN_TO_PERSOARABIC_PUNC_TRANSLATOR = str.maketrans(LATIN_TO_PERSOARABIC_PUNCTUATIONS)

SCRIPT_CODE_TO_NUMERALS = {
    # ISO 15924 codes for script names

    # North Indic
    "Beng": "০১২৩৪৫৬৭৮৯",
    "Deva": "०१२३४५६७८९",
    "Gujr": "૦૧૨૩૪૫૬૭૮૯",
    "Guru": "੦੧੨੩੪੫੬੭੮੯",
    "Orya": "୦୧୨୩୪୫୬୭୮୯",

    # South Indic
    "Knda": "೦೧೨೩೪೫೬೭೮೯",
    "Mlym": "൦൧൨൩൪൫൬൭൮൯",
    "Sinh": "෦෧෨෩෪෫෬෭෮෯",
    "Taml": "௦௧௨௩௪௫௬௭௮௯",
    "Telu": "౦౧౨౩౪౫౬౭౮౯",

    # Tibetic
    "Mtei": "꯰꯱꯲꯳꯴꯵꯶꯷꯸꯹",

    # Misc
    "Arab": "۰۱۲۳۴۵۶۷۸۹", # Perso-Arabic numerals
    "Aran": "۰۱۲۳۴۵۶۷۸۹", # Perso-Arabic numerals
    "Latn": "0123456789",
    "Olck": "᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙",
    "Thaa": "٠١٢٣٤٥٦٧٨٩", # East-Arabic numerals. (Dhivehi does code-mixing with Arabic)
}

LANG_CODE_TO_NUMERALS = {
    lang_code: SCRIPT_CODE_TO_NUMERALS[script_code]
    for lang_code, script_code in LANG_CODE_TO_SCRIPT_CODE.items()
}

INDIC_TO_STANDARD_NUMERALS_GLOBAL_MAP = {}
for lang_code, lang_numerals in LANG_CODE_TO_NUMERALS.items():
    map_dict = {lang_numeral: en_numeral for lang_numeral, en_numeral in zip(lang_numerals, LANG_CODE_TO_NUMERALS["en"])}
    INDIC_TO_STANDARD_NUMERALS_GLOBAL_MAP.update(map_dict)

INDIC_TO_STANDARD_NUMERALS_TRANSLATOR = str.maketrans(INDIC_TO_STANDARD_NUMERALS_GLOBAL_MAP)

NATIVE_TO_LATIN_NUMERALS_TRANSLATORS = {
    lang_code: str.maketrans({lang_numeral: en_numeral for lang_numeral, en_numeral in zip(lang_numerals, LANG_CODE_TO_NUMERALS["en"])})
    for lang_code, lang_numerals in LANG_CODE_TO_NUMERALS.items()
    if lang_code != "en"
}

LATIN_TO_NATIVE_NUMERALS_TRANSLATORS = {
    lang_code: str.maketrans({en_numeral: lang_numeral for en_numeral, lang_numeral in zip(LANG_CODE_TO_NUMERALS["en"], lang_numerals)})
    for lang_code, lang_numerals in LANG_CODE_TO_NUMERALS.items()
    if lang_code != "en"
}

WORDFINAL_INDIC_VIRAMA_REGEX = re.compile("(\u09cd|\u094d|\u0acd|\u0a4d|\u0b4d|\u0ccd|\u0d4d|\u0dca|\u0bcd|\u0c4d|\uaaf6)$")
def hardfix_wordfinal_virama(text):
    # Add ZWNJ after a word-final halanta
    # Not applicable for non-Brahmic scripts (like Arabic & Ol-Chiki)
    return WORDFINAL_INDIC_VIRAMA_REGEX.sub("\\1\u200c", text)

# To replace last N occurences of a substring in a string
# Src: https://stackoverflow.com/questions/2556108/
def rreplace(text, find_pattern, replace_pattern, match_count=1):
    splits = text.rsplit(find_pattern, match_count)
    return replace_pattern.join(splits)
