from bs4 import BeautifulSoup
import re
import glob

# lang = ['Gujarati', 'Hindi', 'Kannada', 'Assamese', 'Bodo', 'Punjabi', 'Odia', 
# 'Konkani',  'Malayalam', 'Bengali', 'Dogri', 'Marathi', 'Kashmiri', 'Maithili', 'Manipuri', 
# 'Tamil', 'Urdu', 'Telugu', 'Nepali']
lang = ['Malayalam']
for Lang in lang:
    with open(f'/Users/priyankabedekar/Desktop/IndicXlit/Data/LDC-IL/test.txt', 'w') as w:
        for f in glob.glob(f'/Users/priyankabedekar/Desktop/IndicXlit/Data/LDC-IL/LDCIL_dataset_RawTextCorpora_MalayalamTextCorpus_Data_ML00001.xml'):
    # with open(f'/home/cs20m050/LDC-IL/{Lang}_ldcil.txt', 'w') as w:
    #     for f in glob.glob(f'/home/cs20m050/LDC-IL/RawTextCorpora/{Lang}TextCorpus/Data/*.xml'):
            with open(f, "r", encoding= 'utf-8') as file:
                files = file.read()
                soup = BeautifulSoup(files, features="html.parser")
                paragraphs = str(soup.findAll('body')) #turn the soup object into a string
                sentences = paragraphs.split('.') #creates a list of sentences
                for e in sentences:
                    e = re.sub(r'(<.*?>)', '', e) #gets rid of the tags
                    w.write(e + '\n')
