import sys
import json

lang = sys.argv[1]
lang_abr = sys.argv[2]

f = open('../en-'+lang_abr+'/output/generate-test.txt','r')
lines = f.read().split('\n')

list_s = [line for line in lines if 'S-' in line]
list_t = [line for line in lines if 'T-' in line]
list_h = [line for line in lines if 'H-' in line]
list_d = [line for line in lines if 'D-' in line]

list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_t.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_d.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )

res_dict = {}
for s in list_s:
    s_id = int(s.split('\t')[0].split('-')[1])
    
    res_dict[s_id] = { 'S' : s.split('\t')[1] }
    
    for t in list_t:
        t_id = int(t.split('\t')[0].split('-')[1])
        if s_id == t_id:
            res_dict[s_id]['T'] = t.split('\t')[1] 

    res_dict[s_id]['H'] = []
    res_dict[s_id]['D'] = []
    
    for h in list_h:
        h_id = int(h.split('\t')[0].split('-')[1])

        if s_id == h_id:
            res_dict[s_id]['H'].append( ( h.split('\t')[2], pow(2,float(h.split('\t')[1])) ) )
    
    for d in list_d:
        d_id = int(d.split('\t')[0].split('-')[1])
    
        if s_id == d_id:
            res_dict[s_id]['D'].append( ( d.split('\t')[2], pow(2,float(d.split('\t')[1]))  ) )

for r in res_dict.keys():
    res_dict[r]['H'].sort(key = lambda x : float(x[1]) ,reverse =True)
    res_dict[r]['D'].sort(key = lambda x : float(x[1]) ,reverse =True)





f_out = open('../en-'+lang_abr+'/output/result_dict_'+lang_abr+'.json','w')


from xml.dom import minidom

root = minidom.Document()


root_element = root.createElement('TransliterationTaskResults') 
root.appendChild(root_element)
root_element.setAttribute('SourceLang', lang) 
root_element.setAttribute('TargetLang', 'English')

result_dict = {}

for i in res_dict.keys():
    word = root.createElement('Name')
    word.setAttribute('ID', str(i+1))
    root_element.appendChild(word)

    source_word = root.createElement('SourceName')
    source_text = root.createTextNode(res_dict[i]['S'])
    source_word.appendChild(source_text)
    word.appendChild(source_word)
    
    result_dict[res_dict[i]['S']] = {}

    for j in range(len(res_dict[i]['H'])):
        target_word = root.createElement('TargetName')
        target_word.setAttribute('ID', str(j+1))
        target_text = root.createTextNode(res_dict[i]['H'][j][0] )
        target_word.appendChild(target_text)
        word.appendChild(target_word)
        result_dict[res_dict[i]['S']][res_dict[i]['H'][j][0]] = res_dict[i]['H'][j][1]

xml_str = root.toprettyxml(indent ="\t", encoding="UTF-8") 
  
save_path_file = "../en-"+lang_abr+"/output/translit_result.xml"
  
with open(save_path_file, "wb") as f:
    f.write(xml_str) 

json.dump(result_dict, f_out, indent = 4)
f_out.close()







root = minidom.Document()


root_element = root.createElement('TransliterationCorpus') 
root.appendChild(root_element)
root_element.setAttribute('SourceLang', lang)
root_element.setAttribute('TargetLang', 'English')
root_element.setAttribute('CorpusID' , 'Test')

for i in res_dict.keys():
    word = root.createElement('Name')
    word.setAttribute('ID', str(i+1))
    root_element.appendChild(word)

    source_word = root.createElement('SourceName')
    source_text = root.createTextNode(res_dict[i]['S'])
    source_word.appendChild(source_text)
    word.appendChild(source_word)

    for j in range(1):
        target_word = root.createElement('TargetName')
        target_word.setAttribute('ID', str(j+1))
        target_text = root.createTextNode(res_dict[i]['T'])
        target_word.appendChild(target_text)
        word.appendChild(target_word)
    
xml_str = root.toprettyxml(indent ="\t", encoding="UTF-8") 
  
save_path_file = "../en-"+lang_abr+"/output/translit_test.xml"
  
with open(save_path_file, "wb") as f:
    f.write(xml_str)
