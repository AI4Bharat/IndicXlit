import re

lang_abr_test_valid_list = ['bn', 'gu', 'hi', 'kn', 'ml', 'mr', 'pa', 'ta', 'te', 'sd', 'si', 'ur']
lang_test_valid_list = ['Bangla', 'Gujarati', 'Hindi', 'Kannada', 'Malayalam', 'Marathi', 'Punjabi', 'Tamil', 'Telugu', 'Sindhi', 'Sinhala', 'Urdu']
lang_patterns_test_valid_dict = {
                        'Bangla' : "[^\u0980-\u09FF]", 
                        'Gujarati' : "[^\u0A80-\u0AFF]",
                        'Hindi' : "[^\u0900-\u097F]",
                        'Kannada' : "[^\u0C80-\u0CFF]",
                        'Malayalam' : "[^\u0D00-\u0D7F]",
                        'Marathi' : "[^\u0900-\u097F]",
                        'Punjabi' : "[^\u0A00-\u0A7F]",
                        'Tamil' : "[^\u0B80-\u0BFF]",
                        'Telugu' : "[^\u0C00-\u0C7F]",
                        'Sindhi' : "[^\u0600-\u06FF]",
                        'Sinhala' : "[^\u0D80-\u0DFF]",
                        'Urdu' : "[^\u0600-\u06FF]"
                        }




for lang_test_valid, lang_abr_test_valid in zip(lang_test_valid_list, lang_abr_test_valid_list):
    
    print("lang : ",lang_test_valid)

    # test data
    f_in_test = open('/home/yashkm/indic-xlit/corpus_org/dakshina_dataset_v1.0/'+lang_abr_test_valid+'/lexicons/'+lang_abr_test_valid+'.translit.sampled.test.tsv','r')
    lines_test = f_in_test.read().split('\n')

    lines_test = [line for line in lines_test if line]
    print("Dakshina test pairs: ",len(lines_test))

    lines_test = ['\t'.join(line.split('\t')[:2]) for line in lines_test]
    print("dakshina test pairs : ",len(lines_test))

    pattern = '[^a-zA-Z]'    
    lines_test = [line for line in lines_test if not re.compile(pattern).search(line.split('\t')[1]) ]
    print("total test pairs (removing words containing non-english characters) : ",len(lines_test))

    lines_test = [line for line in lines_test if not re.compile(lang_patterns_test_valid_dict[lang_test_valid]).search(line.split('\t')[0]) ]
    print("total test pairs (removing words containing non-hindi characters) : ",len(lines_test))

    # filtering the test data

    lines_test = [line for line in lines_test if line]
    print("lines_test size (valid) : ",len(lines_test))
        
    lines_test = list(set(lines_test))
    print("lines_test size (removed duplicates) : ",len(lines_test))

    lines_test = [line for line in lines_test if len(line.split('\t'))==2 ]
    print("lines_test size (ensuring 2 words in one line) : ",len(lines_test))

    lines_test = ['\t'.join([line.split('\t')[0]]+[line.split('\t')[1].lower()]) for line in lines_test ]
    print("lines_test size (converting english characters to small caps) : ",len(lines_test))

    lines_test = list(set(lines_test))
    print("lines_test size (removed duplicates after converting small caps) : ",len(lines_test)) 







    # valid data
    f_in_valid = open('/home/yashkm/indic-xlit/corpus_org/dakshina_dataset_v1.0/'+lang_abr_test_valid+'/lexicons/'+lang_abr_test_valid+'.translit.sampled.dev.tsv','r')
    lines_valid = f_in_valid.read().split('\n')

    lines_valid = [line for line in lines_valid if line]
    print("Dakshina valid pairs: ",len(lines_valid))

    lines_valid = ['\t'.join(line.split('\t')[:2]) for line in lines_valid]
    print("dakshina valid pairs : ",len(lines_valid))

    pattern = '[^a-zA-Z]'       
    lines_valid = [line for line in lines_valid if not re.compile(pattern).search(line.split('\t')[1]) ]
    print("total valid pairs (removing words containing non-english characters) : ",len(lines_valid))

    lines_valid = [line for line in lines_valid if not re.compile(lang_patterns_test_valid_dict[lang_test_valid]).search(line.split('\t')[0]) ]
    print("total valid pairs (removing words containing non-hindi characters) : ",len(lines_valid))

    # filtering the test data

    lines_valid = [line for line in lines_valid if line]
    print("lines_valid size (valid) : ",len(lines_valid))
        
    lines_valid = list(set(lines_valid))
    print("lines_valid size (removed duplicates) : ",len(lines_valid))

    lines_valid = [line for line in lines_valid if len(line.split('\t'))==2 ]
    print("lines_valid size (ensuring 2 words in one line) : ",len(lines_valid))

    lines_valid = ['\t'.join([line.split('\t')[0]]+[line.split('\t')[1].lower()]) for line in lines_valid ]
    print("lines_valid size (converting english characters to small caps) : ",len(lines_valid))

    lines_valid = list(set(lines_valid))
    print("lines_valid size (removed duplicates after converting small caps) : ",len(lines_valid)) 


    print('separating parallel test corpus')
    # removing pairs by selecting romanize words in test and valid
    # separating parallel corpus
    lines_test_nat = [line.split('\t')[0] for line in lines_test]
    lines_test_rom = [line.split('\t')[1] for line in lines_test]

    # including spaces between characters
    lines_test_nat = [' '.join(list(line)) for line in lines_test_nat]
    lines_test_rom = [' '.join(list(line)) for line in lines_test_rom]

    print('writing files to the test corpus')
    # writing files to the corpus
    f_out_test_nat = open('../en-'+lang_abr_test_valid+'/corpus/test.'+lang_abr_test_valid,'w')
    f_out_test_rom = open('../en-'+lang_abr_test_valid+'/corpus/test.en','w')
    f_out_test_nat.write('\n'.join(lines_test_nat))
    f_out_test_rom.write('\n'.join(lines_test_rom))
    f_out_test_nat.close()
    f_out_test_rom.close()


    print('separating parallel valid corpus')
    # removing pairs by selecting romanize words in test and valid
    # separating parallel corpus
    lines_valid_nat = [line.split('\t')[0] for line in lines_valid]
    lines_valid_rom = [line.split('\t')[1] for line in lines_valid]

    # including spaces between characters
    lines_valid_nat = [' '.join(list(line)) for line in lines_valid_nat]
    lines_valid_rom = [' '.join(list(line)) for line in lines_valid_rom]

    print('writing files to the train corpus')
    # writing files to the corpus
    f_out_valid_nat = open('../en-'+lang_abr_test_valid+'/corpus/valid.'+lang_abr_test_valid,'w')
    f_out_valid_rom = open('../en-'+lang_abr_test_valid+'/corpus/valid.en','w')
    f_out_valid_nat.write('\n'.join(lines_valid_nat))
    f_out_valid_rom.write('\n'.join(lines_valid_rom))
    f_out_valid_nat.close()
    f_out_valid_rom.close()

    f_in_test.close()
    f_in_valid.close()
