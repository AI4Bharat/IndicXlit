import json

lang_code_list = [
    'as', 'brx', 'bn', 
    'gom', 'gu', 'hi', 
    'kn', 'mai', 'ml', 'mni', 'mr', 
    'ne', 'or', 'pa', 'sa', 'sd', 
    'ta', 'te', 'ks', 'ur'
    ]
for lang_code in lang_code_list:
    input_file_name = '../'+lang_code+'/fairseq_op_'+lang_code+'_en.txt'
    file_in = open(input_file_name, 'r')
    lines_in = file_in.read().split('\n')

    
    list_s = [line for line in lines_in if 'S-' in line]
    list_h = [line for line in lines_in if 'H-' in line]

    list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
    list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )

    res_dict = {}
    for s in list_s:
        s_id = int(s.split('\t')[0].split('-')[1])
        
        res_dict[s_id] = { 'S' : s.split('\t')[1] }

        res_dict[s_id]['H'] = []

        
    for h in list_h:
        h_id = int(h.split('\t')[0].split('-')[1])

        if h_id in res_dict:
            res_dict[h_id]['H'].append( ( h.split('\t')[2], pow(2, float(h.split('\t')[1]) ) ) )


    for r in res_dict.keys():
        res_dict[r]['H'].sort(key = lambda x : float(x[1]) ,reverse =True)


    output_dict = {}
    for r in res_dict.keys():
        output_dict[ ''.join( res_dict[r]['S'].split(' ')[1:] ) ] = ''.join( res_dict[r]['H'][0][0].split(' ') )
    
    
    output_file_name = '../'+lang_code+'/'+lang_code+'_output_dict.json'
    file_out = open(output_file_name, 'w')
  
    json.dump(output_dict, file_out, indent = 4)
    
    file_out.close()
    file_in.close()