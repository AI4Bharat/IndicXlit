import re
import sys
import json 
from indicnlp.tokenize.indic_tokenize import trivial_tokenize
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from custom_interactive import Transliterator

class Model:

    def __init__(self, beam, nbest):
        
        print("Initializing Multilingual model for transliteration")
        
        assert beam >= nbest , "beam should be grater than equal to nbest"

        # initialize the model
        self.transliterator = Transliterator(
            f"corpus-bin", f"transformer/indicxlit.pt", beam, nbest, batch_size = 32
        )
        

        # loading the word_prob_dict for rescoring module
        self.word_prob_dict_wrapped_dict = {
            target_lang_key : json.load(open(f"word_prob_dicts/{target_lang_key}_word_prob_dict.json", 'r'))
            for target_lang_key in ['bn','gu','hi','kn','ml','mr','pa','ta','te','gom','mai','sa']  
        }
        # for adding language token
        # self.target_lang = target_lang

    # def normalize(self, words, target_lang):
        
    #     if target_lang not in ['gom','ks','ur','mai']:
    #         normalizer_factory = IndicNormalizerFactory()
    #         normalizer = normalizer_factory.get_normalizer(target_lang)
    #         words = [ normalizer.normalize(word.split('\t')[0]) for word in words ]
    #         print("Normalized word : ",len(words))
            
    #     if target_lang == 'gom':
    #         normalizer_factory = IndicNormalizerFactory()
    #         normalizer = normalizer_factory.get_normalizer('kK')
    #         words = [ normalizer.normalize(word.split('\t')[0]) for word in words ]
    #         print("Normalized word : ",len(words))

    #     return words

    # def hard_normalizer(self, normalized_words):
    #     return normalized_words
    
    def pre_process(self, words, target_lang):
        
        # small caps 
        words = [word.lower() for word in words]

        # normalize and tokenize the words
        # normalized_words = self.normalize(words)

        # manully mapping certain characters
        # normalized_words = self.hard_normalizer(normalized_words)

        # convert the word into sentence which contains space separated chars
        words = [' '.join(list(word)) for word in words]
        
        # adding language token
        words = ['__'+ target_lang +'__ ' + word for word in words]

        return words

    def rescore(self, res_dict, result_dict, target_lang, alpha ):
        
        alpha = alpha
        # word_prob_dict = {}
        word_prob_dict = self.word_prob_dict_wrapped_dict[target_lang]

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

    def post_process(self, translation_str, target_lang, rescore):
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
        if rescore:
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

    def translate_word(self, words, target_lang, rescore):
        
        assert isinstance(words, str)

        if not isinstance(words, list):
            words = [words,]
        
        # check for blank lines
        words = [word for word in words if word]

        # exit if invalid inputs
        if not words:
            print("error : Please insert valid inputs : pass atleast one word")
            return

        # check if there is non-english characters
        pattern = '[^a-zA-Z]'    
        words = [ word for word in words if not re.compile(pattern).search(word) ]
        
        if not words:
            print("error : Please insert valid inputs : only pass english characters ")
            return
        
        words = self.pre_process(words, target_lang)

        # Passing the list of words
        translation_str = self.transliterator.translate(words)
        
        transliterated_word_list = self.post_process(translation_str, target_lang, rescore)

        print(transliterated_word_list)
        return transliterated_word_list

    # def batch_translate(self, words, rescore):

    #     assert isinstance(words, list)

    #     # check for blank lines
    #     words = [word for word in words if word]

    #     # exit if invalid inputs
    #     if not words:
    #         print("error : Please insert valid inputs : pass atleast one word")
    #         sys.exit()

    #     # check if there is non-english characters
    #     pattern = '[^a-zA-Z]'    
    #     len_words = len(words)
    #     words = [ word for word in words if not re.compile(pattern).search(word) ]
        
    #     if len(words) < len_words:
    #         print(" Warning : words will got removed from input list which has non-english characters")

    #     if not words:
    #         print("error : Please insert valid inputs : only pass english characters ")
    #         sys.exit()

    #     words = self.pre_process(words)

    #     # Passing the list of words
    #     translation_str = self.transliterator.translate(words)
        
    #     transliterated_word_list = self.post_process(translation_str, rescore)
    #     print(transliterated_word_list)

    #     return transliterated_word_list

 
