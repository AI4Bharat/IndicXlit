
import re
import sys

# lang_abr = 'bn'
# lang = 'Bangla'

lang_abr = sys.argv[1]
lang = sys.argv[2]

lang_patterns_dict = {
                        'Assamese' : "[^\u0980-\u09FF]",
                        'Bangla' : "[^\u0980-\u09FF]",
                        'Konkani' : "[^\u0900-\u097F]", 
                        'Gujarati' : "[^\u0A80-\u0AFF]",
                        'Hindi' : "[^\u0900-\u097F]",
                        'Kannada' : "[^\u0C80-\u0CFF]",
                        'Kashmiri' : "[^\u0900-\u097F]",
                        'Maithili' : "[^\u0900-\u097F]",
                        'Malayalam' : "[^\u0D00-\u0D7F]",
                        'Marathi' : "[^\u0900-\u097F]",
                        'Nepali' : "[^\u0900-\u097F]",
                        'Oriya' : "[^\u0B00-\u0B7F]",
                        'Punjabi' : "[^\u0A00-\u0A7F]",
                        'Sanskrit' : "[^\u0900-\u097F]",
                        'Sindhi' : "[^\u0600-\u06FF]",
                        'Sinhala' : "[^\u0D80-\u0DFF]",
                        'Tamil' : "[^\u0B80-\u0BFF]",
                        'Telugu' : "[^\u0C00-\u0C7F]",
                        'Urdu' : "[^\u0600-\u06FF]"
}

data_resources = {
            'Assamese' : ['S','W'],
            'Bangla' : ['S','W','E'],
            'Konkani' : ['E'], 
            'Gujarati' : ['S','W','E'],
            'Hindi' : ['S','W','E'],
            'Kannada' : ['S','W','E'],
            'Kashmiri' : ['W'],
            'Maithili' : ['W','E'],
            'Malayalam' : ['S','W','E'],
            'Marathi' : ['S','W','E'],
            'Nepali' : ['W'],
            'Oriya' : ['S','W'],
            'Punjabi' : ['S','W','E'],
            'Sanskrit' : ['W'],
            'Sindhi' : ['W','E'],
            'Sinhala' : ['E'],
            'Tamil' : ['S','W','E'],
            'Telugu' : ['S','W','E'],
            'Urdu' : ['W','E']
}


print("lang : ",lang)

lines_train = []

if 'S' in data_resources[lang]:
    # samanantar train data
    f_samanantar_train = open('/home/yashkm/indic-xlit/all_data/samanantar/valid_pairs/'+lang_abr+'-en_valid.csv','r')
    lines_samanantar_train = f_samanantar_train.read().split('\n')
    lines_samanantar_train = ['\t'.join(line.split(',')) for line in lines_samanantar_train]
    lines_train += lines_samanantar_train
    print("samanantar train pairs: ",len(lines_samanantar_train))

if 'W' in data_resources[lang]:
    # wikidata train data
    f_wikidata_train = open('/home/yashkm/indic-xlit/all_data/wikidata/true_pairs/'+lang_abr+'.txt','r')
    lines_wikidata_train = f_wikidata_train.read().split('\n')
    lines_wikidata_train = ['\t'.join(line.split('|')[::-1]) for line in lines_wikidata_train]
    lines_train += lines_wikidata_train
    print("wikidata train pairs: ",len(lines_wikidata_train))

if 'E' in data_resources[lang]:
    # existing train data
    f_existing_train = open('/home/yashkm/indic-xlit/all_data/existing_data/Indic_Xlit_translit_parallel_corpus/'+lang+'/'+lang_abr+'_train.txt','r')
    lines_existing_train = f_existing_train.read().split('\n')
    lines_train += lines_existing_train
    print("existing train pairs: ",len(lines_existing_train))



# filtering the data
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


lines_train = [line for line in lines_train if not re.compile(lang_patterns_dict[lang]).search(line.split('\t')[0]) ]
print("total train pairs (removing words containing non-hindi characters) : ",len(lines_train))

lines_train = ['\t'.join([line.split('\t')[0]]+[line.split('\t')[1].lower()]) for line in lines_train ]
print("total train pairs (converting english characters to small caps) : ",len(lines_train))

lines_train = list(set(lines_train))
print("total train pairs (removed duplicates after converting small caps) : ",len(lines_train)) 

# test data
f_in_test = open('/home/yashkm/indic-xlit/corpus_org/dakshina_dataset_v1.0/'+lang_abr+'/lexicons/'+lang_abr+'.translit.sampled.test.tsv','r')
lines_test = f_in_test.read().split('\n')

lines_test = [line for line in lines_test if line]
print("Dakshina test pairs: ",len(lines_test))

# valid data
f_in_valid = open('/home/yashkm/indic-xlit/corpus_org/dakshina_dataset_v1.0/'+lang_abr+'/lexicons/'+lang_abr+'.translit.sampled.dev.tsv','r')
lines_valid = f_in_valid.read().split('\n')

lines_valid = [line for line in lines_valid if line]
print("Dakshina valid pairs: ",len(lines_valid))


print('removing test and valid data pairs from train data pairs if any (train_data - test_data), (train_data - valid_data)')
print(len(lines_train))    
# removing test and valid data pairs from train data pairs if any (train_data - test_data), (train_data - valid_data) 
lines_train = list( set(lines_train).difference( set( lines_test ) ) )
lines_train = list( set(lines_train).difference( set( lines_valid ) ) )
print(len(lines_train))

print('removing pairs by selecting romanize words in test and valid')
print("--separating train parallel corpus temporary")
# removing pairs by selecting romanize words in test and valid
# separating parallel corpus
temp_lines_train_nat = [line.split('\t')[0] for line in lines_train]
temp_lines_train_rom = [line.split('\t')[1] for line in lines_train]

print("--separating test parallel corpus")
# separating parallel corpus
lines_test_nat = [line.split('\t')[0] for line in lines_test]
lines_test_rom = [line.split('\t')[1] for line in lines_test]

print("--separating valid parallel corpus")
# separating parallel corpus
lines_valid_nat = [line.split('\t')[0] for line in lines_valid]
lines_valid_rom = [line.split('\t')[1] for line in lines_valid]

print('consolidating test and valid romanize and native words temporary')
# consolidating test and valid romanize and native words
temp_test_valid_nat = lines_valid_nat + lines_test_nat
temp_test_valid_rom = lines_valid_rom + lines_test_rom

print('removing romanized words and native words from train data with corresponding pairs')
print('--finding words which are in train,test and valid data.')
# removing romanized words and native words from train data with corresponding pairs
# finding words which are in train,test and valid data.
temp_test_valid_train_nat = list(set(temp_lines_train_nat).intersection(set(temp_test_valid_nat)))
temp_test_valid_train_rom = list(set(temp_lines_train_rom).intersection(set(temp_test_valid_rom)))
print("----native : ",len(temp_test_valid_train_nat))
print("----roman : ",len(temp_test_valid_train_rom))


print('--finding the list of indexes which has one or both romanized word and native word in training pairs')
print('----finding the list of indexes for native words')
# finding the list of indexes which has one or both romanized word and native word in training pairs
temp_indices_list = []
for temp_word_nat in temp_test_valid_train_nat:
    for word_pair_index in range(len(lines_train)):
        if temp_word_nat == lines_train[word_pair_index].split('\t')[0]: 
            temp_indices_list.append(word_pair_index)   
print('------native : ',len(temp_indices_list))

print('----finding the list of indexes for roman words')
for temp_word_rom in temp_test_valid_train_rom:
    for word_pair_index in range(len(lines_train)):
        if temp_word_rom == lines_train[word_pair_index].split('\t')[1]: 
            temp_indices_list.append(word_pair_index)
print('------native+roman : ',len(temp_indices_list))

print('----remove duplicates from temp_indices_list')
# remove duplicates
temp_indices_list = list(set(temp_indices_list))
print('------native+roman : ',len(temp_indices_list))


print('----sorting in descending order')
# sorting in descending way
temp_indices_list.sort(reverse=True)

print('--removing pairs from training data with corresponding indices')
print('----trian pairs : ',len(lines_train))
# removing pairs with corresponding indices
for temp_index in temp_indices_list:
    lines_train.pop(temp_index)
print('----trian pairs : ',len(lines_train))

print('separating parallel train corpus')
# removing pairs by selecting romanize words in test and valid
# separating parallel corpus
lines_train_nat = [line.split('\t')[0] for line in lines_train]
lines_train_rom = [line.split('\t')[1] for line in lines_train]

# including spaces between characters
lines_train_nat = [' '.join(list(line)) for line in lines_train_nat]
lines_train_rom = [' '.join(list(line)) for line in lines_train_rom]

print('writing files to the train corpus')
# writing files to the corpus
f_out_train_nat = open('../en-'+lang_abr+'/corpus/train.'+lang_abr,'w')
f_out_train_rom = open('../en-'+lang_abr+'/corpus/train.en','w')
f_out_train_nat.write('\n'.join(lines_train_nat))
f_out_train_rom.write('\n'.join(lines_train_rom))
f_out_train_nat.close()
f_out_train_rom.close()




# print('writing files to the test corpus')
# # including spaces between characters
# lines_test_nat = [' '.join(list(line)) for line in lines_test_nat]
# lines_test_rom = [' '.join(list(line)) for line in lines_test_rom]

# # writing files to the corpus
# f_out_test_nat = open('../en-'+lang_abr+'/corpus/test.'+lang_abr,'w')
# f_out_test_rom = open('../en-'+lang_abr+'/corpus/test.en','w')
# f_out_test_nat.write('\n'.join(lines_test_nat))
# f_out_test_rom.write('\n'.join(lines_test_rom))
# f_out_test_nat.close()
# f_out_test_rom.close()
f_in_test.close()


# print('writing files to the valid corpus')
# # including spaces between characters
# lines_valid_nat = [' '.join(list(line)) for line in lines_valid_nat]
# lines_valid_rom = [' '.join(list(line)) for line in lines_valid_rom]

# # writing files to the corpus
# f_out_valid_nat = open('../en-'+lang_abr+'/corpus/valid.'+lang_abr,'w')
# f_out_valid_rom = open('../en-'+lang_abr+'/corpus/valid.en','w')
# f_out_valid_nat.write('\n'.join(lines_valid_nat))
# f_out_valid_rom.write('\n'.join(lines_valid_rom))
# f_out_valid_nat.close()
# f_out_valid_rom.close()
f_in_valid.close()


