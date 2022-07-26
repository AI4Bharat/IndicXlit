import os
from collections.abc import Iterable

import logging
logging.basicConfig(level=logging.WARNING)

from .base_engine import BaseEngineTransformer, LANG_LIST_FILE

F_DIR = os.path.dirname(os.path.realpath(__file__))

MODEL_DOWNLOAD_URL = 'https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/indicxlit-indic-en-v1.0.zip'
DICTS_DOWNLOAD_URL = 'https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/word_prob_dicts_en.zip'
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

class XlitEngineTransformer_Indic2En(BaseEngineTransformer):
    """
    For Managing the top level tasks and applications of transliteration

    TODO: Ability to pass `beam_width` dynamically
    """
    def __init__(self, beam_width=4, rescore=True):
        if is_directory_writable(F_DIR):
            models_path = os.path.join(F_DIR, 'models')
        else:
            user_home = os.path.expanduser("~")
            models_path = os.path.join(user_home, '.AI4Bharat_Xlit_Models')
        models_path = os.path.join(models_path, "indic2en", XLIT_VERSION)
        os.makedirs(models_path, exist_ok=True)

        lang_list_file = os.path.join(models_path, LANG_LIST_FILE)
        _all_supported_langs = open(lang_list_file).read().strip().split('\n')
        self._all_supported_langs = set(_all_supported_langs)
        if "en" in self._all_supported_langs:
            self._all_supported_langs.remove("en")

        self._tgt_langs = set(["en"])

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
    
    def translit_word(self, word, lang_code, topk=4):
        if lang_code not in self.all_supported_langs:
            raise NotImplementedError(f"Language: `{lang_code}` not yet supported")
        return self._transliterate_word(word, src_lang=lang_code, tgt_lang='en', topk=topk)
    
    def translit_sentence(self, indic_sentence, lang_code):
        if lang_code not in self.all_supported_langs:
            raise NotImplementedError(f"Language: `{lang_code}` not yet supported")
        return self._transliterate_sentence(indic_sentence, src_lang=lang_code, tgt_lang='en')
