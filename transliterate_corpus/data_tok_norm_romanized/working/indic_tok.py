import re
lang_patterns_not_dict = {
    'Assamese' : "[^\u0980-\u09FF]+",
    'Bangla' : "[^\u0980-\u09FF]+",
    'Bodo' : "[^\u0900-\u097F]+",
    'Konkani' : "[^\u0900-\u097F]+", 
    'Gujarati' : "[^\u0A80-\u0AFF]+",
    'Hindi' : "[^\u0900-\u097F]+",
    'Kannada' : "[^\u0C80-\u0CFF]+",
    'Kashmiri' : "[^\u0600-\u089F]+",
    'Maithili' : "[^\u0900-\u097F]+",
    'Malayalam' : "[^\u0D00-\u0D7F]+",
    'Manipuri' : "[^\uABC0-\uABFF]+",
    'Marathi' : "[^\u0900-\u097F]+",
    'Nepali' : "[^\u0900-\u097F]+",
    'Oriya' : "[^\u0B00-\u0B7F]+",
    'Punjabi' : "[^\u0A00-\u0A7F]+",
    'Sanskrit' : "[^\u0900-\u097F]+",
    'Sindhi' : "[^\u0600-\u06FF]+",
    'Sinhala' : "[^\u0D80-\u0DFF]+",
    'Tamil' : "[^\u0B80-\u0BFF]+",
    'Telugu' : "[^\u0C00-\u0C7F]+",
    'Urdu' : "[^\u0600-\u06FF]+",
    'Dogri' : "[^\u0900-\u097F]+",
    'Santali' : "[^\u1C50-\u1C7F]+"
}
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
    'mni' : 'Manipuri',
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
#     'ta', 'te', 'ks'
#     ]

# lang_code_list = [ 'ur', 'dg', 'sat' ]
lang_code_list = ['as', 'bn', 'gom', 'gu', 
'hi', 'kn', 'ks', 'mai', 'ml', 'mni', 'mr', 
'ne', 'or', 'pa', 'sa', 'sat', 'sd', 'ta', 'te']

for lang_code in lang_code_list:
    input_file_name = '../../wikipedia_tok_norm/' +lang_code + '/'+lang_code + '_tok_norm.txt'
    file_in = open(input_file_name, 'r')
    lines_in = file_in.read().split('\n')


    # tokenize word with mix language scripts e.g., 'भारतindia'
    # tokenize characters come along with numbers e.g., 'बोइंग737'
    final_pattern = lang_patterns_dict[lang_code_dict[lang_code]] + '|' + lang_patterns_not_dict[lang_code_dict[lang_code]]
    lines_in = [ ' '.join(re.findall(final_pattern, line)) for line in lines_in ]
    
    # replace double spaces to single space
    lines_in = [ re.sub(' +', ' ', line) for line in lines_in ]
    
    
    output_file_name = '../' + lang_code + '/'+lang_code + '_indic_tok.txt'
    file_out = open(output_file_name, 'w')
    file_out.write('\n'.join(lines_in))
    file_out.close()