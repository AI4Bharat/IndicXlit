from collections import Counter
import pandas as pd
import csv
import time
import re

base = {
    'Assamese': u'['u'\U00000000-\U0000097F'u'\U000009E6-\U000009EF'u'\U000009F2-\U0010FFFF]+',
    'Bengali': u'['u'\U00000000-\U0000097F'u'\U000009E6-\U0010FFFF]+',
    'Gujarati': u'['u'\U00000000-\U00000A7F'u'\U00000AE4-\U0010FFFF]+',
    'Hindi': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'Konkani' : u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'Dogri': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'Kannada': u'['u'\U00000000-\U00000C7F'u'\U00000CE6-\U0010FFFF]+',
    'Malayalam': u'['u'\U00000000-\U00000CFF'u'\U00000D4E-\U00000D4F'u'\U00000D58-\U00000D5F'u'\U00000D66-\U00000D79'u'\U00000D80-\U0010FFFF]+',
    'Marathi': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'Odia': u'['u'\U00000000-\U00000AFF'u'\U00000B66-\U00000B6F'u'\U00000B72-\U0010FFFF]+',
    'Punjabi': u'['u'\U00000000-\U000009FF'u'\U00000A66-\U00000A6F'u'\U00000A74-\U0010FFFF]+',
    'Tamil': u'['u'\U00000000-\U00000B7F'u'\U00000BE6-\U0010FFFF]+',
    'Telugu': u'['u'\U00000000-\U00000BFF'u'\U00000C66-\U0010FFFF]+',
    'Manipuri': u'['u'\U00000000-\U0000ABBF'u'\U0000ABEE-\U0010FFFF]+',
    'Maithili': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'Nepali': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'Bodo': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    # 'en': u'['u'\U00000000-\U00000040'u'\U0000005B-\U00000060'u'\U0000007B-\U0010FFFF]+',
}
base1 = {
    'Assamese': u'['u'\U00000980-\U00000983'u'\U000009BC-\U000009D7]+',
    'Bengali': u'['u'\U00000980-\U00000983'u'\U000009BC-\U000009D7]+',
    'Gujarati': u'['u'\U00000A81-\U00000A83'u'\U00000ABC-\U00000ACD]+',
    'Hindi': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Konkani' : u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Dogri': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Kannada': u'['u'\U00000C80-\U00000C84'u'\U00000CBC-\U00000CD6'u'\U00000CE2-\U00000CE3]+',
    'Malayalam': u'['u'\U00000D00-\U00000D04'u'\U00000D3B-\U00000D4F'u'\U00000D62-\U00000D63]+',
    'Marathi': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Odia': u'['u'\U00000B01-\U00000B03'u'\U00000B3C-\U00000B57'u'\U00000B62-\U00000B63]+',
    'Punjabi': u'['u'\U00000A01-\U00000A03'u'\U00000A3C-\U00000A51'u'\U00000A70-\U00000A71]+',
    'Tamil': u'['u'\U00000B82-\U00000B83'u'\U00000BBE-\U00000BCD'u'\U00000BD7]+',
    'Telugu': u'['u'\U00000C00-\U00000C04'u'\U00000C3E-\U00000C56'u'\U00000C62-\U00000C63]+',
    'Manipuri': u'['u'\U0000ABE3-\U0000ABED]+',
    'Maithili': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Nepali': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Bodo': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'Kashmiri': u'['u'\U00000600–\U000006FF]+',
    'Urdu': u'['u'\U00000600–\U000006FF]+'
    # en':u'['u'\U00000980-\U00000983'u'\U000009BC-\U000009D7]+'
}
for lang in base.keys():
    start = time.time()
    Words = Counter({})
    newfile = f'/home/cs20m050/LDC-IL/{lang}_ldcil.txt'
    with open(newfile, 'r', encoding='utf-8', newline='') as file:
        text_file = file.read()
        split_text = filter(None, re.split(base[lang], text_file))
        Words = Counter(split_text)
        pattern = re.compile(base1[lang])
        with open(f'/home/cs20m050/LDC-IL/CSV/{lang}_Unique_list_with_freq.csv', 'w', encoding='utf-8', newline='') as outfile1:
            with open(f'/home/cs20m050/LDC-IL/CSV/{lang}_Word_char_list.csv', 'w', encoding='utf-8', newline='') as outfile2: #Query_model_on
                writer1 = csv.writer(outfile1)
                writer2 = csv.writer(outfile2)
                for word, freq in Words.items():
                    print(word)
                    test = pattern.sub('', word[0])
                    if test == word[0] and len(word) < 30 and len(word) > 2 and re.sub("\\S*(\\S)\\1\\1\\S*\\s?", "",word)  and 'ह्ह' not in word:
                        writer1.writerow([word, freq])
                        writer2.writerow([word.replace('',' ').strip()])
    end = time.time()
    print(f"Runtime = {end - start}")
