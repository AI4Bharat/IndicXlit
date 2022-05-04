import re
import sys
from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from random import sample
from urduhack import normalize

# lang_abr_train = 'as'
# lang_train = 'Assamese'
# lang_pattern_train = "[^\u0980-\u09FF]"

lang_abr_train = sys.argv[1]
lang_train = sys.argv[2]

lang_patterns_train_dict = {
                        'Assamese' : "[^\u0980-\u09FF]",
                        'Bangla' : "[^\u0980-\u09FF]",
                        'Bodo' : "[^\u0900-\u097F]",
                        'Konkani' : "[^\u0900-\u097F]", 
                        'Gujarati' : "[^\u0A80-\u0AFF]",
                        'Hindi' : "[^\u0900-\u097F]",
                        'Kannada' : "[^\u0C80-\u0CFF]",
                        'Kashmiri' : "[^\u0600-\u089F]",
                        'Maithili' : "[^\u0900-\u097F]",
                        'Malayalam' : "[^\u0D00-\u0D7F]",
                        'Manipuri' : "[^\uABC0-\uABFF]",
                        'Marathi' : "[^\u0900-\u097F]",
                        'Nepali' : "[^\u0900-\u097F]",
                        'Oriya' : "[^\u0B00-\u0B7F]",
                        'Punjabi' : "[^\u0A00-\u0A7F]",
                        'Sanskrit' : "[^\u0900-\u097F]",
                        'Sindhi' : "[^\u0600-\u06FF]",
                        'Sinhala' : "[^\u0D80-\u0DFF]",
                        'Tamil' : "[^\u0B80-\u0BFF]",
                        'Telugu' : "[^\u0C00-\u0C7F]",
                        'Urdu' : "[^\u0600-\u06FF]",

}


data_resources = {
            'Assamese' : ['I','S','W','M'],
            'Bangla' : ['I','S','W','E','M'],
            'Bodo' : ['I','M'],
            'Konkani' : ['I','E','M'], 
            'Gujarati' : ['I','S','W','E','M'],
            'Hindi' : ['I','S','W','E','M'],
            'Kannada' : ['I','S','W','E','M'],
            'Kashmiri' : ['I','W', 'M'],
            'Maithili' : ['I','W','E','M'],
            'Malayalam' : ['I','S','W','E','M'],
            'Manipuri' : ['I','M'],
            'Marathi' : ['I','S','W','E','M'],
            'Nepali' : ['I','W','M'],
            'Oriya' : ['I','S','W','M'],
            'Punjabi' : ['I','S','W','E','M'],
            'Sanskrit' : ['I','W','M'],
            'Sindhi' : ['I','W','E'],
            'Sinhala' : ['E'],
            'Tamil' : ['I','S','W','E','M'],
            'Telugu' : ['I','S','W','E','M'],
            'Urdu' : ['I','W','E','M']
}



# preparing train data
print("lang_train : ",lang_train)

lines_train = []

if 'I' in data_resources[lang_train]:
    # indiccorp train data
    f_indiccorp_train = open('../indiccorp/threshold_0_35_files/translit_pairs_with_avg_score_thr_035_'+lang_abr_train+'.txt','r')
    lines_indiccorp_train = f_indiccorp_train.read().split('\n')
    lines_indiccorp_train = ['\t'.join(line.split('\t')[:2]) for line in lines_indiccorp_train]
    lines_train += lines_indiccorp_train
    print("indiccorp train pairs: ",len(lines_indiccorp_train))

if 'S' in data_resources[lang_train]:
    # samanantar train data
    f_samanantar_train = open('/nlsasfs/home/ai4bharat/manidl/yash/indic-xlit/all_data/samanantar/valid_pairs/'+lang_abr_train+'-en_valid.csv','r')
    lines_samanantar_train = f_samanantar_train.read().split('\n')
    lines_samanantar_train = ['\t'.join(line.split(',')) for line in lines_samanantar_train]
    lines_train += lines_samanantar_train
    print("samanantar train pairs: ",len(lines_samanantar_train))

if 'W' in data_resources[lang_train]:
    # wikidata train data
    f_wikidata_train = open('/nlsasfs/home/ai4bharat/manidl/yash/indic-xlit/all_data/wikidata/true_pairs/'+lang_abr_train+'.txt','r')
    lines_wikidata_train = f_wikidata_train.read().split('\n')
    lines_wikidata_train = ['\t'.join(line.split('|')[::-1]) for line in lines_wikidata_train]
    lines_train += lines_wikidata_train
    print("wikidata train pairs: ",len(lines_wikidata_train))


# filtering the train data
print("total train pairs: ",len(lines_train))

lines_train = [line for line in lines_train if line]
print("total train pairs (valid) : ",len(lines_train))
    
lines_train = list(set(lines_train))
print("total train pairs (removed duplicates) : ",len(lines_train))

lines_train = [line for line in lines_train if len(line.split('\t'))==2 ]
print("total train pairs (ensuring 2 words in one line) : ",len(lines_train))

# pattern = '[!@#$\")(\'\,%^&*?+:;{}<>/|\[\].`~-]'
# lines_train = [line for line in lines_train if not re.match( pattern, line.split('\t')[0] ) or re.match( pattern, line.split('\t')[1] ) ]

pattern = '[^a-zA-Z]'    
lines_train = [line for line in lines_train if not re.compile(pattern).search(line.split('\t')[1]) ]
print("total train pairs (removing words containing non-english characters) : ",len(lines_train))


lines_train = [line for line in lines_train if not re.compile(lang_patterns_train_dict[lang_train]).search(line.split('\t')[0]) ]
print("total train pairs (removing words containing non-hindi characters) : ",len(lines_train))

lines_train = ['\t'.join([line.split('\t')[0]]+[line.split('\t')[1].lower()]) for line in lines_train ]
print("total train pairs (converting english characters to small caps) : ",len(lines_train))


if lang_abr_train not in ['gom','ks','ur','mai', 'brx', 'mni']:
    normalizer_factory = IndicNormalizerFactory()
    normalizer = normalizer_factory.get_normalizer(lang_abr_train)
    lines_train = [ normalizer.normalize(line.split('\t')[0]) + '\t' + line.split('\t')[1] for line in lines_train ]
    print("total train pairs (normalizing native word) : ",len(lines_train))

if lang_abr_train in ['mai', 'brx' ]:
    normalizer_factory = IndicNormalizerFactory()
    normalizer = normalizer_factory.get_normalizer('hi')
    lines_train = [ normalizer.normalize(line.split('\t')[0]) + '\t' + line.split('\t')[1] for line in lines_train ]
    print("total train pairs (normalizing native word) : ",len(lines_train))

if lang_abr_train in [ 'ur' ]:
    lines_train = [ normalize(line.split('\t')[0]) + '\t' + line.split('\t')[1] for line in lines_train ]
    print("total train pairs (normalizing native word) : ",len(lines_train))
    
if lang_abr_train == 'gom':
    normalizer_factory = IndicNormalizerFactory()
    normalizer = normalizer_factory.get_normalizer('kK')
    lines_train = [ normalizer.normalize(line.split('\t')[0]) + '\t' + line.split('\t')[1] for line in lines_train ]
    print("total train pairs (normalizing native word) : ",len(lines_train))


lines_train = list(set(lines_train))
print("total train pairs (removed duplicates after converting small caps) : ",len(lines_train)) 


file_out = open('ISW_'+lang_abr_train+'.txt','w')
file_out.write( '\n'.join(lines_train) )
file_out.close()