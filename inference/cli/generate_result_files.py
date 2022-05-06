import sys

lang_dict = {
    'as' : 'Assamese',
    'bn' : 'Bangla',
    'brx' : 'Bodo',
    'gom' : 'Konkani', 
    'gu' : 'Gujarati',
    'hi' : 'Hindi',
    'kn' : 'Kannada',
    'ks' : 'Kashmiri',
    'mai' : 'Maithili',
    'ml' : 'Malayalam',
    'mni' : 'Manipuri',
    'mr' : 'Marathi',
    'ne' : 'Nepali',
    'or' : 'Oriya',
    'pa' : 'Punjabi',
    'sa' : 'Sanskrit',
    'sd' : 'Sindhi',
    'si' : 'Sinhala',
    'ta' : 'Tamil',
    'te' : 'Telugu',
    'ur' : 'Urdu' 
}



lang_abr = sys.argv[1]
lang = lang_dict[lang_abr]

f = open('output/en_'+lang_abr+'.txt','r')

f_output = open('output/final_transliteration.txt', 'w')

lines = f.read().split('\n')

list_s = [line for line in lines if 'S-' in line]
list_h = [line for line in lines if 'H-' in line]
list_d = [line for line in lines if 'D-' in line]

list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_d.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )

res_dict = {}
for s in list_s:
    s_id = int(s.split('\t')[0].split('-')[1])
    
    res_dict[s_id] = { 'S' : s.split('\t')[1] }

    res_dict[s_id]['H'] = []
    res_dict[s_id]['D'] = []
    
    for h in list_h:
        h_id = int(h.split('\t')[0].split('-')[1])

        if s_id == h_id:
            res_dict[s_id]['H'].append( ( h.split('\t')[2], float(h.split('\t')[1]) ) )
    
    for d in list_d:
        d_id = int(d.split('\t')[0].split('-')[1])
    
        if s_id == d_id:
            res_dict[s_id]['D'].append( ( d.split('\t')[2], float(d.split('\t')[1]) ) )

for r in res_dict.keys():
    res_dict[r]['H'].sort(key = lambda x : float(x[1]) ,reverse =True)
    res_dict[r]['D'].sort(key = lambda x : float(x[1]) ,reverse =True)



from xml.dom import minidom

root = minidom.Document()


root_element = root.createElement('TransliterationTaskResults') 
root.appendChild(root_element)
root_element.setAttribute('SourceLang', lang) 
root_element.setAttribute('TargetLang', 'English')

lines_output = []

for i in res_dict.keys():
    word = root.createElement('Name')
    word.setAttribute('ID', str(i+1))
    root_element.appendChild(word)

    source_word = root.createElement('SourceName')
    source_text = root.createTextNode(res_dict[i]['S'])
    source_word.appendChild(source_text)
    word.appendChild(source_word)

    for j in range(len(res_dict[i]['H'])):
        target_word = root.createElement('TargetName')
        target_word.setAttribute('ID', str(j+1))
        target_text = root.createTextNode(res_dict[i]['H'][j][0] )
        target_word.appendChild(target_text)
        word.appendChild(target_word)
    
    lines_output.append( ''.join(res_dict[i]['S'].split(' ')[:6]) + ':\t' + ''.join(res_dict[i]['H'][0][0].split(' ')) )

f_output.write('\n'.join(lines_output))
f_output.close()

xml_str = root.toprettyxml(indent ="\t", encoding="UTF-8") 
  
save_path_file = "output/translit_result_"+lang_abr+".xml"
  
with open(save_path_file, "wb") as f:
    f.write(xml_str) 
