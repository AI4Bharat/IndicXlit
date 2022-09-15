import re

lang_patterns_dict = {
    'Assamese' : "[\u0980-\u09FF]+",
    'Bangla' : "[\u0980-\u09FF]+",
    'Bodo' : "[\u0900-\u097F]+",
    'Konkani' : "[\u0900-\u097F]+", 
    'Gujarati' : "[\u0A80-\u0AFF]+",
    'Hindi' : "[\u0900-\u097F]+",
    'Kannada' : "[\u0C80-\u0CFF]+",
    'Kashmiri' : "[\u0600-\u089F]+",
    'Maithili' : "[\u0900-\u097F]+",
    'Malayalam' : "[\u0D00-\u0D7F]+",
    'Manipuri' : "[\uABC0-\uABFF]+",
    'Marathi' : "[\u0900-\u097F]+",
    'Nepali' : "[\u0900-\u097F]+",
    'Oriya' : "[\u0B00-\u0B7F]+",
    'Punjabi' : "[\u0A00-\u0A7F]+",
    'Sanskrit' : "[\u0900-\u097F]+",
    'Sindhi' : "[\u0600-\u06FF]+",
    'Sinhala' : "[\u0D80-\u0DFF]+",
    'Tamil' : "[\u0B80-\u0BFF]+",
    'Telugu' : "[\u0C00-\u0C7F]+",
    'Urdu' : "[\u0600-\u06FF]+",
    'Dogri' : "[\u0900-\u097F]+",
    'Santali' : "[\u1C50-\u1C7F]+"
}
lang_code_dict = {
    'as' : 'Assamese',
    'bn' : 'Bangla',
    'brx' : 'Bodo',
    'gom' : 'Konkani', 
    'gu' : 'Gujarati',
    'hi' : 'Hindi',
    'kn' : 'Kannada',
    'ks' : 'Kashmiri',
    'mai' : 'Maithili',
    'ml' : 'Malayalam',
    'mni_mei' : 'Manipuri',
    'mr' : 'Marathi',
    'ne' : 'Nepali',
    'or' : 'Oriya',
    'pa' : 'Punjabi',
    'sa' : 'Sanskrit',
    'sd' : 'Sindhi',
    'si' : 'Sinhala',
    'ta' : 'Tamil',
    'te' : 'Telugu',
    'ur' : 'Urdu',
    'dg' : 'Dogri',
    'sat' : 'Santali'
}
# lang_code_list = [
#     'as', 'brx', 'bn', 
#     'gom', 'gu', 'hi', 
#     'kn', 'mai', 'ml', 'mni', 'mr', 
#     'ne', 'or', 'pa', 'sa', 'sd', 
#     'ta', 'te', 'ks', 'ur'
#     ]
lang_code_list = ['as', 'bn', 'gom', 'gu', 
'hi', 'kn', 'ks', 'mai', 'ml', 'mni_mei', 'mr', 
'ne', 'or', 'pa', 'sa', 'sat', 'sd', 'ta', 'te']

for lang_code in lang_code_list:
    input_file_name = '../' +lang_code + '/'+lang_code + '_indic_tok.txt'
    file_in = open(input_file_name, 'r')
    lines_in = file_in.read().split('\n')

    word_list = []

    # tokenize word with mix language scripts e.g., 'भारतindia'
    # tokenize characters come along with numbers e.g., 'बोइंग737'
    final_pattern = lang_patterns_dict[lang_code_dict[lang_code]]
    for line in lines_in:
        word_list += re.findall(final_pattern, line)
    unique_word_list = list(set(word_list))
    
    unique_word_list = [ ' '.join(list(word)) for word in unique_word_list]

    output_file_name =  '../' + lang_code + '/' + lang_code + '_unique_word_list.txt'
    file_out = open(output_file_name, 'w')
    file_out.write('\n'.join(unique_word_list))
    file_out.close()
