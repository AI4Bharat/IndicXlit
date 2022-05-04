import sys

tgt_lang = sys.argv[1]

f = open('../output/possible_translit_pair_score_en_'+tgt_lang+'.txt','r')
lines = f.read().split('\n')

list_s = [line for line in lines if 'S-' in line]
list_h = [line for line in lines if 'H-' in line]
list_d = [line for line in lines if 'D-' in line]

list_s.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_h.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )
list_d.sort(key = lambda x: int(x.split('\t')[0].split('-')[1]) )


f_out = open('../output/possible_translit_pairs_with_score_en_'+tgt_lang+'.txt', 'w')
lines_out = []
for s,h in zip(list_s,list_h):
    
    s_id = int(s.split('\t')[0].split('-')[1])
    h_id = int(h.split('\t')[0].split('-')[1])

    if s_id == h_id:
        lines_out.append( ''.join(s.split('\t')[1].split(' ')[1:]) + '\t' + ''.join(h.split('\t')[2].split(' ')) + '\t' + str( float(h.split('\t')[1]) ) )

lines_out.sort(key = lambda x: float( x.split('\t')[2] ), reverse= True)

f_out.write('\n'.join(lines_out))
f_out.close()
f.close()

