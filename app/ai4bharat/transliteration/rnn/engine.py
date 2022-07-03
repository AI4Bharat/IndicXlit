import os
import json
import enum
import traceback
from collections.abc import Iterable
from pydload import dload
import zipfile

from .core import XlitPiston

F_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(F_DIR, "models/default_lineup.json")

MODEL_DOWNLOAD_URL_PREFIX = 'https://github.com/AI4Bharat/IndianNLP-Transliteration/releases/download/xlit_v0.5.0/'
XLIT_VERSION = "v0.5" # If model/dict is changed on the storage, do not forget to change this variable in-order to force-download new assets

class XlitError(enum.Enum):
    lang_err = "Unsupported langauge ID requested ;( Please check available languages."
    string_err = "String passed is incompatable ;("
    internal_err = "Internal crash ;("
    unknown_err = "Unknown Failure"
    loading_err = "Loading failed ;( Check if metadata/paths are correctly configured."


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

class XlitEngineRNN():
    """
    For Managing the top level tasks and applications of transliteration

    Global Variables: F_DIR
    """
    def __init__(self, lang2use = "all", beam_width = 4, rescore=True):
        self.beam_width = beam_width

        lineup = json.load( open(CONFIG_PATH, encoding='utf-8') )
        self.lang_config = {}
        if isinstance(lang2use, str):
            if lang2use == "all":
                self.lang_config = lineup
            elif lang2use in lineup:
                self.lang_config[lang2use] = lineup[lang2use]
            else:
                raise Exception("XlitError: The entered Langauge code not found. Available are {}".format(lineup.keys()) )

        elif isinstance(lang2use, Iterable):
                for l in lang2use:
                    try:
                        self.lang_config[l] = lineup[l]
                    except:
                        print("XlitError: Language code {} not found, Skipping...".format(l))
        else:
            raise Exception("XlitError: lang2use must be a list of language codes (or) string of single language code" )

        if is_directory_writable(F_DIR):
            models_path = os.path.join(F_DIR, 'models')
        else:
            user_home = os.path.expanduser("~")
            models_path = os.path.join(user_home, '.AI4Bharat_Xlit_Models')
        models_path = os.path.join(models_path, XLIT_VERSION)
        os.makedirs(models_path, exist_ok=True)
        self.download_models(models_path)

        self.langs = set()
        self.lang_model = {}
        for la in self.lang_config:
            try:
                print("Loading {}...".format(la) )
                vocab_file = None
                if rescore:
                    vocab_file = os.path.join(models_path, self.lang_config[la]["vocab"])
                self.lang_model[la] = XlitPiston(
                    weight_path = os.path.join(models_path,
                                    self.lang_config[la]["weight"]) ,
                    iglyph_cfg_file = "en",
                    tglyph_cfg_file = os.path.join(models_path,
                                    self.lang_config[la]["script"]),
                    vocab_file = vocab_file,
                )
                self.langs.add(la)
            except Exception as error:
                print("XlitError: Failure in loading {} \n".format(la), traceback.format_exc())
                print(XlitError.loading_err.value)

    def download_models(self, models_path):
        '''
        Download models from GitHub Releases if not exists
        '''
        for l in self.lang_config:
            lang_name = self.lang_config[l]["eng_name"]
            lang_model_path = os.path.join(models_path, lang_name)
            if not os.path.isdir(lang_model_path):
                print('Downloading model for language: %s' % lang_name)
                remote_url = MODEL_DOWNLOAD_URL_PREFIX + lang_name + '.zip'
                downloaded_zip_path = os.path.join(models_path, lang_name + '.zip')
                dload(url=remote_url, save_to_path=downloaded_zip_path, max_time=None)

                if not os.path.isfile(downloaded_zip_path):
                    exit(f'ERROR: Unable to download model from {remote_url} into {models_path}')

                with zipfile.ZipFile(downloaded_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(models_path)

                if os.path.isdir(lang_model_path):
                    os.remove(downloaded_zip_path)
                else:
                    exit(f'ERROR: Unable to find models in {lang_model_path} after download')
        return

    def translit_word(self, eng_word, lang_code = "default", topk = 4):
        if eng_word == "":
            return []

        if (lang_code in self.langs):
            try:
                res_list = self.lang_model[lang_code].inferencer(eng_word, beam_width = self.beam_width)
                return res_list[:topk]

            except Exception as error:
                print("XlitError:", traceback.format_exc())
                print(XlitError.internal_err.value)
                return XlitError.internal_err

        elif lang_code == "default":
            try:
                res_dict = {}
                for la in self.lang_model:
                    res = self.lang_model[la].inferencer(eng_word, beam_width = self.beam_width)
                    res_dict[la] = res[:topk]
                return res_dict

            except Exception as error:
                print("XlitError:", traceback.format_exc())
                print(XlitError.internal_err.value)
                return XlitError.internal_err

        else:
            print("XlitError: Unknown Langauge requested", lang_code)
            print(XlitError.lang_err.value)
            return XlitError.lang_err


    def translit_sentence(self, eng_sentence, lang_code = "default"):
        if eng_sentence == "":
            return []

        if (lang_code in self.langs):
            try:
                out_str = ""
                for word in eng_sentence.split():
                    res_ = self.lang_model[lang_code].inferencer(word, beam_width = self.beam_width)
                    out_str = out_str + res_[0] + " "
                return out_str[:-1]

            except Exception as error:
                print("XlitError:", traceback.format_exc())
                print(XlitError.internal_err.value)
                return XlitError.internal_err

        elif lang_code == "default":
            try:
                res_dict = {}
                for la in self.lang_model:
                    out_str = ""
                    for word in eng_sentence.split():
                        res_ = self.lang_model[la].inferencer(word, beam_width = self.beam_width)
                        out_str = out_str + res_[0] + " "
                    res_dict[la] = out_str[:-1]
                return res_dict

            except Exception as error:
                print("XlitError:", traceback.format_exc())
                print(XlitError.internal_err.value)
                return XlitError.internal_err

        else:
            print("XlitError: Unknown Langauge requested", lang_code)
            print(XlitError.lang_err.value)
            return XlitError.lang_err


if __name__ == "__main__":

    engine = XlitEngine()
    y = engine.translit_sentence("Hello World !")
    print(y)
