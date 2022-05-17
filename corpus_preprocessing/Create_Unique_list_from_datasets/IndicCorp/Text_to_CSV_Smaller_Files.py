from collections import Counter
import pandas as pd
import glob
import cld3
import time
import re

base = {
    'as': u'['u'\U00000000-\U0000097F'u'\U000009E6-\U000009EF'u'\U000009F2-\U0010FFFF]+',
    'bn': u'['u'\U00000000-\U0000097F'u'\U000009E6-\U0010FFFF]+',
    'gu': u'['u'\U00000000-\U00000A7F'u'\U00000AE4-\U0010FFFF]+',
    'hi': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'kn': u'['u'\U00000000-\U00000C7F'u'\U00000CE6-\U0010FFFF]+',
    'ml': u'['u'\U00000000-\U00000CFF'u'\U00000D4E-\U00000D4F'u'\U00000D58-\U00000D5F'u'\U00000D66-\U00000D79'u'\U00000D80-\U0010FFFF]+',
    'mr': u'['u'\U00000000-\U000008FF'u'\U00000964-\U0010FFFF]+',
    'or': u'['u'\U00000000-\U00000AFF'u'\U00000B66-\U00000B6F'u'\U00000B72-\U0010FFFF]+',
    'pa': u'['u'\U00000000-\U000009FF'u'\U00000A66-\U00000A6F'u'\U00000A74-\U0010FFFF]+',
    'ta': u'['u'\U00000000-\U00000B7F'u'\U00000BE6-\U0010FFFF]+',
    'te': u'['u'\U00000000-\U00000BFF'u'\U00000C66-\U0010FFFF]+'
    # 'en': u'['u'\U00000000-\U00000040'u'\U0000005B-\U00000060'u'\U0000007B-\U0010FFFF]+',
}

for lang in base.keys():
    length = len(glob.glob(f'/home/cs20m050/Text/{lang}/{lang}.txt.*'))
    start = time.time()
    Words = Counter({})

    for i in range(0, length):
        print(i)
        newfile = f'/home/cs20m050/Text/{lang}/{lang}.txt.{str(i)}'
        with open(newfile, 'r', encoding='utf-8', newline='') as file:
            text_file = file.read()
            split_text = filter(None, re.split(base[lang], text_file))
            Words = Counter(split_text)
            (pd.DataFrame.from_dict(data=Words, orient='index')
            .to_csv(f'/home/cs20m050/Text/{lang}/{lang}.{str(i)}.csv', header=False))

    end = time.time()
    print(f"Runtime = {end - start}")
