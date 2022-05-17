import cld3
import glob

lang = 'hi'
length = len(glob.glob(f'/Users/priyankabedekar/Desktop/IndicXlit/Data/Indic_corp/Text/{lang}.txt.*'))

for i in range(0, length):
    input = f'/Users/priyankabedekar/Desktop/IndicXlit/Data/Indic_corp/Text/{lang}.txt.{str(i)}'
    output = f'/Users/priyankabedekar/Desktop/IndicXlit/Data/Indic_corp/New_Text/{lang}.txt.{str(i)}'
    with open(input, encoding='utf-8') as inputfile:
        with open(output, 'w', encoding='utf-8') as outputfile:
            for i, line in enumerate(inputfile):
                p = cld3.get_language(line)
                if p.language == 'hi':
                    outputfile.write(line)



