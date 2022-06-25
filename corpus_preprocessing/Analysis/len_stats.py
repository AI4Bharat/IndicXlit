from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics
import glob
import time
import re

start = time.time()

langs = ["bn", "gu", "hi", "kn", "ml", "mr", "pa", "ta", "te"]
lang_dict = Counter()
avgdict = {}

for lang in langs:
    lang_dict[lang] = {}
    file = rf"C:\IIT - Madras\MTP\Lots and Lots of Data\dakshina_dataset_v1.0\dakshina_dataset_v1.0\{lang}\lexicons\{lang}.translit.sampled.test.tsv"
    df = pd.read_csv(file, header=None, sep='\t')#, usecols=[1], sep='\t')
    for row in df[0]:
        if len(row) in lang_dict[lang]:
            lang_dict[lang][len(row)] += 1
        else:
            lang_dict[lang][len(row)] = 1

    lang_dict[lang] = OrderedDict(sorted(lang_dict[lang].items()))

    print(lang_dict[lang].keys())
    total_len = 0
    for key, values in lang_dict[lang].items():
        total_len += (key * values)
    print(total_len)
    print(sum(lang_dict[lang].values()))
    avgdict[lang] = total_len / sum(lang_dict[lang].values())

print(avgdict)

end = time.time()
print(f'Runtime: {end - start}')