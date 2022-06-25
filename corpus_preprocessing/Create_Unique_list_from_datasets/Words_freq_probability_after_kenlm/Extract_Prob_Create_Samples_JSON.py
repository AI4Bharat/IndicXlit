import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np
import time
import math
import glob
import json
import csv

LDCIL_mapping= {
    'as': 'Assamese',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kok': 'Konkani',
    'doi': 'Dogri',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'or': 'Odia',
    'pa': 'Punjabi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mni': 'Manipuri',
    'mai': 'Maithili',
    'ne': 'Nepali',
    'brx':'Bodo',
    'sa':'Sanskrit',
    'ks':'Kashmiri',
    'ur':'Urdu'
}
# Lang = ['ml', 'or', 'pa', 'ta', 'te']# 'bn', 'gu']
# Lang = ['bn','gu','hi', 'mr', 'sa']
# Lang = ['kok', 'mai']
Lang = ['ne', 'brx', 'ks']
# Lang = ['mni']
sample_size = 5000
variants_required = 4

for lang in Lang:
    prob_file = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Words with Prob - 07 Dec 21/temp_sp_Model_tok_{lang}_{lang}_prob.csv'
    words_with_freq = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Words with Freq - 07 Dec 21/temp_sp_Model_files_tokenizer_Unique_list_with_freq_{lang}.csv'
    words_freq_prob = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/word_freq_probs/{lang}.csv'
    sample_csv = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Data/PB_fifth_2K_uniform_task/{lang}_pb.csv'
    sample_json = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Data/Third_task_2k_freq/JSON/{lang}_sskls.json'

    start = time.time()
    prob_list = []
    with open(prob_file, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        for word in reader:
            if word[0][0] == 'P' or word[0][0] == 'O' or word[0][0] == 'T':
                continue 
            prob = len(word[0].split())
            prob_list.append(10 ** (float(word[0].split()[prob - 3])))

    df_temp = pd.DataFrame(prob_list)
    length = len(prob_list)

    col1 = pd.read_csv(words_with_freq, header=None)
    df = pd.concat([col1, df_temp], axis=1, ignore_index= True)
    df.iloc[:, 0] = df.iloc[:, 0].astype(str).apply(lambda x: x.replace(' ', ''))


    #Check list part
    # check_list = []
    # folder = glob.glob(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/check_list/{lang}/*.csv')
    # for file in folder:
    #     temp = pd.read_csv(file, usecols=[0], header=None)[0].tolist()
    #     check_list.extend(temp)
    # print(len(check_list))

    # with open(prob_file, 'r', encoding='utf-8', newline='') as file:
    #     reader = csv.reader(file)
    #     for word in reader:
    #         if word[0][0] == 'P' or word[0][0] == 'O' or word[0][0] == 'T':
    #             continue 
    #         prob = len(word[0].split())
    #         prob_list.append(10 ** (float(word[0].split()[prob - 3])))

    # df_temp = pd.DataFrame(prob_list)
    # length = len(prob_list)

    #Removing checklist words
    # col1 = pd.read_csv(words_with_freq, header=None)

    # df = pd.concat([col1, df_temp], axis=1, ignore_index= True)
    # print(len(df))
    # df = df[~df[0].isin(check_list)]
    # print(len(df))
    # df.iloc[:, 0] = df.iloc[:, 0].astype(str).apply(lambda x: x.replace(' ', ''))


    # #***** Normalize *****#

    df[len(df.columns)] = df.iloc[:, 0:3].apply(lambda x: x[2] ** (1/len(x[0])), axis=1)
    maxi = max(df.iloc[:, 3])
    df.iloc[:, 3] = df.iloc[:, 3].apply(lambda x: x/maxi)
    df.to_csv(words_freq_prob, header=False, index=False)
    df = pd.read_csv(words_freq_prob, header=None)
    data = sorted(df.to_numpy(), key= lambda x: x[1], reverse=True)
    print(len(data))

    myxticks = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']
    decile_dict = {key: [] for key in myxticks}

    for num in range(len(data)):
        if len(data[num][0]) <= 20 and 'एक्सएक्स' not in data[num][0] and 'डब्ल्यूडब्ल्यू' not in data[num][0]:
            if data[num][3] > 0 and data[num][3] <= 0.1:
                key = '0.1'
            elif data[num][3] > 0.1 and data[num][3] <= 0.2:
                key = '0.2'
            elif data[num][3] > 0.2 and data[num][3] <= 0.3:
                key = '0.3'
            elif data[num][3] > 0.3 and data[num][3] <= 0.4:
                key = '0.4'
            elif data[num][3] > 0.4 and data[num][3] <= 0.5:
                key = '0.5'
            elif data[num][3] > 0.5 and data[num][3] <= 0.6:
                key = '0.6'
            elif data[num][3] > 0.6 and data[num][3] <= 0.7:
                key = '0.7'
            elif data[num][3] > 0.7 and data[num][3] <= 0.8:
                key = '0.8'
            elif data[num][3] > 0.8 and data[num][3] <= 0.9:
                key = '0.9'
            elif data[num][3] > 0.9 and data[num][3] <= 1:
                key = '1.0'
            decile_dict[key].append(data[num][0])

    plt.bar(range(len(decile_dict)), list(len(value) for key, value in decile_dict.items()), align='center')

    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i], y[i], ha = 'center', fontsize=10)

    addlabels(decile_dict, list(len(value) for key, value in decile_dict.items()))

    plt.title(f"Decile vs Number of Words - {lang}")
    plt.xlabel("Decile")
    plt.ylabel("Number of Words")
    plt.xticks(range(len(decile_dict)), myxticks, fontsize=10)
    plt.show()

    words_list = []
    total_words_required = sample_size
    bin_count = 10

    for bin, words in decile_dict.items():

        if len(words) < sample_size//10:
            for word in words:
                words_list.append(word)
            bin_count -= 1
            print(bin, len(words_list))
    total_words_required = sample_size - len(words_list)
    print(total_words_required)

    sample_no_of_words = math.ceil(total_words_required / bin_count)
    print(sample_no_of_words)

    for bin, words in decile_dict.items():
        if len(words) < sample_no_of_words and len(words) >= sample_size//10:
            for word in words:
                words_list.append(word)
            bin_count -= 1
            print(bin, len(words_list))
    total_words_required = sample_size - len(words_list)
    print(total_words_required)

    sample_no_of_words = math.ceil(total_words_required / bin_count)
    print(sample_no_of_words)

    for bin, words in decile_dict.items():
        if len(words) >= sample_no_of_words:
            Words = random.sample(words, sample_no_of_words)
            for word in Words:
                words_list.append(word)
                # words.remove(word)
                # df.drop(df.loc[df[0]==word].index, inplace=True)
            print(bin, len(words_list), sample_no_of_words)

    print(len(words_list))

    if len(words_list) > sample_size:
        delete_word = random.sample(words_list, len(words_list) - sample_size)
        for word in delete_word:
            words_list.remove(word)

    print(len(words_list))

    # For Frequent data
    # words_list = []
    # for word in range(sample_size):
    #     words_list.append(data[word][0])


    df = df[~df[0].isin(words_list)] #it will remove the sampled words from the file.
    print(len(df)) 
    df.to_csv(words_freq_prob, header=False, index=False)

    limit = [variants_required for _ in range(len(words_list))]
    pd.DataFrame(zip(words_list, limit)).to_csv(sample_csv, index=False, header=["word", "limit"])
    jsonArray = []

    with open(sample_csv, encoding='utf-8', newline='') as csvf: 
                csvReader = csv.DictReader(csvf) 
                for row in csvReader: 
                    jsonArray.append(row)
    with open(sample_json, 'w', encoding='utf-8', newline='') as jsonf: 
            jsonString = json.dumps(jsonArray, ensure_ascii= False, indent=4)
            jsonf.write(jsonString)

    end = time.time()
    print(f'Runtime: {end - start}')