import sys

src_lang = sys.argv[1]

f = open('../output/interactive_script_output_'+src_lang+'_en.txt','r')
lines = f.read().split('\n')

list_s = [line for line in lines if 'S-' in line]
list_h = [line for line in lines if 'H-' in line]
list_d = [line for line in lines if 'D-' in line]

list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_d.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )

res_dict = {}
for s,h in zip(list_s,list_h):
    s_id = int(s.split('\t')[0].split('-')[1])
    
    res_dict[s_id] = { 'S' : ''.join(s.split('\t')[1].split(' ')[1:]) }
        
    h_id = int(h.split('\t')[0].split('-')[1])

    if s_id == h_id:
        res_dict[s_id]['H'] = ( ''.join(h.split('\t')[2].split(' ')), float(h.split('\t')[1]) ) 


f_out = open('../output/interactive_translit_pairs_'+src_lang+'_en.txt', 'w')
lines_out = []
for i in res_dict.keys():
    lines_out.append( res_dict[i]['S'] + '\t' + res_dict[i]['H'][0] + '\t' + str(res_dict[i]['H'][1]) )

f_out.write('\n'.join(lines_out))
f_out.close()