import os
from collections.abc import Iterable

import logging
logging.basicConfig(level=logging.WARNING)

from .base_engine import BaseEngineTransformer, LANG_LIST_FILE

F_DIR = os.path.dirname(os.path.realpath(__file__))

MODEL_DOWNLOAD_URL = 'https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/indicxlit-en-indic-v1.0.zip'
DICTS_DOWNLOAD_URL = 'https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/word_prob_dicts.zip'
XLIT_VERSION = "v1.0" # If model/dict is changed on the storage, do not forget to change this variable in-order to force-download new assets

def is_folder_writable(folder):
    try:
        os.makedirs(folder, exist_ok=True)
        tmp_file = os.path.join(folder, '.write_test')
        with open(tmp_file, 'w') as f:
            f.write('Permission Check')
        os.remove(tmp_file)
        return True
    except:
        return False

def is_directory_writable(path):
    if os.name == 'nt':
        return is_folder_writable(path)
    return os.access(path, os.W_OK | os.X_OK)

class XlitEngineTransformer_En2Indic(BaseEngineTransformer):
    """
    For Managing the top level tasks and applications of transliteration

    TODO: Ability to pass `beam_width` dynamically
    """
    def __init__(self, lang2use = "all", beam_width=4, rescore=True):

        if is_directory_writable(F_DIR):
            models_path = os.path.join(F_DIR, 'models')
        else:
            user_home = os.path.expanduser("~")
            models_path = os.path.join(user_home, '.AI4Bharat_Xlit_Models')
        models_path = os.path.join(models_path, "en2indic", XLIT_VERSION)
        os.makedirs(models_path, exist_ok=True)

        lang_list_file = os.path.join(models_path, LANG_LIST_FILE)
        _all_supported_langs = open(lang_list_file).read().strip().split('\n')
        self._all_supported_langs = set(_all_supported_langs)
        if "en" in self._all_supported_langs:
            self._all_supported_langs.remove("en")

        self._tgt_langs = set()
        if isinstance(lang2use, str):
            if lang2use == "all":
                self._tgt_langs = self._all_supported_langs
            elif lang2use in self._all_supported_langs:
                self._tgt_langs.add(lang2use)
            else:
                raise Exception("XlitError: The entered Langauge code not found. Available are {}".format(self._all_supported_langs) )
        elif isinstance(lang2use, Iterable):
                for l in lang2use:
                    if l in self._all_supported_langs:
                        self._tgt_langs.add(l)
                    else:
                        print("XlitError: Language code {} not found, Skipping...".format(l))
        else:
            raise Exception("XlitError: lang2use must be a list of language codes (or) string of single language code" )

        

        model_file_path = self.download_models(models_path, MODEL_DOWNLOAD_URL)
        if rescore:
            dicts_folder = self.download_dicts(models_path, DICTS_DOWNLOAD_URL)
        else:
            dicts_folder = None
        
        super().__init__(models_path, beam_width=beam_width, rescore=rescore)
    
    @property
    def all_supported_langs(self):
        return self._all_supported_langs

    @property
    def tgt_langs(self):
        return self._tgt_langs

    def translit_word(self, word, lang_code="default", topk=4, transliterate_numerals=False):
        
        if lang_code in self.tgt_langs:
            transliterated_word_list = self._transliterate_word(word, src_lang='en', tgt_lang=lang_code, topk=topk, nativize_numerals=transliterate_numerals)
            return transliterated_word_list
        elif lang_code == "default":
            res_dict = {}
            for la in self.tgt_langs:
                transliterated_word_list = self._transliterate_word(word, src_lang='en', tgt_lang=la, topk=topk, nativize_numerals=transliterate_numerals)
                res_dict[la] = transliterated_word_list
            return res_dict
        else:
            raise NotImplementedError("Unsupported lang_code: " + lang_code)

    def translit_sentence(self, eng_sentence, lang_code="default", transliterate_numerals=True):

        if lang_code in self.tgt_langs:
            return self._transliterate_sentence(eng_sentence, src_lang='en', tgt_lang=lang_code, nativize_numerals=transliterate_numerals)
        elif lang_code == "default":
            res_dict = {}
            for la in self.tgt_langs:
                res_dict[la] = self._transliterate_sentence(eng_sentence, src_lang='en', tgt_lang=la, nativize_numerals=transliterate_numerals)
            return res_dict
        else:
            raise NotImplementedError("Unsupported lang_code: " + lang_code)
