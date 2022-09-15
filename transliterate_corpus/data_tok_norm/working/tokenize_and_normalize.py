import random
import re
from indicnlp.tokenize.indic_tokenize import trivial_tokenize
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory

class mni_tokenizer():
    def __init__(self, ):
        self.mapping = { 
            '\uABEB': ' \uABEB ', 
            '\uABEC': ' \uABEC ',
            '\uABED': ' \uABED '
        }

    def mni_tokenize(self, string):
        return string.translate(self.mapping)

class arabic_tokenizer():
    def __init__(self, ):
        self.mapping = { 
            '\u0609': ' \u0609 ', 
            '\u060A': ' \u060A ', 
            '\u060C': ' \u060C ', 
            '\u060D': ' \u060D ', 
            '\u061B': ' \u061B ', 
            '\u061D': ' \u061D ', 
            '\u061E': ' \u061E ', 
            '\u061F': ' \u061F ', 
            '\u066A': ' \u066A ', 
            '\u066B': ' \u066B ', 
            '\u066C': ' \u066C ', 
            '\u066D': ' \u066D ', 
            '\u06D4': ' \u06D4 ', 
        }

    def arabic_tokenize(self, string):
        return string.translate(self.mapping)

class old_chikki_tokenizer():
    def __init__(self, ):
        self.mapping = { 
            '\u1C7E': ' \u1C7E ', 
            '\u1C7F': ' \u1C7F ', 
        }

    def old_chikki_tokenize(self, string):
        return string.translate(self.mapping)


# lang_code_list = ['as', 'brx', 'bn', 'gom', 'gu', 'hi', 'kn', 'ks', 'mai', 'ml', 'mni', 'mr', 'ne', 'or', 'pa', 'sa', 'sd', 'ta', 'te', 'ur']
# lang_code_list = ['as', 'brx', 'bn', 
# 'gom', 'gu', 'hi', 'kn', 'mai', 'ml', 
#  'mni', 'mr', 'ne', 'or', 'pa', 'sa',
#   'sd', 'ta', 'te', 'ks', 'ur']
# lang_code_list = ['ur', 'dg', 'sat']

lang_code_list = ['as', 'bn', 'gom', 'gu', 
'hi', 'kn', 'ks', 'mai', 'ml', 'mni', 'mr', 
'ne', 'or', 'pa', 'sa', 'sat', 'sd', 'ta', 'te']

for lang_code in lang_code_list:
    combined_file_name = '../../wikipedia_raw_data/' +lang_code + '/'+lang_code + '.txt'
    file_in = open(combined_file_name, 'r')
    lines_in = file_in.read().split('\n')
    random.shuffle(lines_in)

    tok_norm_file_name = '../' +lang_code + '/'+lang_code + '_tok_norm.txt'
    file_out = open(tok_norm_file_name, 'w')
    
    # check for valid line
    lines_in = [line for line in lines_in if line]
    print(len(lines_in))


    # tokenizing
    lines_in = [ ' '.join(trivial_tokenize(line, lang_code)) for line in lines_in ]
    
    # replace double spaces to single space
    lines_in = [ re.sub(' +', ' ', line) for line in lines_in ]
    
    if lang_code in ['mni']:
        tokenizer = mni_tokenizer()
        lines_in = [ tokenizer.mni_tokenize(line) for line in lines_in ]
        
        # replace double spaces to single space
        lines_in = [ re.sub(' +', ' ', line) for line in lines_in ]

    if lang_code in ['sat']:
        tokenizer = old_chikki_tokenizer()
        lines_in = [ tokenizer.old_chikki_tokenize(line) for line in lines_in ]
        
        # replace double spaces to single space
        lines_in = [ re.sub(' +', ' ', line) for line in lines_in ]

    if lang_code in ['ur']:
        tokenizer = arabic_tokenizer()
        lines_in = [ tokenizer.arabic_tokenize(line) for line in lines_in ]
        
        # replace double spaces to single space
        lines_in = [ re.sub(' +', ' ', line) for line in lines_in ]
    
    
    if lang_code in ['ks']:
        tokenizer = arabic_tokenizer()
        lines_in = [ tokenizer.arabic_tokenize(line) for line in lines_in ]

        # replace double spaces to single space
        lines_in = [ re.sub(' +', ' ', line) for line in lines_in ]



    print(len(lines_in))


    # normalization
    if lang_code not in ['gom', 'ks', 'ur', 'mai', 'brx', 'mni', 'sat', 'dg']:
        normalizer_factory = IndicNormalizerFactory()
        normalizer = normalizer_factory.get_normalizer(lang_code)
        lines_in = [ normalizer.normalize(line) for line in lines_in ]

    if lang_code in ['mai', 'brx' , 'dg']:
        normalizer_factory = IndicNormalizerFactory()
        normalizer = normalizer_factory.get_normalizer('hi')
        lines_in = [ normalizer.normalize(line) for line in lines_in ]
    
    if lang_code in ['gom']:
        normalizer_factory = IndicNormalizerFactory()
        normalizer = normalizer_factory.get_normalizer('kK')
        lines_in = [ normalizer.normalize(line) for line in lines_in ]

    print(len(lines_in))

    tok_norm_file_name = '../' +lang_code + '/'+lang_code + '_tok_norm.txt'
    
    file_out = open(tok_norm_file_name, 'w')
    file_out.write('\n'.join(lines_in))
    file_out.close()