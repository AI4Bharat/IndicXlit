import xlit_translit
import re
import timeit

lang_abr_test_valid_list = [ 'gu', 'hi', 'bn', 'kn', 'ml', 'mr', 'pa', 'ta', 'te']
lang_test_valid_list = ['Gujarati', 'Hindi', 'Bangla', 'Kannada', 'Malayalam', 'Marathi', 'Punjabi', 'Tamil', 'Telugu']
#lang_abr_test_valid_list = ['bn']
#lang_test_valid_list = ['Bangla']
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


NUM_SUGGESTIONS = 4

model = xlit_translit.Model('multi_lang', NUM_SUGGESTIONS, NUM_SUGGESTIONS)

file_out = open('results_analysis.txt', 'w')

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

    lines_test_native = [line.split('\t')[0] for line in lines_test]
    lines_test_roman = [line.split('\t')[1] for line in lines_test]

    start = timeit.default_timer()
    predictions = [model.translate_word(line, lang_abr_test_valid, rescore = True)[0] for line in lines_test_roman]
    end = timeit.default_timer()
    
    f_wrongly_predicted = open('experiment/wong_predicted_'+lang_abr_test_valid+'.txt','w')
    f_correct_predicted = open('experiment/correct_predicted_'+lang_abr_test_valid+'.txt','w')
    
    count = 0
    for pred, target, roman in zip(predictions, lines_test_native, lines_test_roman): 
        if pred==target:
            count+=1
            f_correct_predicted.write(roman+'\t'+target+'\t'+pred+'\n')
        else:
            f_wrongly_predicted.write(roman+'\t'+target+'\t'+pred+'\n')
    f_wrongly_predicted.close()
    f_correct_predicted.close()

    print(lang_abr_test_valid + ' : ' +str(count/len(lines_test_native)) )
    print("time elapsed for prediction : " , (end-start))

    file_out.write( lang_abr_test_valid + ' : ' +str(count/len(lines_test_native)) + ' : ' + str(end-start) +'\n')

file_out.close()
