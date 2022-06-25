import json
import pandas as pd
import csv
from zipfile import ZipFile
from os import path
import os
import zipfile

from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
# from urduhack import normalize
import csv
import json
import numpy as np
import pandas as pd
import time
import glob


data_resources = {
    'Assamese' : ['I','S','W','M'],
    'Bengali' : ['I','S','W','M','D','Br','F'],
    'Bodo' : ['I','M'],
    'Konkani' : ['I','Br','M','AI'],
    'Gujarati' : ['I','S','W','M','D','Br','F'],
    'Hindi' : ['I','S','W','M','D','AI','XC','XB','Br','F'],
    'Kannada' : ['I','S','W','M','D'],
    'Kashmiri' : ['I','W','M'],
    'Maithili' : ['I','W','AI','M'],
    'Malayalam' : ['I','S','W','Br','M','D'],
    'Manipuri' : ['I','M'],
    'Marathi' : ['I','S','W','Br','M','D'],
    'Nepali' : ['I','W','M'],
    'Oriya' : ['I','S','W','M'],
    'Punjabi' : ['I','S','W','Br','M','D'],
    'Sanskrit' : ['I','W','M'],
    'Sindhi' : ['I','W','E','D'],
    # 'Sinhala' : ['E','D'],
    'Tamil' : ['I','S','W','Br','M','D'],
    'Telugu' : ['I','S','W','Br','M','D','NAI'],
    'Urdu' : ['I','W','Br','M','D']
}

mapping= {
    'as': 'Assamese',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'kok': 'Konkani',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'or': 'Oriya',
    'pa': 'Punjabi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'mni': 'Manipuri',
    'mai': 'Maithili',
    'ne': 'Nepali',
    'brx':'Bodo',
    'ks': 'Kashmiri',
    'sa':'Sanskrit',
    'sd': 'Sindhi',
    'ur':'Urdu'
}

map_3 = {
    'as': 'asm',
    'bn': 'ben',
    'gu': 'guj',
    'hi': 'hin',
    'kok': 'kok',
    'kn': 'kan',
    'ml': 'mal',
    'mr': 'mar',
    'or': 'ori',
    'pa': 'pan',
    'ta': 'tam',
    'te': 'tel',
    'mni': 'mni',
    'mai': 'mai',
    'ne': 'nep',
    'brx':'brx',
    'ks': 'kas',
    'sa':'san',
    'sd': 'sid',
    'ur':'urd'
}

norm = {
    'mai':'hi',
    'brx':'hi',
    'kok':'kK',
    'as': 'as',
    'bn': 'bn',
    'gu': 'gu',
    'hi': 'hi',
    'kn': 'kn',
    'ml': 'ml',
    'mr': 'mr',
    'or': 'or',
    'pa': 'pa',
    'ta': 'ta',
    'te': 'te',
    'ne': 'ne',
    'sa':'sa',
    'sd': 'sd',
}

# Lang = ['hi','gu','mr','pa','ta','te','ur','bn','ml','mai','kok']
Lang = []
# Train
for lang in Lang:
    all_data = list()
    start = time.time()
    print(f"{mapping[lang]}")

    if lang not in ['ur','ks','mni']:
        normalizer_factory = IndicNormalizerFactory()
        normalizer = normalizer_factory.get_normalizer(norm[lang])
    if 'D' in data_resources[mapping[lang]]:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Dakshina/{lang}/lexicons/{lang}.translit.sampled.train.tsv') as D:
            Dakshina = list([(row[0],row[1].lower()) for row in csv.reader(D, delimiter ='\t')])
            if lang in ['ur']:
                # Dakshina = [(normalize(tup[0]), tup[1]) for tup in Dakshina]
                pass
            else:
                Dakshina = [(normalizer.normalize(tup[0]), tup[1]) for tup in Dakshina]
            print("Total_words D:" + str(len(Dakshina)))

    #### Existing
   
    if 'AI' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/Existing/{lang}/AI4B-StoryWeaver_{lang}_train.txt') as E:
            AI = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                AI = [(normalizer.normalize(tup[0]), tup[1]) for tup in AI]

            print("Total_words AI:" + str(len(AI)))
    
    if 'XB' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/Existing/{lang}/Xlit-IITB-Par_{lang}.txt') as E:
            XB = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                XB = [(normalizer.normalize(tup[0]), tup[1]) for tup in XB]

            print("Total_words:" + str(len(XB)))

    if 'Br' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/Existing/{lang}/Brahminet_{lang}.txt') as E:
            Br = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                Br = [(normalizer.normalize(tup[0]), tup[1]) for tup in Br]

            print("Total_words Br:" + str(len(Br)))

    if 'XC' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/Existing/{lang}/Xlit-Crowd_{lang}.txt') as E:
            XC = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                XC = [(normalizer.normalize(tup[0]), tup[1]) for tup in XC]

            print("Total_words:" + str(len(XC)))

    if 'F' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/Existing/{lang}/FIRE-2013-Track_{lang}.txt') as E:
            # for i in csv.reader(E, delimiter ='\t'):
            #     print(i[0])
            F = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                F = [(normalizer.normalize(tup[0]), tup[1]) for tup in F]

            print("Total_words:" + str(len(F)))

    if 'NAI' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/Existing/{lang}/NotAI-tech_{lang}_train.txt') as E:
            NAI = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                NAI = [(normalizer.normalize(tup[0]), tup[1]) for tup in NAI]

            print("Total_words:" + str(len(NAI)))


    ####
    if 'M' in data_resources[mapping[lang]]:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/train_set/{lang}_train.txt') as B:
            BenchMark = list([(row[0],row[1].lower()) for row in csv.reader(B, delimiter ='\t')])
            
            if lang in ['ur']:
                # BenchMark = [(normalize(tup[0]), tup[1]) for tup in BenchMark]
                pass
            
            else:
                BenchMark = [(normalizer.normalize(tup[0]), tup[1]) for tup in BenchMark]
            
            print("Total_words:" + str(len(BenchMark)))
            with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/Categorised_data/uniform/{lang}.csv') as U:
                Uniform = [word[0] for word in csv.reader(U)]
                if lang in ['ur']:
                    # Uniform = [normalize(tup[0]) for tup in Uniform]
                    pass
                else:
                    Uniform = [normalizer.normalize(tup[0]) for tup in Uniform]
                
                print("Total_words:" + str(len(Uniform)))
    if 'W' in data_resources[mapping[lang]]:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/wikidata/true_pairs/{lang}.txt') as W:
            Wiki = list([(row[1],row[0].lower()) for row in csv.reader(W, delimiter ='|')])
            if lang in ['ur']:
                # Wiki = [(normalize(tup[0]), tup[1]) for tup in Wiki]
                pass
            else:
                Wiki = [(normalizer.normalize(tup[0]), tup[1]) for tup in Wiki]
            print("Total_words:" + str(len(Wiki)))
    if 'S' in data_resources[mapping[lang]]:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/samanantar/valid_pairs/{lang}-en_valid.csv') as S:
            Samanantar = list([(row[0],row[1].lower()) for row in csv.reader(S, delimiter =',')])
            if lang in ['ur']:
                # Samamantar = [(normalize(tup[0]), tup[1]) for tup in Samanantar]
                pass
            else:
                Samamantar = [(normalizer.normalize(tup[0]), tup[1]) for tup in Samanantar]
            
            print("Total_words:" + str(len(Samanantar)))
    if 'I' in data_resources[mapping[lang]]:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/indiccorp/threshold_0_35_files/translit_pairs_with_avg_score_thr_035_{lang}.txt') as I:
            IndicCorp = list([(row[0],row[1].lower(),row[2]) for row in csv.reader(I, delimiter ='\t')])
            
            if lang in ['ur']:
                # IndicCorp = [(normalize(tup[0]), tup[1], tup[2]) for tup in IndicCorp]
                pass
            else:
                IndicCorp = [(normalizer.normalize(tup[0]), tup[1], tup[2]) for tup in IndicCorp]
            
            print("Total_words:" + str(len(IndicCorp)))
            with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/corpus/en-{lang}/corpus/train.{lang}') as F1:
                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/corpus/en-{lang}/corpus/train.en') as F2:
                    r1 = csv.reader(F1)
                    r2 = csv.reader(F2)             
                    ind_word_list = ["".join(word).replace(" ","") for word in r1]
                    en_word_list = ["".join(word).replace(" ","") for word in r2]
                    pair = list(zip(ind_word_list,en_word_list))

                    df = pd.DataFrame(pair)
                    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_all_data.csv', index=False)

                    print("Pairs Left: " + str(len(pair)))

                    # Dakshina_Pairs
                    if 'D' in data_resources[mapping[lang]]:
                        D = [k for k in set(Dakshina).intersection(pair)]
                        print(len(D))
                        all_data.extend([a+("Dakshina",None) for a in D])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(D)))
                        print("Pairs Left: " + str(len(pair)))

                    # Benchmark_Pairs
                    if 'M' in data_resources[mapping[lang]]:
                        B = [k for k in set(BenchMark).intersection(pair)]
                        print(len(B))
                        B_U = [k for k in B if k[0] in Uniform]
                        print(len(B_U))
                        all_data.extend([a+("AK-Uni",None) for a in B_U])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(B_U)))
                        print("Pairs Left: " + str(len(pair)))
                        B = (set(B).difference(set(B_U)))
                        print(len(B))
                        all_data.extend([a+("AK-Freq",None) for a in B])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(B)))
                        print("Pairs Left: " + str(len(pair)))

                    # Existing_Pairs

                    if 'AI' in data_resources[mapping[lang]]:
                        E = [k for k in set(AI).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("AI4B-StoryWeaver",None) for a in E])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(E)))
                        print("Pairs Left: " + str(len(pair)))

                    if 'XC' in data_resources[mapping[lang]]:
                        E = [k for k in set(XC).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("Xlit-Crowd",None) for a in E])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(E)))
                        print("Pairs Left: " + str(len(pair)))
                    
                    if 'XB' in data_resources[mapping[lang]]:
                        E = [k for k in set(XB).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("Xlit-IITB-Par",None) for a in E])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(E)))
                        print("Pairs Left: " + str(len(pair)))
                    
                    if 'Br' in data_resources[mapping[lang]]:
                        E = [k for k in set(Br).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("Brahminet",None) for a in E])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(E)))
                        print("Pairs Left: " + str(len(pair)))
                    
                    if 'F' in data_resources[mapping[lang]]:
                        E = [k for k in set(F).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("FIRE-2013-Track",None) for a in E])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(E)))
                        print("Pairs Left: " + str(len(pair)))
                    
                    if 'NAI' in data_resources[mapping[lang]]:
                        E = [k for k in set(NAI).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("NotAI-tech",None) for a in E])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(E)))
                        print("Pairs Left: " + str(len(pair)))

                    # Wikidata_Pairs
                    if 'W' in data_resources[mapping[lang]]:
                        W = [k for k in set(Wiki).intersection(pair)]
                        print(len(W))
                        all_data.extend([a+("Wikidata",None) for a in W])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(W)))
                        print("Pairs Left: " + str(len(pair)))

                    # Samanantar_Pairs
                    if 'S' in data_resources[mapping[lang]]:
                        S = [k for k in set(Samanantar).intersection(pair)]
                        print(len(S))
                        all_data.extend([a+("Samanantar",None) for a in S])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(S)))
                        print("Pairs Left: " + str(len(pair)))


                    # IndicCorp_Pairs
                    if 'I' in data_resources[mapping[lang]]:
                        Slice = {row[:2]:row[2] for row in IndicCorp}
                        # print(Slice)
                        I = [k for k in set(Slice.keys()).intersection(pair)]
                        print(len(I))
                        all_data.extend([a+("IndicCorp",eval(Slice[a])) for a in I])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(I)))
                        print("Pairs Left: " + str(len(pair)))
                    df = pd.DataFrame(pair)
                    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_left_existing.csv', index=False)
    
    ind = [f'{map_3[lang]}'+str(index) for index in range(1,len(all_data))]
    # print(ind[0], ind[-1])
    all_data = [(ind[i-1],) + all_data[i] for i in range(1,len(all_data))]
    # print(all_data)
    df = pd.DataFrame(all_data, columns=["unique_identifier", "native word", "english word", "source", "score"])
    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_final_data_existing.csv', index=False)
    # Create a multiline json
    json_list = json.loads(df.to_json(orient = "records"))

    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/JSONL/{map_3[lang]}/{map_3[lang]}_existing_train.json', 'w', encoding='utf-8') as f:
        for item in json_list:
            f.write("%s\n" % json.dumps(item, ensure_ascii=False))
    end = time.time()
    print(f"{mapping[lang]}:" + str(end-start))


def create_zip(file_name, file_dir):
    """
    Function to create zip archive
    """
    os.chdir(file_dir)
    zipfiles_list = ['data.json', 'params.json']
    file_name_part = file_name
    zip_name = '{0}.zip'.format(file_name_part)
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        # for file_extension in zipfiles_list:
        #     full_file_path = '{1}'.format(file_name_part, file_extension)
        zip_archive.write('data.json')
        zip_archive.write('params.json')


map_2 = {
    'asm': 'as',
    'ben': 'bn',
    'guj': 'gu', 
    'hin': 'hi', 
    'kok': 'kok', 
    'kan': 'kn', 
    'mal': 'ml', 
    'mar': 'mr', 
    'ori': 'or', 
    'pan': 'pa', 
    'tam': 'ta', 
    'tel': 'te',
    'mni': 'mni',
    'mai': 'mai',
    'nep': 'ne',
    'brx': 'brx',
    'kas': 'ks',
    'san': 'sa',
    'sid': 'sd',
    'urd': 'ur',
} 

split = 'train'


Lang = ['ben','guj','hin','kok','mai','mal','mar','pan','tam','tel','urd']

with open (f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ULCA/ULCA_IndicXlit_existing_{split}.csv', 'w') as stats:
    w = csv.writer(stats)
    w.writerow(['S.No','Source','Pair','DatasetName','Link'])
    S = 1
    for lang in Lang:
        jsonArray = []
        source = {}
        #JSONL files from Aksharantar(spliting existing sources)
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/JSONL/{lang}/{lang}_existing_{split}.json','r') as JSONL:
            List = list(JSONL)
        for pair in List:
            dict = json.loads(pair)    

            try:
                if dict["source"] == "IndicCorp":
                    source[dict["source"]].append([dict["english word"],dict["native word"],dict["score"]])
                else:
                    source[dict["source"]].append([dict["english word"],dict["native word"]])
            except KeyError:
                source[dict["source"]] = []
                if dict["source"] == "IndicCorp":
                    source[dict["source"]].append([dict["english word"],dict["native word"],dict["score"]])
                else:
                    source[dict["source"]].append([dict["english word"],dict["native word"]])
        for i in source.keys():
            jsonArray = source[i]
            words = []

            CSV = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/CSV/{i}_{split}_en_{map_2[lang]}_existing.csv'

            data = f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/{split}/{map_2[lang]}/data.json'

            if i == "IndicCorp":
                pd.DataFrame(jsonArray).to_csv(CSV, index=False, header=["sourceText","targetText","scores"])
                with open(CSV, encoding='utf-8', newline='') as csvf:
                    words = [
                        {
                            "sourceText": row["sourceText"],
                            "targetText": row["targetText"],
                            "collectionMethod": {
                                "collectionDetails": {
                                    "alignmentScore": eval(row["scores"])
                                }
                             }
                        }
                        for row in csv.DictReader(csvf)
                    ]
            else:

                pd.DataFrame(jsonArray).to_csv(CSV, index=False, header=["sourceText","targetText"])

                with open(CSV, encoding='utf-8', newline='') as csvf: 
                    csvReader = csv.DictReader(csvf) 
                    for row in csvReader:
                        words.append(row)

            with open(data, 'w', encoding='utf-8', newline='') as jsonf: 
                jsonString = json.dumps(words, ensure_ascii= False, indent=4)
                jsonf.write(jsonString)
            w.writerow([S,i,f'en_{map_2[lang]}',f'{i}_{split}_en_{map_2[lang]}',f'https://storage.cloud.google.com/indic-xlit-public/ulca/{split}/{map_2[lang]}/{i}_{split}_en_{map_2[lang]}.zip'])
            S+=1

            #params.json
            if i == 'Dakshina':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_dak.json', 'r')
                name = {
                f'{i}': f"{i} {split}set en-{map_2[lang]} Transliteration Data"}
            elif i == 'IndicCorp':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_ic.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}
            elif i == 'Samanantar':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_sam.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}
            elif i == 'Wikidata':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_wiki.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}
            
            elif i == 'Xlit-Crowd':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_xc.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}

            elif i == 'Xlit-IITB-Par':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_xb.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}
            
            elif i == 'Brahminet':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_b.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}
            
            elif i == 'FIRE-2013-Track':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_f.json', 'r')
                name = {
                f'{i}': f"{i} en-{map_2[lang]} Transliteration Data"}
            
            elif i == 'AI4B-StoryWeaver':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_a.json', 'r')
                name = {
                f'{i}': f"{i} trainset en-{map_2[lang]} Transliteration Data"}
            
            elif i == 'NotAI-tech':
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params_na.json', 'r')
                name = {
                f'{i}': f"{i} trainset en-{map_2[lang]} Transliteration Data"}
            
            else:
                params = open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/params.json', 'r')
                name = {
                f'{i}': f"Aksharantar ({i}) en-{map_2[lang]} Transliteration Data"}

            J = json.load(params)
        

            description = {
                'AK-Freq':f"This Data is a subset from the Aksharantar {split} set, and contains the most frequently-used words in the language in order to evaluate the performance of models on commonly-occurring vocabulary. For more details, refer our paper: https://arxiv.org/abs/2205.03018",
                'AK-Uni' :f"This Data is a subset from the Aksharantar {split} set, and contains the uniformly sampled words from the language in order to evaluate the performance of models on words with diverse n-gram i.e rare and also common words in the language. For more details, refer our paper: https://arxiv.org/abs/2205.03018",
                'AK-NEI' :f"This Data is a subset from the Aksharantar {split} set, and contains the words of Indian origin Named Entities in order to evaluate the performance of model on various groups of named entities from India. For more details, refer our paper: https://arxiv.org/abs/2205.03018",
                'AK-NEF' :f"This Data is a subset from the Aksharantar {split} set, and contains words of the Foreign origin Named Entities in order to evaluate the performance of model on various groups of Foreign named entities. For more details, refer our paper: https://arxiv.org/abs/2205.03018",
                'Dakshina'  :f"This Data is from the Dakshina {split} set, For more details, refer the paper: https://arxiv.org/abs/2007.01176",
                'IndicCorp' :f"This {split} subset contains the transliteration pairs mined from largest publicly available monolingual corpora, refer the papers: https://doi.org/10.48550/arXiv.2005.00085, https://arxiv.org/abs/2205.03018",
                'Samanantar':f"This {split} subset contains the transliteration pairs mined from largest publicly available parallel translation corpora, refer the papers: https://doi.org/10.48550/arXiv.2104.05596, https://arxiv.org/abs/2205.03018",
                'Wikidata'  :f"This {split} subset contains the transliteration pairs extracted from wikidata.",
                'Xlit-Crowd':"This train subset contains transliteration pairs obtained via crowdsourcing by asking workers to transliterate Hindi words into the Roman script, refer paper for more details: https://aclanthology.org/L14-1713/",
                'Xlit-IITB-Par':"This train subset contains Hindi-English Transliteration pairs mined from parallel translation corpora, refer paper for more details: https://www.cfilt.iitb.ac.in/iitb_parallel/lrec2018_iitbparallel.pdf",
                'FIRE-2013-Track':"This train subset contains the transliteration pairs sourced from dataset released as part of track 2013, refer paper for more details: https://www.isical.ac.in/~fire/wn/STTS/2013-translit_search-track_overview.pdf",
                'Brahminet':"This train subset contains the transliteration pairs from publicly available Brahminet corpus, refer paper for more details: https://aclanthology.org/N15-3017/",
                'AI4B-StoryWeaver':"This train subset contains the transliteration pairs from publicly available Story Weaver dataset.",
                'NotAI-tech':"This train subset contains the transliteration pairs from publicly available NotAI-tech corpus.",
            }
            targetLanguage = map_2[lang]
            J['name'] = name[i]
            J['description'] = description[i]
            J['languages']['targetLanguage'] = targetLanguage

            with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/{split}/{map_2[lang]}/params.json','w') as JS:
                json.dump(J, JS, indent=4)

            #create zip
            script_dir = path.dirname(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_model_data_ulca/ulca/{split}/{map_2[lang]}/')
            file_name = f"{i}_{split}_en_{map_2[lang]}"
            create_zip(file_name, script_dir)
