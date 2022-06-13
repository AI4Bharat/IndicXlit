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
    'Bengali' : ['I','S','W','E','M','D'],
    'Bodo' : ['I','M'],
    'Konkani' : ['I','E','M'],
    'Gujarati' : ['I','S','W','E','M','D'],
    'Hindi' : ['I','S','W','E','M','D'],
    'Kannada' : ['I','S','W','E','M','D'],
    'Kashmiri' : ['I','W','M'],
    'Maithili' : ['I','W','E','M'],
    'Malayalam' : ['I','S','W','E','M','D'],
    'Manipuri' : ['I','M'],
    'Marathi' : ['I','S','W','E','M','D'],
    'Nepali' : ['I','W','M'],
    'Oriya' : ['I','S','W','M'],
    'Punjabi' : ['I','S','W','E','M','D'],
    'Sanskrit' : ['I','W','M'],
    'Sindhi' : ['I','W','E','D'],
    # 'Sinhala' : ['E','D'],
    'Tamil' : ['I','S','W','E','M','D'],
    'Telugu' : ['I','S','W','E','M','D'],
    'Urdu' : ['I','W','E','M','D']
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

# Lang = ['hi','kok','bn','gu','as','kn','mai','ml','mr','ne','or','pa','sa','sd','ta','te','brx','mni','ur','ks']
Lang = ['ur']
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
            print("Total_words:" + str(len(Dakshina)))
    if 'E' in data_resources[mapping[lang]]: 
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/existing_data/Indic_Xlit_translit_parallel_corpus/{mapping[lang]}/{lang}_train.txt') as E:
            Existing = list([(row[0],row[1].lower()) for row in csv.reader(E, delimiter ='\t')])
            if lang in ['ur']:
                # Existing = [(normalize(tup[0]), tup[1]) for tup in Existing]
                pass
            else:
                Existing = [(normalizer.normalize(tup[0]), tup[1]) for tup in Existing]

            print("Total_words:" + str(len(Existing)))
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
                    if 'E' in data_resources[mapping[lang]]:
                        E = [k for k in set(Existing).intersection(pair)]
                        print(len(E))
                        all_data.extend([a+("Existing",None) for a in E])
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
                    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_left.csv', index=False)
    
    ind = [f'{map_3[lang]}'+str(index) for index in range(1,len(all_data))]
    # print(ind[0], ind[-1])
    all_data = [(ind[i-1],) + all_data[i] for i in range(1,len(all_data))]
    # print(all_data)
    df = pd.DataFrame(all_data, columns=["unique_identifier", "native word", "english word", "source", "score"])
    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_final_data.csv', index=False)
    # Create a multiline json
    json_list = json.loads(df.to_json(orient = "records"))

    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/{map_3[lang]}/{map_3[lang]}_train.json', 'w', encoding='utf-8') as f:
        for item in json_list:
            f.write("%s\n" % json.dumps(item, ensure_ascii=False))
    end = time.time()
    print(f"{mapping[lang]}:" + str(end-start))

# Test
for lang in Lang:
    all_data = list()
    start = time.time()
    print(f"{mapping[lang]}")
    if lang not in ['ur','ks','mni']:
        normalizer_factory = IndicNormalizerFactory()
        normalizer = normalizer_factory.get_normalizer(norm[lang])
    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/corpus/en-{lang}/corpus/test.{lang}') as F1:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/corpus/en-{lang}/corpus/test.en') as F2:
            r1 = csv.reader(F1)
            r2 = csv.reader(F2)             
            ind_word_list = ["".join(word).replace(" ","") for word in r1]
            en_word_list = ["".join(word).replace(" ","") for word in r2]
            pair = list(zip(ind_word_list,en_word_list))

            df = pd.DataFrame(pair)
            df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_all_data_test.csv', index=False)

            print("Pairs Left: " + str(len(pair)))

            if lang not in ['sd']:

                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/test_set/{lang}_test.txt') as B:
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

                    # Benchmark_Pairs
                    B = [k for k in set(BenchMark).intersection(pair)]
                    print(len(B))
                    B_U = [k for k in B if k[0] in Uniform]
                    print(len(B_U))
                    all_data.extend([a+('AK-Uni',) for a in B_U])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(B_U)))
                    print("Pairs Left: " + str(len(pair)))
                    B = (set(B).difference(set(B_U)))
                    print(len(B))
                    all_data.extend([a+('AK-Freq',) for a in B])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(B)))
                    print("Pairs Left: " + str(len(pair)))

                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/Named_entities/normalized_names_files/{lang}_benchmark_names.txt') as N:
                    NE = list([(row[0],row[1].lower()) for row in csv.reader(N, delimiter ='\t')])
                    if lang not in ['ur']:
                        NE = [(normalizer.normalize(tup[0]), tup[1]) for tup in NE]
                    else:
                        # NE = [(normalize(tup[0]), tup[1]) for tup in NE]
                        pass
                    print("Total_words:" + str(len(NE)))
                    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/Named_entities/Foreign/Foreign_Lastname.txt') as NFN, open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/Named_entities/Foreign/Foreign_locations.txt') as NFL:
                        FN = [word[0] for word in csv.reader(NFN)]
                        # FN = [normalizer.normalize(tup[0]) for tup in Uniform]
                        print("Total_words:" + str(len(FN)))
                        FN.extend([word[0] for word in csv.reader(NFL)])
                    # Benchmark_Pairs
                    N = [k for k in set(NE).intersection(pair)]
                    print(len(N))
                    N_F = [k for k in N if k[1] in FN]
                    print(len(N_F))
                    all_data.extend([a+('AK-NEF',) for a in N_F])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(N_F)))
                    print("Pairs Left: " + str(len(pair)))
                    N = (set(N).difference(set(N_F)))
                    print(len(N))
                    all_data.extend([a+('AK-NEI',) for a in N])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(N)))
                    print("Pairs Left: " + str(len(pair)))
                
            if lang not in ['ks','kok','as','or','mni','brx','ne','mai','sa']:
                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Dakshina/{lang}/lexicons/{lang}.translit.sampled.test.tsv') as D:
                    Dakshina = list([(row[0],row[1].lower()) for row in csv.reader(D, delimiter ='\t')])
                    if lang not in ['ur']:
                        Dakshina = [(normalizer.normalize(tup[0]), tup[1]) for tup in Dakshina]
                    else:
                        # Dakshina = [(normalize(tup[0]), tup[1]) for tup in Dakshina]
                        pass
                    print("Total_words:" + str(len(Dakshina)))

                    # Dakshina_Pairs
                    D = [k for k in set(Dakshina).intersection(pair)]
                    print(len(D))
                    all_data.extend([a+("Dakshina",) for a in D])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(D)))
                    print("Pairs Left: " + str(len(pair)))

                    ##
                    all_data.extend([a+("Dakshina",) for a in pair])
                    ##

            df = pd.DataFrame(pair)
            df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_left_test.csv', index=False)
    
    ind = [f'{map_3[lang]}'+str(index) for index in range(1,len(all_data))]
    # print(ind[0], ind[-1])
    all_data = [(ind[i-1],) + all_data[i] for i in range(1,len(all_data))]
    # print(all_data)
    df = pd.DataFrame(all_data, columns=["unique_identifier", "native word", "english word", "source"])
    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_final_data_test.csv', index=False)
    # Create a multiline json
    json_list = json.loads(df.to_json(orient = "records"))

    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/{map_3[lang]}/{map_3[lang]}_test.json', 'w') as f:
        for item in json_list:
            f.write("%s\n" % json.dumps(item,ensure_ascii=False))
    end = time.time()
    print(f"{mapping[lang]}:" + str(end-start))

# Val
for lang in Lang:
    all_data = list()
    start = time.time()
    print(f"{mapping[lang]}")
    if lang not in ['ur','ks','mni']:
        normalizer_factory = IndicNormalizerFactory()
        normalizer = normalizer_factory.get_normalizer(norm[lang])
    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/corpus/en-{lang}/corpus/valid.{lang}') as F1:
        with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/corpus/en-{lang}/corpus/valid.en') as F2:
            r1 = csv.reader(F1)
            r2 = csv.reader(F2)             
            ind_word_list = ["".join(word).replace(" ","") for word in r1]
            en_word_list = ["".join(word).replace(" ","") for word in r2]
            pair = list(zip(ind_word_list,en_word_list))

            df = pd.DataFrame(pair)
            df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_all_data_valid.csv', index=False)

            print("Pairs Left: " + str(len(pair)))

            if lang not in ['sd']:

                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Benchmark/valid_set/{lang}_valid.txt') as B:
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

                    # Benchmark_Pairs
                    B = [k for k in set(BenchMark).intersection(pair)]
                    print(len(B))
                    B_U = [k for k in B if k[0] in Uniform]
                    print(len(B_U))
                    all_data.extend([a+('AK-Uni',None) for a in B_U])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(B_U)))
                    print("Pairs Left: " + str(len(pair)))
                    B = (set(B).difference(set(B_U)))
                    print(len(B))
                    all_data.extend([a+('AK-Freq',None) for a in B])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(B)))
                    print("Pairs Left: " + str(len(pair)))
            
            #mined data


            with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/mined_data/valid_set_random_sample/valid_random_sample_2k_{lang}.txt') as N:
                V = list([(row[0],row[1].lower()) for row in csv.reader(N, delimiter ='\t')])
                if lang in ['ur']:
                    # V = [(normalize(tup[0]), tup[1]) for tup in V]
                    pass
                else:
                    V = [(normalizer.normalize(tup[0]), tup[1]) for tup in V]
                print("Total_words:" + str(len(V)))
                if lang not in ['kok', 'brx']:
                    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/wikidata/true_pairs/{lang}.txt') as W:
                        Wiki = list([(row[1],row[0].lower()) for row in csv.reader(W, delimiter ='|')])
                        if lang in ['ur']:
                            # Wiki = [(normalize(tup[0]), tup[1]) for tup in Wiki]
                            pass
                        else:
                            Wiki = [(normalizer.normalize(tup[0]), tup[1]) for tup in Wiki]
                        
                        print("Total_words:" + str(len(Wiki)))

                        W = [k for k in set(Wiki).intersection(pair)]
                        print(len(W))
                        all_data.extend([a+("Wikidata",None) for a in W])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(W)))
                        print("Pairs Left: " + str(len(pair)))
                if lang not in ['ks', 'mni', 'kok', 'brx','ne','mai','sa', 'ur', 'sd']:
                    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/samanantar/valid_pairs/{lang}-en_valid.csv') as S:
                        Samanantar = list([(row[0],row[1].lower()) for row in csv.reader(S, delimiter =',')])
                        if lang in ['ur']:
                            # Samamantar = [(normalize(tup[0]), tup[1]) for tup in Samanantar]
                            pass
                        else:
                            Samamantar = [(normalizer.normalize(tup[0]), tup[1]) for tup in Samanantar]
                        
                        print("Total_words:" + str(len(Samanantar)))
                        S = [k for k in set(Samanantar).intersection(pair)]
                        print(len(S))
                        all_data.extend([a+("Samanantar",None) for a in S])
                        print("Data so far: " + str(len(all_data)))
                        pair = (set(pair).difference(set(S)))
                        print("Pairs Left: " + str(len(pair)))
            
                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/indiccorp/threshold_0_35_files/translit_pairs_with_avg_score_thr_035_{lang}.txt') as I:
                    IndicCorp = list([(row[0],row[1].lower(),row[2]) for row in csv.reader(I, delimiter ='\t')])
                    if lang in ['ur']:
                        # IndicCorp = [(normalize(tup[0]), tup[1], tup[2]) for tup in IndicCorp]
                        pass
                    else:
                        IndicCorp = [(normalizer.normalize(tup[0]), tup[1], tup[2]) for tup in IndicCorp]
                    
                    Slice = {row[:2]:row[2] for row in IndicCorp}
                    # print(Slice)
                    I = [k for k in set(Slice.keys()).intersection(pair)]
                    print(len(I))
                    all_data.extend([a+("IndicCorp",eval(Slice[a])) for a in I])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(I)))
                    print("Pairs Left: " + str(len(pair)))
                    
            if lang not in ['ks','kok','as','or','mni','brx','ne','mai','sa']:
                with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/Dakshina/{lang}/lexicons/{lang}.translit.sampled.dev.tsv') as D:
                    Dakshina = list([(row[0],row[1].lower()) for row in csv.reader(D, delimiter ='\t')])
                    if lang in ['ur']:
                        # Dakshina = [(normalize(tup[0]), tup[1]) for tup in Dakshina]
                        pass
                    else:
                        Dakshina = [(normalizer.normalize(tup[0]), tup[1]) for tup in Dakshina]
                    print("Total_words:" + str(len(Dakshina)))

                    # Dakshina_Pairs
                    D = [k for k in set(Dakshina).intersection(pair)]
                    print(len(D))
                    all_data.extend([a+("Dakshina",None) for a in D])
                    print("Data so far: " + str(len(all_data)))
                    pair = (set(pair).difference(set(D)))
                    print("Pairs Left: " + str(len(pair)))

                    ##
                    all_data.extend([a+("Dakshina",None) for a in pair])
                    ##


            df = pd.DataFrame(pair)
            df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_left_val.csv', index=False)
    
    ind = [f'{map_3[lang]}'+str(index) for index in range(1,len(all_data))]
    # print(ind[0], ind[-1])
    all_data = [(ind[i-1],) + all_data[i] for i in range(1,len(all_data))]
    # print(all_data)
    df = pd.DataFrame(all_data, columns=["unique_identifier", "native word", "english word", "source","score"])
    df.to_csv(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/CSV/{lang}_final_data_val.csv', index=False)
    # Create a multiline json
    json_list = json.loads(df.to_json(orient = "records"))

    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/All_Data/JSONL/{map_3[lang]}/{map_3[lang]}_valid.json', 'w') as f:
        for item in json_list:
            f.write("%s\n" % json.dumps(item,ensure_ascii=False))
    end = time.time()
    print(f"{mapping[lang]}:" + str(end-start))

    