from random import sample
import re
# Benchmark : collecting all test data across all the langs in all_lang_lines_test_valid list

lang_abr_test_valid_list = ['as', 'bn', 'brx', 'gom', 'gu', 'hi', 'kn', 'ks', 'mai', 'ml', 'mni', 'mr', 'ne', 'or', 'pa', 'sa', 'sd', 'ta', 'te', 'ur']
lang_test_valid_list = ['Assamese', 'Bangla', 'Bodo', 'Konkani', 'Gujarati', 'Hindi', 'Kannada', 'Kashmiri', 'Maithili', 'Malayalam', 'Manipuri', 'Marathi', 'Nepali', 'Oriya', 'Punjabi', 'Sanskrit', 'Sindhi', 'Tamil', 'Telugu', 'Urdu']

lang_patterns_test_valid_dict = {
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


for lang_test_valid, lang_abr_test_valid in zip(lang_test_valid_list, lang_abr_test_valid_list):
    f_in_random_samp = open('../ISW_'+lang_abr_test_valid+'.txt','r')
    lines_random_samp = sample(f_in_random_samp.read().split('\n'), 2000)

    lines_random_samp = [line for line in lines_random_samp if line]
    print("Mined random sample valid pairs: ",len(lines_random_samp))

    lines_random_samp = ['\t'.join(line.split('\t')[:2]) for line in lines_random_samp]
    print("Mined random sample valid pairs : ",len(lines_random_samp))


    pattern = '[^a-zA-Z]'    
    lines_random_samp = [line for line in lines_random_samp if not re.compile(pattern).search(line.split('\t')[1]) ]
    print("total Mined random sample valid pairs (removing words containing non-english characters) : ",len(lines_random_samp))

    lines_random_samp = [line for line in lines_random_samp if not re.compile(lang_patterns_test_valid_dict[lang_test_valid]).search(line.split('\t')[0]) ]
    print("total Mined random sample valid pairs (removing words containing non-hindi characters) : ",len(lines_random_samp))

    f_in_random_samp.close()


    f_out_random_samp = open('valid_random_sample_2k_'+lang_abr_test_valid+'.txt','w')
    f_out_random_samp.write('\n'.join(lines_random_samp))
    f_out_random_samp.close()
