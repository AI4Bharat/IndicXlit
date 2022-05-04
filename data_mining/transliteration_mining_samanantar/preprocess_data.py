# The path to the local git repo for Indic NLP library
INDIC_NLP_LIB_HOME=r"/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/tools/IndicNLPlib/indic_nlp_library"

# The path to the local git repo for Indic NLP Resources
INDIC_NLP_RESOURCES=r"/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/tools/IndicNLPlib/indic_nlp_resources"


import sys
sys.path.append(r'{}'.format(INDIC_NLP_LIB_HOME))

from indicnlp import common
common.set_resources_path(INDIC_NLP_RESOURCES)

from indicnlp import loader 
loader.load()


from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize import indic_tokenize

f_en = open('/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/corpus_org/v2/en-mr/train.en', 'r')
lines_en = f_en.read().split('\n')
lines_en_out = []

f_nt = open('/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/corpus_org/v2/en-mr/train.mr', 'r')
lines_nt = f_nt.read().split('\n')
lines_nt_out = []

remove_nuktas=False
factory=IndicNormalizerFactory()
normalizer_nt=factory.get_normalizer("mr", remove_nuktas = False)

print(len(lines_nt))
print(len(lines_en))

lines_nt_norm = []
for line_nt in lines_nt:
    
    output_nt = normalizer_nt.normalize(line_nt)
    lines_nt_norm.append(output_nt)

print(len(lines_nt_norm))
print(len(lines_en))

lines_nt_out = [' '.join(indic_tokenize.trivial_tokenize(line_nt)) for line_nt in lines_nt_norm]
lines_en_out = [' '.join(indic_tokenize.trivial_tokenize(line_en)) for line_en in lines_en]

print(len(lines_nt_out))
print(len(lines_en_out))

f_en_out = open('/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/workplace/en-mr/corpus/train.en','w')
f_en_out.write('\n'.join(lines_en_out))

f_nt_out = open('/home/yashmadhani1997/Indic_xlit/translit_data_mine_samanantar/workplace/en-mr/corpus/train.mr','w')
f_nt_out.write('\n'.join(lines_nt_out))

f_nt_out.close()
f_en_out.close()
f_en.close()
f_nt.close()


