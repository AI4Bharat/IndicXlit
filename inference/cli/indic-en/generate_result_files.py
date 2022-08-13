import sys
import json

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
_rescore = int(sys.argv[2])



def post_process(translation_str, target_lang, _rescore):
    lines = translation_str.split('\n')

    list_s = [line for line in lines if 'S-' in line]
    list_h = [line for line in lines if 'H-' in line]
    # list_d = [line for line in lines if 'D-' in line]

    list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
    list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
    # list_d.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )

    res_dict = {}
    for s in list_s:
        s_id = int(s.split('\t')[0].split('-')[1])
        
        res_dict[s_id] = { 'S' : s.split('\t')[1] }

        res_dict[s_id]['H'] = []
        # res_dict[s_id]['D'] = []
        
        for h in list_h:
            h_id = int(h.split('\t')[0].split('-')[1])

            if s_id == h_id:
                res_dict[s_id]['H'].append( ( h.split('\t')[2], pow(2, float(h.split('\t')[1]) ) ) )
        
        # for d in list_d:
        #     d_id = int(d.split('\t')[0].split('-')[1])
        
        #     if s_id == d_id:
        #         res_dict[s_id]['D'].append( ( d.split('\t')[2], float(d.split('\t')[1]) ) )

    for r in res_dict.keys():
        res_dict[r]['H'].sort(key = lambda x : float(x[1]) ,reverse =True)
        # res_dict[r]['D'].sort(key = lambda x : float(x[1]) ,reverse =True)

    # for rescoring 
    result_dict = {}
    for i in res_dict.keys():            
        result_dict[res_dict[i]['S']] = {}
        for j in range(len(res_dict[i]['H'])):
            result_dict[res_dict[i]['S']][res_dict[i]['H'][j][0]] = res_dict[i]['H'][j][1]


    
    output_dict = {}
    if _rescore:
        output_dir = rescore(res_dict, result_dict, target_lang, alpha = 0.9)            
        for src_word in output_dir.keys():
            transliterated_word_list = []
            for j in range(len(output_dir[src_word])):
                transliterated_word_list.append( output_dir[src_word][j] )
            transliterated_word_list = [''.join(word.split(' ')) for word in transliterated_word_list]
            output_dict[src_word] = transliterated_word_list

    else:
        for i in res_dict.keys():
            # transliterated_word_list.append( res_dict[i]['S'] + '  :  '  + res_dict[i]['H'][0][0] )
            transliterated_word_list = []
            for j in range(len(res_dict[i]['H'])):
                transliterated_word_list.append( res_dict[i]['H'][j][0] )

            transliterated_word_list = [''.join(word.split(' ')) for word in transliterated_word_list]
            output_dict[res_dict[i]['S']] = transliterated_word_list

    # remove extra spaces
    # transliterated_word_list = [''.join(pair.split(':')[0].split(' ')[1:]) + ' : ' + ''.join(pair.split(':')[1].split(' ')) for pair in transliterated_word_list]

    
    return output_dict





def rescore(res_dict, result_dict, target_lang, alpha ):
        
    alpha = alpha
    # word_prob_dict = {}
    word_prob_dict = json.load( open('word_prob_dicts/en_word_prob_dict.json', 'r') )

    candidate_word_prob_norm_dict = {}
    candidate_word_result_norm_dict = {}

    input_data = {}
    for i in res_dict.keys():
        input_data[res_dict[i]['S']] = []
        for j in range(len(res_dict[i]['H'])):
            input_data[res_dict[i]['S']].append( res_dict[i]['H'][j][0] )
    
    for src_word in input_data.keys():
        candidates = input_data[src_word]

        candidates = [' '.join(word.split(' ')) for word in candidates]
        
        total_score = 0

        if src_word.lower() in result_dict.keys():
            for candidate_word in candidates:
                if candidate_word in result_dict[src_word.lower()].keys():
                    total_score += result_dict[src_word.lower()][candidate_word]
        
        candidate_word_result_norm_dict[src_word.lower()] = {}
        
        for candidate_word in candidates:
            candidate_word_result_norm_dict[src_word.lower()][candidate_word] = (result_dict[src_word.lower()][candidate_word]/total_score)

        candidates = [''.join(word.split(' ')) for word in candidates ]
        
        total_prob = 0 
        
        for candidate_word in candidates:
            if candidate_word in word_prob_dict.keys():
                total_prob += word_prob_dict[candidate_word]        
        
        candidate_word_prob_norm_dict[src_word.lower()] = {}
        for candidate_word in candidates:
            if candidate_word in word_prob_dict.keys():
                candidate_word_prob_norm_dict[src_word.lower()][candidate_word] = (word_prob_dict[candidate_word]/total_prob)
        
    output_data = {}
    for src_word in input_data.keys():
        
        temp_candidates_tuple_list = []
        candidates = input_data[src_word]
        candidates = [ ''.join(word.split(' ')) for word in candidates]
        
        
        for candidate_word in candidates:
            if candidate_word in word_prob_dict.keys():
                temp_candidates_tuple_list.append((candidate_word, alpha*candidate_word_result_norm_dict[src_word.lower()][' '.join(list(candidate_word))] + (1-alpha)*candidate_word_prob_norm_dict[src_word.lower()][candidate_word] ))
            else:
                temp_candidates_tuple_list.append((candidate_word, 0 ))

        temp_candidates_tuple_list.sort(key = lambda x: x[1], reverse = True )
        
        temp_candidates_list = []
        for cadidate_tuple in temp_candidates_tuple_list: 
            temp_candidates_list.append(' '.join(list(cadidate_tuple[0])))

        output_data[src_word] = temp_candidates_list

    return output_data


f = open('output/'+lang_abr+'_en.txt','r')
translation_str = f.read()

dict_output = post_process(translation_str, lang_abr, _rescore)

f_output = open('output/final_transliteration.txt', 'w')
for d in dict_output:
    f_output.write(''.join(d.split(' ')[1:]) + '\t[' + ', '.join(dict_output[d]) + ']\n')
f_output.close()
f.close()