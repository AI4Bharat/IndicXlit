import itertools
import csv
import unicodedata
import re

eng_vowels = []
eng_stop_list = []
indic_vowels = []
indic_stop_list = []
eng_indic_map = {}
lang_base = {}

def Load_mapping(file):
    global eng_indic_map, eng_stop_list, eng_vowels, indic_vowels, lang_base, indic_stop_list
    with open(file, 'r', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile)
        for i, row in enumerate(read):
            if i == 0:
                eng_vowels = row[1:]
            elif i == 1:
                eng_stop_list = row[1:]
            elif i>1 and i<24:
                lang_base[row[0]] = row[1]
            elif i == 24:
                indic_vowels = row[1:]
            elif i == 25:
                indic_stop_list = row[1:]
            else:
                eng_indic_map[row[0]] = row[1:]

def Preprocess(eng_word):
    eng_word = eng_word.lower()
    nfkd_form = unicodedata.normalize('NFKD', eng_word)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def Validate_XLit(lang, indic_word, eng_word):

    base = int(lang_base[lang])

    string_check = re.compile("[-@_!#$%^&*()<>?/\|}{~:;,.']") # special characters
    eng_word = Preprocess(eng_word) # Diacritics.

    if base == 3328 or base == 2944 or base == 3200 or base == 3072:
        if eng_word[-1] != 'u' and eng_word[-1] in eng_vowels and eng_word[-1] != 'a' and eng_word[-1] != 'e' and indic_word[-1] not in indic_vowels and indic_word[-1] != (chr)(base + 47) and indic_word[-1] != (chr)(base + 3):
            return False
        if eng_word[0] != 'y' and eng_word[0] not in eng_vowels and indic_word[0] in indic_vowels:
            return False
    elif base == 2432:
        if eng_word[-1] in eng_vowels and eng_word[-1] != 'a' and eng_word[-1] != 'e' and eng_word[-1] != 'o' and indic_word[-1] not in indic_vowels and indic_word[-1] != (chr)(base + 47) and indic_word[-1] != (chr)(base + 23) and indic_word[-1] != (chr)(base + 60):
            return False
    elif base == 2688:
        if eng_word[-1] in eng_vowels and eng_word[-1] != 'a' and eng_word[-1] != 'e' and eng_word[-1] != 'o' and indic_word[-1] not in indic_vowels and indic_word[-1] != (chr)(base + 47) and indic_word[-1] != (chr)(base + 60) and indic_word[-1] != (chr)(2690):
            return False
    else:
        if eng_word[-1] in eng_vowels and eng_word[-1] != 'a' and eng_word[-1] != 'e' and eng_word[-1] != 'o' and indic_word[-1] not in indic_vowels and indic_word[-1] != (chr)(base + 47) and indic_word[-1] != (chr)(base + 60):
            return False
    if eng_word[-1] not in eng_vowels and eng_word[-1] != 'w' and eng_word[-1] not in eng_stop_list and indic_word[-1] in indic_vowels:
        return False
    if eng_word[0] in eng_vowels and indic_word[0] not in indic_vowels and indic_word[0] != (chr)(base + 47):
        return False
    if base != 3328 and base != 2944 and eng_word[0] not in eng_vowels and indic_word[0] in indic_vowels:
        return False

    eng_word = ''.join([l for l in eng_word if l not in eng_vowels and l not in eng_stop_list and not l.isdigit() and string_check.search(l) == None])

    indic_word_new = {}
    indic_word_new[0] = ''

    for spelling in indic_word:

        if spelling == (chr)(base + 0) or spelling == (chr)(base + 1) or spelling == (chr)(base + 2) or spelling == (chr)(2672) or spelling == (chr)(3328) or spelling == (chr)(3076): # Nasalisation, te - 3072 + 4, ml - 3328 + 0, pa - 2560 + 112.
            temp = len(indic_word_new)
            for j in range(len(indic_word_new)):
                if base == 2432:
                    indic_word_new[temp] = indic_word_new[j] + (chr)(base + 40) + (chr)(base + 23)
                    indic_word_new[temp + 1] = indic_word_new[j] + (chr)(base + 40)
                    indic_word_new[temp + 2] = indic_word_new[j] + (chr)(base + 46)
                    temp += 3
                else:
                    indic_word_new[temp] = indic_word_new[j] + (chr)(base + 40)
                    indic_word_new[temp + 1] = indic_word_new[j] + (chr)(base + 46)
                    temp += 2
            continue

        elif spelling == (chr)(base + 67) or spelling == (chr)(base + 68): # "Ra" addition
            for k in range(len(indic_word_new)):
                indic_word_new[k] += (chr)(base + 48)

        elif (base == 3328 or base == 3200 or base == 3072) and (spelling == (chr)(base + 97) or spelling == (chr)(base + 98) or spelling == (chr)(base + 99)):
            for k in range(len(indic_word_new)):
                indic_word_new[k] += (chr)(base + 50)

        elif base == 3328 and spelling == (chr)(base + 25): # "Ng" addition for Malayalam
            temp = len(indic_word_new)
            for j in range(len(indic_word_new)):
                indic_word_new[temp] = indic_word_new[j] + (chr)(base + 40) + (chr)(base + 23)
                indic_word_new[temp + 1] = indic_word_new[j] + (chr)(base + 40)
                temp += 2

        elif base == 2944 and spelling == (chr)(base + 25): # "Ng" addition for Tamil
            temp = len(indic_word_new)
            for j in range(len(indic_word_new)):
                indic_word_new[temp] = indic_word_new[j] + (chr)(base + 40) + (chr)(base + 21)
                indic_word_new[temp + 1] = indic_word_new[j] + (chr)(base + 40)
                temp += 2

        elif spelling == (chr)(base + 30): # "Nj" addition for Tamil and Malayalam, "nya" for Marathi.
            temp = len(indic_word_new)
            for j in range(len(indic_word_new)):
                if base == 3328 or base == 2944:
                    indic_word_new[temp] = indic_word_new[j] + (chr)(base + 40) + (chr)(base + 28)
                    indic_word_new[temp + 1] = indic_word_new[j] + (chr)(base + 40)
                    temp += 2
                else:
                    indic_word_new[temp] = indic_word_new[j] + (chr)(base + 40)
                    indic_word_new[temp + 1] = indic_word_new[j]
                    temp += 2

        elif base == 2944 and spelling == (chr)(base + 49): # "Tra" addition
            temp = len(indic_word_new)
            for j in range(len(indic_word_new)):
                indic_word_new[temp] = indic_word_new[j] + (chr)(base + 31) + (chr)(base + 48)
                indic_word_new[temp + 1] = indic_word_new[j] + (chr)(base + 48)
                temp += 2

        elif  (spelling == (chr)(base + 95) and (base == 2304 or base == 2432)) or spelling == (chr)(base + 60) or spelling == (chr)(base + 61) or spelling == (chr)(base + 77) or (spelling == (chr)(base + 113) and base != 2432) or spelling in indic_stop_list or spelling in indic_vowels or spelling.isdigit() or string_check.search(spelling) != None: #Check for digits and special characters are not required.
            continue
        else:
            for k in range(len(indic_word_new)):
                indic_word_new[k] += spelling

    prev = ['']
    checks = []
    count = 0
    try:
        for i, spelling in enumerate(eng_word):
            if count%10 == 0:
                for i in range(len(indic_word_new)):
                    word = indic_word_new[i][:count]
                    checks.append(word)
                prev = list(set(prev).intersection(list(checks)))

            if spelling == " ":
                continue
            if i==0:
                prev = eng_indic_map[spelling]
            else:
                temp_list = []
                for x in prev:
                    for y in eng_indic_map[spelling]:
                        temp_list.append(x + y)
                prev = temp_list
            count += 1
    except:
        return False

    for i in range(len(indic_word_new)):
        indic_word_new[i] = ''.join(c[0] for c in itertools.groupby(indic_word_new[i]))

    for i in range(len(prev)):
        prev[i] = ''.join(c[0] for c in itertools.groupby(prev[i]))

    for i in range(len(indic_word_new)):
        if indic_word_new[i] in prev: return True
    return False





# Sample word
# Lang = "mai"
# file = "/Users/priyankabedekar/Desktop/IndicXlit/Data/Mappings/mapping_mai.csv"
# Load_mapping(file)
# indic_word = "समस्तवेदार्थसाससंग्रहात्मिकेतिसमस्तवेदार्थसासस"
# eng_word = "samastvedarthsasasangrahtmiketisamastvedarthsasas"
# print(Validate_XLit(Lang, indic_word, eng_word))


# Dataset
lang_list = ['bn', 'gu', 'hi', 'mr', 'kn', 'pa', 'ta', 'te', 'ml', "as", "or"]
for Lang in lang_list:
    count = 0
    true_count = 0
    Load_mapping(f"/Users/priyankabedekar/Desktop/IndicXlit/Data/mapping_{Lang}.csv")
    input_path = f'/Users/priyankabedekar/Desktop/IndicXlit/Data/Dakshina/Dakshina_{Lang}_train.csv'
    with open(input_path, 'r', encoding='utf-8') as sample_file:
        with open(f'{Lang}_Invalid_words.csv', 'w', encoding = 'utf-8') as outputfile:
            header = ['Indic', 'English']
            outfile = csv.DictWriter(outputfile, fieldnames = header)
            outfile.writeheader()
            sample_list = csv.reader(sample_file, delimiter=',')
            next(sample_list)
            for word in sample_list:
                if Validate_XLit(Lang, word[0].lower(), word[1].lower()) == True:
                    true_count += 1
                else:
                    outfile.writerow({'Indic' : word[0], 'English' : word[1]})
                count += 1

    print(Lang, "-" ,true_count/count * 100)
