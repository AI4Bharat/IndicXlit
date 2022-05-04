import re

lang_abr_list = [ 'bn', 'gom', 'gu', 'hi', 'kn', 'mai', 'ml', 'mr', 'pa', 'sd', 'si', 'ta', 'te', 'ur']
lang_list = [ 'Bangla','Konkani' ,'Gujarati', 'Hindi', 'Kannada' ,'Maithili' ,'Malayalam', 'Marathi','Punjabi', 'Sindhi', 'Sinhala', 'Tamil', 'Telugu', 'Urdu']

all_lang_train_lines_nat = []
all_lang_train_lines_rom = []


for lang, lang_abr in zip(lang_list, lang_abr_list):
    

    print("lang : ",lang)

    f_in_train_nat = open('../en-'+lang_abr+'/corpus/train.'+lang_abr,'r')
    f_in_train_rom = open('../en-'+lang_abr+'/corpus/train.en','r')

    lines_train_nat = f_in_train_nat.read().split('\n')
    lines_train_rom = f_in_train_rom.read().split('\n')

    all_lang_train_lines_nat += lines_train_nat
    all_lang_train_lines_rom += lines_train_rom


    f_in_train_nat.close()
    f_in_train_rom.close()



print('writing files to the train corpus')
# writing files to the corpus
f_out_train_nat = open('../multi_lang/corpus/train.mlt','w')
f_out_train_rom = open('../multi_lang/corpus/train.en','w')
f_out_train_nat.write('\n'.join(all_lang_train_lines_nat))
f_out_train_rom.write('\n'.join(all_lang_train_lines_rom))
f_out_train_nat.close()
f_out_train_rom.close()


