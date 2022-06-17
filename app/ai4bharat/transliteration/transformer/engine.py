import os
import json
import enum
import traceback
import re
import tqdm

import logging
logging.basicConfig(level=logging.WARNING)

from .custom_interactive import Transliterator, SUPPORTED_INDIC_LANGS

F_DIR = os.path.dirname(os.path.realpath(__file__))

class XlitError(enum.Enum):
    lang_err = "Unsupported langauge ID requested ;( Please check available languages."
    string_err = "String passed is incompatable ;("
    internal_err = "Internal crash ;("
    unknown_err = "Unknown Failure"
    loading_err = "Loading failed ;( Check if metadata/paths are correctly configured."



from collections.abc import Iterable
from pydload import dload
import zipfile

# added by yash
MODEL_DOWNLOAD_URL = 'https://storage.googleapis.com/indic-xlit-public/final_model/indicxlit-en-indic-v1.0.zip'
DICTS_DOWNLOAD_URL = 'https://storage.googleapis.com/indic-xlit-public/final_model/word_prob_dicts.zip'
XLIT_VERSION = "v1.0" # If model/dict is changed on the storage, do not forget to change this variable in-order to force-download new assets

MODEL_FILE = 'transformer/indicxlit.pt'
CHARS_FOLDER = 'corpus-bin'
DICTS_FOLDER = 'word_prob_dicts'
DICT_FILE_FORMAT = '%s_word_prob_dict.json'

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

class XlitEngineTransformer():
    """
    For Managing the top level tasks and applications of transliteration

    TODO: Ability to pass `beam_width` dynamically
    """
    def __init__(self, lang2use = "all", beam_width=4, rescore=True):

        self.langs = set()
        if isinstance(lang2use, str):
            if lang2use == "all":
                self.langs = SUPPORTED_INDIC_LANGS
            elif lang2use in SUPPORTED_INDIC_LANGS:
                self.langs.add(lang2use)
            else:
                raise Exception("XlitError: The entered Langauge code not found. Available are {}".format(SUPPORTED_INDIC_LANGS) )
        elif isinstance(lang2use, Iterable):
                for l in lang2use:
                    if l in SUPPORTED_INDIC_LANGS:
                        self.langs.add(l)
                    else:
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

        # added by yash

        print("Initializing Multilingual model for transliteration")

        # initialize the model
        self.transliterator = Transliterator(
            os.path.join(models_path, CHARS_FOLDER), os.path.join(models_path, MODEL_FILE), beam_width, batch_size = 32
        )
        
        self._rescore = rescore
        if self._rescore:
            self.download_dicts(models_path)
            # loading the word_prob_dict for rescoring module
            self.word_prob_dicts = {}
            for la in tqdm.tqdm(self.langs, desc="Loading dicts into RAM"):
                self.word_prob_dicts[la] = json.load(open(
                    os.path.join(models_path, DICTS_FOLDER, DICT_FILE_FORMAT%la)
                ))


    def download_models(self, models_path):
        '''
        Download models from bucket
        '''
        # added by yash
        model_file_path = os.path.join(models_path, MODEL_FILE)
        if not os.path.isfile(model_file_path):
            print('Downloading Multilingual model for transliteration')
            remote_url = MODEL_DOWNLOAD_URL
            downloaded_zip_path = os.path.join(models_path, 'model.zip')
            
            dload(url=remote_url, save_to_path=downloaded_zip_path, max_time=None)

            if not os.path.isfile(downloaded_zip_path):
                exit(f'ERROR: Unable to download model from {remote_url} into {models_path}')

            with zipfile.ZipFile(downloaded_zip_path, 'r') as zip_ref:
                zip_ref.extractall(models_path)

            if os.path.isfile(model_file_path):
                os.remove(downloaded_zip_path)
            else:
                exit(f'ERROR: Unable to find models in {models_path} after download')
            
            print("Models downloaded to:", models_path)
            print("NOTE: When uninstalling this library, REMEMBER to delete the models manually")
        return

    def download_dicts(self, models_path):
        '''
        Download language model probablitites dictionaries
        '''
        dicts_folder = os.path.join(models_path, DICTS_FOLDER)
        if not os.path.isdir(dicts_folder):
            # added by yash
            print('Downloading language model probablitites dictionaries for rescoring module')
            remote_url = DICTS_DOWNLOAD_URL
            downloaded_zip_path = os.path.join(models_path, 'dicts.zip')
            
            dload(url=remote_url, save_to_path=downloaded_zip_path, max_time=None)

            if not os.path.isfile(downloaded_zip_path):
                exit(f'ERROR: Unable to download model from {remote_url} into {models_path}')

            with zipfile.ZipFile(downloaded_zip_path, 'r') as zip_ref:
                zip_ref.extractall(models_path)

            if os.path.isdir(dicts_folder):
                os.remove(downloaded_zip_path)
            else:
                exit(f'ERROR: Unable to find models in {models_path} after download')
        return



    def pre_process(self, words, lang_code):
        
        # small caps 
        words = [word.lower() for word in words]

        # normalize and tokenize the words
        # normalized_words = self.normalize(words)

        # manully mapping certain characters
        # normalized_words = self.hard_normalizer(normalized_words)

        # convert the word into sentence which contains space separated chars
        words = [' '.join(list(word)) for word in words]
        
        # adding language token
        words = ['__'+ lang_code +'__ ' + word for word in words]

        return words

    def rescore(self, res_dict, result_dict, target_lang, alpha ):
        
        alpha = alpha
        # word_prob_dict = {}
        word_prob_dict = self.word_prob_dicts[target_lang]

        candidate_word_prob_norm_dict = {}
        candidate_word_result_norm_dict = {}

        input_data = {}
        for i in res_dict.keys():
            input_data[res_dict[i]['S']] = []
            for j in range(len(res_dict[i]['H'])):
                input_data[res_dict[i]['S']].append( res_dict[i]['H'][j][0] )
        
        for src_word in input_data.keys():
            candidates = input_data[src_word]

            candidates = [' '.join(word.split(' ')) for word in candidates]
            
            total_score = 0

            if src_word.lower() in result_dict.keys():
                for candidate_word in candidates:
                    if candidate_word in result_dict[src_word.lower()].keys():
                        total_score += result_dict[src_word.lower()][candidate_word]
            
            candidate_word_result_norm_dict[src_word.lower()] = {}
            
            for candidate_word in candidates:
                candidate_word_result_norm_dict[src_word.lower()][candidate_word] = (result_dict[src_word.lower()][candidate_word]/total_score)

            candidates = [''.join(word.split(' ')) for word in candidates ]
            
            total_prob = 0 
            
            for candidate_word in candidates:
                if candidate_word in word_prob_dict.keys():
                    total_prob += word_prob_dict[candidate_word]        
            
            candidate_word_prob_norm_dict[src_word.lower()] = {}
            for candidate_word in candidates:
                if candidate_word in word_prob_dict.keys():
                    candidate_word_prob_norm_dict[src_word.lower()][candidate_word] = (word_prob_dict[candidate_word]/total_prob)
            
        output_data = {}
        for src_word in input_data.keys():
            
            temp_candidates_tuple_list = []
            candidates = input_data[src_word]
            candidates = [ ''.join(word.split(' ')) for word in candidates]
            
            
            for candidate_word in candidates:
                if candidate_word in word_prob_dict.keys():
                    temp_candidates_tuple_list.append((candidate_word, alpha*candidate_word_result_norm_dict[src_word.lower()][' '.join(list(candidate_word))] + (1-alpha)*candidate_word_prob_norm_dict[src_word.lower()][candidate_word] ))
                else:
                    temp_candidates_tuple_list.append((candidate_word, 0 ))

            temp_candidates_tuple_list.sort(key = lambda x: x[1], reverse = True )
            
            temp_candidates_list = []
            for cadidate_tuple in temp_candidates_tuple_list: 
                temp_candidates_list.append(' '.join(list(cadidate_tuple[0])))

            output_data[src_word] = temp_candidates_list

        return output_data

    def post_process(self, translation_str, target_lang):
        lines = translation_str.split('\n')

        list_s = [line for line in lines if 'S-' in line]
        # list_t = [line for line in lines if 'T-' in line]
        list_h = [line for line in lines if 'H-' in line]
        # list_d = [line for line in lines if 'D-' in line]

        list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
        # list_t.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
        list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
        # list_d.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )

        res_dict = {}
        for s in list_s:
            s_id = int(s.split('\t')[0].split('-')[1])
            
            res_dict[s_id] = { 'S' : s.split('\t')[1] }
            
            # for t in list_t:
            #     t_id = int(t.split('\t')[0].split('-')[1])
            #     if s_id == t_id:
            #         res_dict[s_id]['T'] = t.split('\t')[1] 

            res_dict[s_id]['H'] = []
            # res_dict[s_id]['D'] = []
            
            for h in list_h:
                h_id = int(h.split('\t')[0].split('-')[1])

                if s_id == h_id:
                    res_dict[s_id]['H'].append( ( h.split('\t')[2], pow(2,float(h.split('\t')[1])) ) )
            
            # for d in list_d:
            #     d_id = int(d.split('\t')[0].split('-')[1])
            
            #     if s_id == d_id:
            #         res_dict[s_id]['D'].append( ( d.split('\t')[2], pow(2,float(d.split('\t')[1]))  ) )

        for r in res_dict.keys():
            res_dict[r]['H'].sort(key = lambda x : float(x[1]) ,reverse =True)
            # res_dict[r]['D'].sort(key = lambda x : float(x[1]) ,reverse =True)
        

        # for rescoring 
        result_dict = {}
        for i in res_dict.keys():            
            result_dict[res_dict[i]['S']] = {}
            for j in range(len(res_dict[i]['H'])):
                 result_dict[res_dict[i]['S']][res_dict[i]['H'][j][0]] = res_dict[i]['H'][j][1]
        
        
        transliterated_word_list = []
        if self._rescore:
            output_dir = self.rescore(res_dict, result_dict, target_lang, alpha = 0.9)            
            for src_word in output_dir.keys():
                for j in range(len(output_dir[src_word])):
                    transliterated_word_list.append( output_dir[src_word][j] )

        else:
            for i in res_dict.keys():
                # transliterated_word_list.append( res_dict[i]['S'] + '  :  '  + res_dict[i]['H'][0][0] )
                for j in range(len(res_dict[i]['H'])):
                    transliterated_word_list.append( res_dict[i]['H'][j][0] )

        # remove extra spaces
        # transliterated_word_list = [''.join(pair.split(':')[0].split(' ')[1:]) + ' : ' + ''.join(pair.split(':')[1].split(' ')) for pair in transliterated_word_list]

        transliterated_word_list = [''.join(word.split(' ')) for word in transliterated_word_list]

        return transliterated_word_list

    def translit_word(self, word, lang_code="default", topk=4):
        # TODO @Yash: The code seems to be directly taken from NMT. Pls adapt for xlit to remove unnecessary things

        # exit if invalid inputs
        if not word:
            print("error : Please insert valid inputs : pass one word")
            return
        
        words = [word, ]

        # check if there is non-english characters
        pattern = '[^a-zA-Z]'    
        words = [ word for word in words if not re.compile(pattern).search(word) ]
        
        if not words:
            print("error : Please insert valid inputs : only pass english characters ")
            return
        
        if (lang_code in self.langs):
            # Passing the list of words
            try:
                perprcossed_words = self.pre_process(words, lang_code)
                translation_str = self.transliterator.translate(perprcossed_words, nbest=topk)
                transliterated_word_list = self.post_process(translation_str, lang_code)
            except Exception as error:
                    print("XlitError:", traceback.format_exc())
                    print(XlitError.internal_err.value)
                    return XlitError.internal_err

            # print(transliterated_word_list)
            # return {lang_code:transliterated_word_list}
            return transliterated_word_list
        
        elif lang_code == "default":
            try:
                res_dict = {}
                for la in self.langs:
                    perprcossed_words = self.pre_process(words, la)
                    translation_str = self.transliterator.translate(perprcossed_words, nbest=topk)
                    transliterated_word_list = self.post_process(translation_str, la)
                    res_dict[la] = transliterated_word_list
                return res_dict

            except Exception as error:
                print("XlitError:", traceback.format_exc())
                print(XlitError.internal_err.value)
                return XlitError.internal_err

        else:
            print("XlitError: Unknown Langauge requested", lang_code)
            print(XlitError.lang_err.value)
            return XlitError.lang_err

    def translit_sentence(self, eng_sentence, lang_code="default"):
        if not eng_sentence:
            return eng_sentence
        
        eng_sentence = eng_sentence.lower()
        matches = re.findall("[a-zA-Z]+", eng_sentence)

        if (lang_code in self.langs):
            try:
                out_str = eng_sentence
                for match in matches:
                    result = self.translit_word(match, lang_code, topk=1)[0]
                    out_str = re.sub(match, result, out_str, 1)
                return out_str

            except Exception as error:
                print("XlitError:", traceback.format_exc())
                print(XlitError.internal_err.value)
                return XlitError.internal_err

        elif lang_code == "default":
            try:
                res_dict = {}
                for la in self.langs:
                    out_str = eng_sentence
                    for match in matches:
                        result = self.translit_word(match, la, topk=1)[la][0]
                        out_str = re.sub(match, result, out_str, 1)
                    res_dict[la] = out_str
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
