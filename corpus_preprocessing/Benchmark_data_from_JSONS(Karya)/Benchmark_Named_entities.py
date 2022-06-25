import glob
import json
import time
from datetime import date

d = date.today().strftime("%d-%m-%Y")
Lang = ['hi', 'as', 'kn', 'mai', 'ml', 'mr', 'pa', 'ta', 'te','sa', 'bn', 'gu', 'kok', 'or', 'mni']
# Lang = ['kn']
for lang in Lang:
    start = time.time()
    words = []
    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Data/Named_entities/Reports/{lang}_clean.txt', 'w', encoding='utf-8') as In:
        for file in glob.glob(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Data/Named_entities/Outputs/{lang}/*/*.json'):
            with open(file, "r", encoding= 'utf-8') as infile:
                data = json.load(infile)
                if "invalid" in data["variants"].keys(): continue
                for variants, status in data["variants"].items():
                    if status["status"] == "VALID":
                        if data["word"].strip() == "nabha" or data["word"].strip() == "novi":
                            print(data["access_code"]) 
                        v = []
                        for i in variants.strip():
                            if i != '\u200d' and i != '\u200c':
                                v.append(i)
                        variant = ''.join(v)
                        In.write("%s\n" % (variant + "\t" + data["word"].strip()))
                        if data["word"] not in words:
                           words.append(data["word"])
    print(lang +'-'+ str(len(words)))
    end = time.time()
    print(f'{lang} Runtime: {end - start}')