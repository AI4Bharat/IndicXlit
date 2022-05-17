import glob
import json
import time
from datetime import date

d = date.today().strftime("%d-%m-%Y")
Lang = ['te']
# Lang = ['hi', 'as', 'kn', 'kok', 'mai', 'ml', 'mr', 'or', 'pa', 'ta', 'te','sa', 'bn', 'gu', 'mni']
for lang in Lang:
    start = time.time()
    with open(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Annotation_Data/Benchmark_Data/{d}/{lang}_benchmark.txt', 'w', encoding='utf-8') as In:
        for file in glob.glob(f'/Users/priyankabedekar/Desktop/IndicXlit_Code/Annotation_Data/TAR_all/{lang}/*/*.json'):
            with open(file, "r", encoding= 'utf-8') as infile:
                data = json.load(infile)
                if "invalid" in data["variants"].keys(): continue
                for variants, status in data["variants"].items():
                    if status["status"] == "VALID":
                        In.write("%s\n" % (data["word"] + "\t" + variants))
    end = time.time()
    print(f'{lang} Runtime: {end - start}')