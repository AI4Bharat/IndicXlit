from collections import Counter
import pandas as pd
import glob
import time
import csv
import re

base = {
    'as': u'['u'\U00000980-\U00000983'u'\U000009BC-\U000009D7]+',
    'bn': u'['u'\U00000980-\U00000983'u'\U000009BC-\U000009D7]+',
    'gu': u'['u'\U00000A81-\U00000A83'u'\U00000ABC-\U00000ACD]+',
    'hi': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'kn': u'['u'\U00000C80-\U00000C84'u'\U00000CBC-\U00000CD6'u'\U00000CE2-\U00000CE3]+',
    'ml': u'['u'\U00000D00-\U00000D04'u'\U00000D3B-\U00000D4F'u'\U00000D62-\U00000D63]+',
    'mr': u'['u'\U00000900-\U00000903'u'\U0000093A-\U0000094F'u'\U00000962-\U00000963]+',
    'or': u'['u'\U00000B01-\U00000B03'u'\U00000B3C-\U00000B57'u'\U00000B62-\U00000B63]+',
    'pa': u'['u'\U00000A01-\U00000A03'u'\U00000A3C-\U00000A51'u'\U00000A70-\U00000A71]+',
    'ta': u'['u'\U00000B82-\U00000B83'u'\U00000BBE-\U00000BCD'u'\U00000BD7]+',
    'te': u'['u'\U00000C00-\U00000C04'u'\U00000C3E-\U00000C56'u'\U00000C62-\U00000C63]+',
    # 'en': u'['u'\U00000980-\U00000983'u'\U000009BC-\U000009D7]+'
}

for lang in base.keys():
    dataframe1 = pd.read_csv(f'home/cs20m050/SWE_data/{lang}/{lang}_swe.csv', header=None)
    swe = Counter(dict.fromkeys(dataframe1[0].to_list(), 1))

    length = len(glob.glob(f'/home/cs20m050/Text/{lang}/{lang}.*.csv'))

    start = time.time()
    mybigdict = Counter()
    mybigdict_temp = Counter()

    for i in range(0, length):
        with open(f'/home/cs20m050/Text/{lang}/{lang}.' + str(i) + '.csv', 'r', encoding='utf-8', newline='') as infile:
            reader = csv.reader(infile)
            mysmalldict = {rows[0]:int(rows[1]) for rows in reader}
            mybigdict += Counter(mysmalldict)

    pattern = re.compile(base[lang])
    mylist = []

    mybigdict_temp = mybigdict + swe
    for key in list(mybigdict):
        if mybigdict[key] != mybigdict_temp[key]:
            del mybigdict[key]

    mybigdict = mybigdict.most_common()
    mybigdict_temp = mybigdict_temp.most_common()

    with open(f'/home/cs20m050/Unique_lists/Unique_list_with_freq/{lang}.csv', 'w', encoding='utf-8', newline='') as outfile1:
        with open(f'/home/cs20m050/Unique_lists/Word_char_list_wo_swe/{lang}.csv', 'w', encoding='utf-8', newline='') as outfile2: #Query_model_on
            writer1 = csv.writer(outfile1)
            writer2 = csv.writer(outfile2)
            for word in mybigdict:
                test = pattern.sub('', word[0][0])
                if word[1] != 1 and test == word[0][0] and len(word[0]) < 30 and len(word[0]) > 2 and re.sub("\\S*(\\S)\\1\\1\\S*\\s?", "",word[0])  and 'ह्ह' not in word[0]:
                    writer1.writerow([word[0], word[1]])
                    writer2.writerow([word[0].replace('',' ').strip()])
    with open(f'/home/cs20m050/Unique_lists/Word_char_list/{lang}.csv', 'w', encoding='utf-8', newline='') as outfile3: #Train_model_on
        writer3 = csv.writer(outfile3)
        for word in mybigdict_temp:
            test = pattern.sub('', word[0][0])
            if word[1] != 1 and test == word[0][0] and len(word[0]) < 30 and len(word[0]) > 2 and re.sub("\\S*(\\S)\\1\\1\\S*\\s?", "",word[0])  and 'ह्ह' not in word[0]:
                writer3.writerow([word[0].replace('',' ').strip()])

    end = time.time()

    print(f'Runtime = {end - start}')
