#!/usr/bin/python

# added by yash
import argparse
import logging
import sys
import json

# # added by yash
# def rescoring_unique_indicorp(input_data):
#     file_unique_words = open('hi_unique_filtered.txt','r')
#     list_unique_words = file_unique_words.read().split('\n')


#     for src_word in input_data.keys():
#         temp_candidates_list = []
#         candidates = input_data[src_word]
#         for candidate_word in candidates:
#             if candidate_word in list_unique_words:
#                 temp_candidates_list.append(candidate_word)
#         if len(temp_candidates_list)>0:
#             input_data[src_word] = temp_candidates_list

#     return input_data

# added by yash
# def rescoring_lm(input_data):

#     word_freq_dict = json.load(open('../../word_freq_dicts/hi_word_freq_dict.json','r'))

#     for src_word in input_data.keys():
#         temp_candidates_tuple_list = []
#         candidates = input_data[src_word]

#         candidates = [ ''.join(word.split(' ')) for word in candidates]
        
#         for candidate_word in candidates:
#             if candidate_word in word_freq_dict.keys():
#                 temp_candidates_tuple_list.append((candidate_word, word_freq_dict[candidate_word] ))
#             else:
#                 temp_candidates_tuple_list.append((candidate_word, 0 ))

#         temp_candidates_tuple_list.sort(key = lambda x: x[1], reverse = True )
        
#         temp_candidates_list = []
#         for cadidate_tuple in temp_candidates_tuple_list: 
#             temp_candidates_list.append(' '.join(list(cadidate_tuple[0])))

#         input_data[src_word] = temp_candidates_list

#     return input_data



# added by yash
def rescoring_wt_avg_score_freq( input_data, word_prob_dict_file, result_dict_file, alpha ):
    
    alpha = alpha
    
    word_prob_dict = json.load(open(word_prob_dict_file, 'r'))

    result_dict = json.load(open(result_dict_file, 'r'))
    
    candidate_word_prob_norm_dict = {}
    candidate_word_result_norm_dict = {}

    
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

        input_data[src_word] = temp_candidates_list

    return input_data


# added by yash
def levenshtein(u, v):
    prev = None
    curr = [0] + list(range(1, len(v) + 1))
    # Operations: (SUB, DEL, INS)
    prev_ops = None
    curr_ops = [(0, 0, i) for i in range(len(v) + 1)]
    for x in range(1, len(u) + 1):
        prev, curr = curr, [x] + ([None] * len(v))
        prev_ops, curr_ops = curr_ops, [(0, x, 0)] + ([None] * len(v))
        for y in range(1, len(v) + 1):
            delcost = prev[y] + 1
            addcost = curr[y - 1] + 1
            subcost = prev[y - 1] + int(u[x - 1] != v[y - 1])
            curr[y] = min(subcost, delcost, addcost)
            if curr[y] == subcost:
                (n_s, n_d, n_i) = prev_ops[y - 1]
                curr_ops[y] = (n_s + int(u[x - 1] != v[y - 1]), n_d, n_i)
            elif curr[y] == delcost:
                (n_s, n_d, n_i) = prev_ops[y]
                curr_ops[y] = (n_s, n_d + 1, n_i)
            else:
                (n_s, n_d, n_i) = curr_ops[y - 1]
                curr_ops[y] = (n_s, n_d, n_i + 1)
    return curr[len(v)], curr_ops[len(v)]

# added by yash
def charerr(ref,hyp):
    _, (s, i, d) = levenshtein(ref, hyp)
    cer_s = s
    cer_i = i
    cer_d = d
    cer_n = len(ref)

    if cer_n > 0:
        return (cer_s + cer_i + cer_d) / cer_n
    else:
        return 0


import codecs
import sys
import getopt
from os.path import basename
import xml.dom.minidom
from xml.dom.minidom import Node

# what we expect to find inside <TransliterationResults> tag...
RESULT_HEADER_ATTR = ('SourceLang', 'TargetLang', 'GroupID', 'RunID', 'RunType', 'Comments')
# ... and inside <TransliterationCorpus> tag
CORPUS_HEADER_ATTR = ('SourceLang', 'TargetLang', 'CorpusID', 'CorpusType', 'CorpusSize', 'CorpusFormat')

MAX_CANDIDATES = 10

def usage():
    '''
    User's manual
    '''
    print('''
Transliteration results evaluation script for NEWS:
Named Entities Workshop - Shared Task on Transliteration    
      
Usage:
    [python] %s [-h|--help] [-i|--input-file=<filename>]
                [-o|--output-file=<filename>]
                -t|--test-file=<filename>
                --max-candidates=<int>
                [--map-n=<int>]
    
Options:
    -h, --help         : Print this help and quit
    
    --check-only       : Only checks that the file is in correct format.
                         When this option is given, only one file is
                         accepted, either stdin or given with -i option.
    
    -i, --input-file   : Input file with transliteration results in NEWS
                         XML format. If not given, standard input is used.
                         
    -t, --test-file    : Test file with transliteration references in NEWS
                         XML format.
    
    -o, --output-file  : Output file with contribution of each source word
                         to each metric. If not given, no details are written.
                         The output file contains comma-separated values
                         and can be opened by a spreadsheet application
                         such as Microsoft Excel or OpenOffice Calc.
                         The values in the file are not divided by the 
                         number of source names.
                         
    --max-candidates   : Maximum number of transliteration candidates
                         to consider. By default, maximum 10 candidates are 
                         considered for evaluation according to the
                         NEWS 2009 whitepaper.

    --acc-matrix-output-file : Output file with accuracy matrices 
    
    --rescoring : rescore the predicted candidates by taking 
                  weighted average of normalized transliteration score 
                  and normalized candidate's probability in IndicCorp monolingual corpora. 

    --rescoring-method : method to rescore 

    --word-prob-dict-file : path to the dictionary file (.json) where probablity of each word is stored.
                            here probability of word is probability of word occuring in IndicCorp.
        
    --result-dict-file : path to the dictionary file (.json) where source word their transliteration 
                          candidates and corresponding transliteration scores are saved.
    
    --alpha : percent of transliteration score in weighted average.

    --correct-predicted-words-file : file path to store correctly predicted words 
                                        and their transliteration and corresponding given references. 
    
    --wrong-predicted-words-file : file path to store wrongly predicted words 
                                        and their transliteration and corresponding given references. 


The input files must be in UTF-8.
Example:
    %s -i translit_results.xml -t test.xml -o evaluation_details.csv
The detailed description of the metrics is in the NEWS 2010 whitepaper.
For comments, suggestions and bug reports email to Vladimir Pervouchine
vpervouchine@i2r.a-star.edu.sg.
    ''' % (basename(sys.argv[0]), basename(sys.argv[0])))
    
    
def get_options():
    '''
    Extracts command line arguments
    '''
    input_fname = None
    output_fname = None
    test_fname = None
    max_candidates = MAX_CANDIDATES
    check_only = False
    silent = False
    
    # added by yash
    acc_matrix_output_file = None
    rescoring = False 
    rescoring_method = None 
    word_prob_dict_file = None 
    result_dict_file = None 
    alpha = None 
    correct_predicted_words_file = None 
    wrong_predicted_words_file = None 

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'hi:o:t:', 
        ['help', 'input-file=', 'output-file=', 'test-file=',
         'check-only', 'silent', 
         'acc-matrix-output-file=', 'rescoring', 'rescoring-method=', 
         'word-prob-dict-file=', 'result-dict-file=', 'alpha=', 
         'correct-predicted-words-file=', 'wrong-predicted-words-file='])
        
    except getopt.GetoptError as err:
        sys.stderr.write('Error: %s\n' % err)
        usage()
        sys.exit(1)
        
    for o, a in opts:
        if o in ('-i', '--input-file'):
            input_fname = a
        elif o in ('-o', '--output-file'):
            output_fname = a
        elif o in ('-t', '--test-file'):
            test_fname = a   
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('--check-only',):
            check_only = True
        elif o in ('--silent',):
            silent = True
        elif o in ('--max-candidates', ):
            try:
                max_candidates = int(a)
            except ValueError as e:
                sys.stderr.write('Error: --max-candidates takes integer argument (you provided %s).\n' % a)
                sys.exit(1)
            if max_candidates < 1:
                sys.stderr.write('Error: --max-candidates must be above 0.\n')
                sys.exit(1)
        
        # added by yash
        elif o in ('--acc-matrix-output-file', ):
            acc_matrix_output_file = a  
        elif o in ('--rescoring',):
            rescoring = True
        elif o in ('--rescoring-method',):
            rescoring_method = a
        elif o in ('--word-prob-dict-file',):
            word_prob_dict_file = a
        elif o in ('--result-dict-file',):
            result_dict_file = a
        elif o in ('--alpha',):
            alpha = float(a)
        elif o in ('--correct-predicted-words-file',):
            correct_predicted_words_file = a
        elif o in ('--wrong-predicted-words-file',):
            wrong_predicted_words_file = a
            
        else:
            sys.stderr.write('Error: unknown option %s. Type --help to see the options.\n' % o)
            sys.exit(1)
            
    if check_only:
        if test_fname or output_fname:
            sys.stderr.write('No test file or output file is required to check the input format.\n')
            sys.exit(1)
    else:   
        if not test_fname:
            sys.stderr.write('Error: no test file provided.\n')
            sys.exit(1)
    
    return input_fname, output_fname, test_fname, max_candidates, check_only, silent, acc_matrix_output_file, rescoring, rescoring_method, word_prob_dict_file, result_dict_file, alpha, correct_predicted_words_file, wrong_predicted_words_file
        
    
    
    
    
def parse_xml(f_in, max_targets=None):
    '''
    Parses XML input and test files with paranoid error checking.
    Returns a tuple of header and content
    Content is a dictionary with source names as keys and contains lists of target names.
    If max_targets is given, the number of target names in the list is cut up to max_targets names.
    Header is a dictionary of header data
    '''
    
    stderr = codecs.getwriter('utf-8')(sys.stderr)
    
    doc = xml.dom.minidom.parse(f_in)
    if doc.encoding.lower() != 'utf-8':
        raise IOError('Invalid encoding. UTF-8 is required but %s found' % doc.encoding)
    
    # try results
    header = doc.getElementsByTagName('TransliterationTaskResults')
    is_results = True
    if not header:
        # try corpus
        is_results = False
        header = doc.getElementsByTagName('TransliterationCorpus')
    if not header:
        raise IOError('Unknown file. TransliterationTaskResults and TransliterationCorpus tags are missing')
    if len(header) > 1:
        raise IOError('Invalid file. Several headers were found')
    header = header[0]
    
    # parse the comments
    header_data = {}
    if is_results:
        attr_list = RESULT_HEADER_ATTR
    else:
        attr_list = CORPUS_HEADER_ATTR
        
    for attr in attr_list:
        header_data[attr] = header.getAttribute(attr)
           
    # parse the data
    data = {}
    for node in doc.getElementsByTagName('Name'):
        # we ignore the name ID unless encounter error
        # get the source name
        s = node.getElementsByTagName('SourceName')
        #import ipdb
        #ipdb.set_trace()
        if not s:
            raise IOError('Invalid file format: one of <Name> nodes does not have <SourceName>')
        if s[0].childNodes[0].nodeType == Node.TEXT_NODE:
            src_name = s[0].childNodes[0].data.strip('" ') # strip quotes and spaces in case someone adds them
            src_name = src_name.upper() # convert to uppercase in case it's a language where case matters
        else:
            raise IOError('For Name ID %s no SourceName was found or its format is invalid' % node.getAttribute('ID'))
        
        # get the targets
        t = node.getElementsByTagName('TargetName')
        if not t:
            raise IOError('Invalid file format: one of <Name> nodes does not have <TargetName>')
        # we'll read target names as tuples: (target_name, ID) so that the list can later be sorted
        # according to the ID, which is going to be removed after that.
        tgt_list = []
        for t_node in t:
            # get the ID, which is the rank for transliteration candidates
            try:
                tgt_id = int(t_node.getAttribute('ID'))
            except ValueError as e:
                raise IOError('For name ID %s (%s) one of target names have invalid ID' % (node.getAttribute('ID'), src_name))
            # get the word
            if not t_node.childNodes:
                raise IOError('For name ID %s (%s) one of the target names ID %s is empty' % (node.getAttribute('ID'), src_name, tgt_id))
            if t_node.childNodes[0].nodeType == Node.TEXT_NODE:
                tgt_name = t_node.childNodes[0].data.strip('" ')
                if tgt_name:
                    tgt_name = tgt_name.upper() # convert to uppercase in case it matters
                    tgt_list.append((tgt_name, tgt_id))
                else:
                    stderr.write('Warning: Name ID %s (%s) contains empty target words\n' % (node.getAttribute('ID'), src_name))
            else:
                raise IOError('For name ID %s (%s) one of target names ID %s have invalid format' % (node.getAttribute('ID'), src_name, tgt_id))
                
        # sort by ID
        if not tgt_list:
            stderr.write('Warning: no non-empty target words found for name ID %s (%s). This name is ignored.\n' % (node.getAttribute('ID'), src_name))
            
        else:
            
            #tgt_list.sort(lambda x, y: cmp(x[1], y[1]))
            tgt_list.sort(key = lambda x: x[1])
            # check for duplicate IDs: if there are any, they must be adjacent elements after sorting
            # we only care for IDs to be unique in the results file because IDs are ranks there.
            if is_results:
                for i in range(len(tgt_list)-1):
                    if tgt_list[i][1] == tgt_list[i+1][1]:
                        raise IOError('XML results file contains duplicate IDs for transliterations of word %s' % src_name)
        
            # cut up to max_targets
            if max_targets:
                tgt_list = tgt_list[0:max_targets]
            
            data[src_name] = [tgt[0] for tgt in tgt_list] # remove IDs, we don't need them anymore
        
        # test (codecs.getwriter('utf-8')(sys.stdout)).write('Name: %s\n' % (data[src_name][0]))
        # test raise IOError('%s' % data[src_name][0])
        
    return header_data, data, is_results
    
    
def LCS_length(s1, s2):
    '''
    Calculates the length of the longest common subsequence of s1 and s2
    s1 and s2 must be anything iterable
    The implementation is almost copy-pasted from Wikibooks.org
    '''
    m = len(s1)
    n = len(s2)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n+1) for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C[m][n]
    
    
def f_score(candidate, references):
    '''
    Calculates F-score for the candidate and its best matching reference
    Returns F-score and best matching reference
    '''
    # determine the best matching reference (the one with the shortest ED)
    best_ref = references[0]
    best_ref_lcs = LCS_length(candidate, references[0])
    for ref in references[1:]:
        lcs = LCS_length(candidate, ref)
        if (len(ref) - 2*lcs) < (len(best_ref) - 2*best_ref_lcs):
            best_ref = ref
            best_ref_lcs = lcs
    
    #try:
    precision = float(best_ref_lcs)/float(len(candidate))
    recall = float(best_ref_lcs)/float(len(best_ref))
    #except:
    #    import ipdb
    #    ipdb.set_trace()
    
    if best_ref_lcs:
        return 2*precision*recall/(precision+recall), best_ref
    else:
        return 0.0, best_ref
    
    
    
def mean_average_precision(candidates, references, n):
    '''
    Calculates mean average precision up to n candidates.
    '''
    
    total = 0.0
    num_correct = 0
    for k in range(n):
        if k < len(candidates) and (candidates[k] in references):
            num_correct += 1
        total += float(num_correct)/float(k+1)
        
    return total/float(n)
    
    

def inverse_rank(candidates, reference):
    '''
    Returns inverse rank of the matching candidate given the reference
    Returns 0 if no match was found.
    '''
    rank = 0
    while (rank < len(candidates)) and (candidates[rank] != reference):
        rank += 1
    if rank == len(candidates):
        return 0.0
    else:
        return 1.0/(rank+1)
    
    
def evaluate(input_data, test_data):
    '''
    Evaluates all metrics to save looping over input_data several times
    n is the map-n parameter
    Returns acc, f_score, mrr, map_ref, map_n
    '''
    mrr = {}
    acc = {}
    f = {}
    f_best_match = {}
    #map_n = {}
    map_ref = {}
    #map_sys = {}
    acc_10 = {}
    
    #added by yash
    characc ={}
    error_words = {}
    correct_words = {}
    
    stderr = codecs.getwriter('utf-8')(sys.stderr)
    
    for src_word in list(test_data.keys()):
        if src_word in input_data:
            candidates = input_data[src_word]
            references = test_data[src_word]
            
            acc[src_word] = max([int(candidates[0] == ref) for ref in references]) # either 1 or 0
            
            if acc[src_word]==0:
                error_words[src_word] = {'ref': references, 'candidates' : candidates }
            if acc[src_word]==1:    
                correct_words[src_word] = {'ref': references, 'candidates' : candidates }

            f[src_word], f_best_match[src_word] = f_score(candidates[0], references)
            
            mrr[src_word] = max([inverse_rank(candidates, ref) for ref in references])
            
            #map_n[src_word] = mean_average_precision(candidates, references, n)
            map_ref[src_word] = mean_average_precision(candidates, references, len(references))
            #map_sys[src_word] = mean_average_precision(candidates, references, len(candidates))
            
            ## compute accuracy at 10- Anoop
            acc_10[src_word] = max([int(ref in candidates) for ref in references]) # either 1 or 0
            
            # compute char accuracy
            characc[src_word] = 1 - charerr(references[0], candidates[0])

        else:
            #stderr.write('Warning: No transliterations found for word %s\n' % src_word)
            print('No transliterations')
            mrr[src_word] = 0.0
            acc[src_word] = 0.0
            f[src_word] = 0.0
            f_best_match[src_word] = ''
            #map_n[src_word] = 0.0
            map_ref[src_word] = 0.0
            #map_sys[src_word] = 0.0
            # Anoop
            acc_10[src_word]=0.0
            characc[src_word] = 0.0

    return acc, f, f_best_match, mrr, map_ref, acc_10, characc, error_words, correct_words # added by Anoop
            


def write_details(output_fname, input_data, test_data, acc, f, f_best_match, mrr, map_ref, acc_10):
    '''
    Writes detailed results to CSV file
    '''
    if output_fname == '-':
        f_out = codecs.getwriter('utf-8')(sys.stdout)
    else:
        f_out = codecs.open(output_fname, 'w', 'utf-8')
    
    f_out.write('%s\n' % (','.join(['"Source word"', '"First candidate"', '"ACC"', '"ACC-10"', '"F-score"', '"Best matching reference"',
    '"MRR"', '"MAP_ref"', '"References"'])))
    
    for src_word in list(test_data.keys()):
        if src_word in input_data:
            first_candidate = input_data[src_word][0]
        else:
            first_candidate = ''
            
        f_out.write('%s,%s,%f,%f,%f,%s,%f,%f,%s\n' % (src_word, first_candidate, acc[src_word], acc_10[src_word], f[src_word], f_best_match[src_word], mrr[src_word], map_ref[src_word], '"' + ' | '.join(test_data[src_word]) + '"'))
    
    if output_fname != '-':
        f_out.close()


def main():
    
    input_fname, output_fname, test_fname, max_candidates, check_only, silent, acc_matrix_output_file, rescoring, rescoring_method, word_prob_dict_file, result_dict_file, alpha, correct_predicted_words_file, wrong_predicted_words_file = get_options()
    stderr = codecs.getwriter('utf-8')(sys.stderr)
    
    if not input_fname:
        f = sys.stdin
    else:
        f = input_fname
    try:
        input_header, input_data, is_results = parse_xml(f, max_targets=max_candidates)
    except IOError as e:
        error_message = e.strerror
        if not error_message:
            error_message = e.message
        stderr.write('Error encountered while parsing input: %s.\n' % error_message)
        sys.exit(1)
        
    if check_only:
        stdout = codecs.getwriter('utf-8')(sys.stdout)
        
        if not silent:
            if is_results:
                corpus_type = 'testing or reference'
            else:
                corpus_type = 'training or development'
            stdout.write('This is %s corpus\n' % corpus_type)
            for elem in list(input_header.keys()):
                stdout.write('%30s : %-30s\n' % (elem, input_header[elem]))
            stdout.write('Number of words: %d\n' % len(input_data))
        else:
            stdout.write("OK\n")
            
        sys.exit()
    
    try:
        test_header, test_data, is_results = parse_xml(test_fname)
    except IOError as e:
        error_message = e.strerror
        if not error_message:
            error_message = e.message
        stderr.write('Error encountered while parsing test file. Here is what the parser said:\n%s.\n' % error_message)
        sys.exit(1)
    

    if rescoring:

        # input_data = rescoring_unique_indicorp(input_data)
        # input_data = rescoring_lm(input_data)

        if rescoring_method == 'weighted_avg':
            input_data = rescoring_wt_avg_score_freq(input_data, word_prob_dict_file, result_dict_file, alpha)

    acc, f, f_best_match, mrr, map_ref, acc_10, characc, error_words, correct_words = evaluate(input_data, test_data)
    

    if output_fname:
        write_details(output_fname, input_data, test_data, acc, f, f_best_match, mrr, map_ref, acc_10)
       
    N = len(acc) 

    # temp to tune the alpha parameter 
    # file_acc_alpha = open('output/alpha_accuracy_trend.txt','a')
    # file_acc_alpha.write( str(alpha) + '\t'  + str((float(sum([acc[src_word] for src_word in list(acc.keys())]))/N)) + '\n' )
    # file_acc_alpha.close()



    sys.stdout.write('ACC:          %f\n' % (float(sum([acc[src_word] for src_word in list(acc.keys())]))/N))
    sys.stdout.write('Mean F-score: %f\n' % (float(sum([f[src_word] for src_word in list(f.keys())]))/N))
    sys.stdout.write('MRR:          %f\n' % (float(sum([mrr[src_word] for src_word in list(mrr.keys())]))/N))
    sys.stdout.write('MAP_ref:      %f\n' % (float(sum([map_ref[src_word] for src_word in list(map_ref.keys())]))/N))
    sys.stdout.write('ACC@10:       %f\n' % (float(sum([acc_10[src_word] for src_word in list(acc_10.keys())]))/N))
    sys.stdout.write('CharACC:       %f\n' % (float(sum([characc[src_word] for src_word in list(characc.keys())]))/N))
    
    #sys.stdout.write('MAP_%d:       %f\n' % (n, float(sum([map_n[src_word] for src_word in map_n.keys()]))/N))
    #sys.stdout.write('MAP_sys:      %f\n' % (float(sum([map_sys[src_word] for src_word in map_sys.keys()]))/N))
    
    # added by yash
    # write results to file metric_score.txt
    file_matrix_score = open(acc_matrix_output_file, 'w')
    file_matrix_score.write('ACC:          %f\n' % (float(sum([acc[src_word] for src_word in list(acc.keys())]))/N) )
    file_matrix_score.write('Mean F-score: %f\n' % (float(sum([f[src_word] for src_word in list(f.keys())]))/N))
    file_matrix_score.write('MRR:          %f\n' % (float(sum([mrr[src_word] for src_word in list(mrr.keys())]))/N))
    file_matrix_score.write('MAP_ref:      %f\n' % (float(sum([map_ref[src_word] for src_word in list(map_ref.keys())]))/N))
    file_matrix_score.write('ACC@10:       %f\n' % (float(sum([acc_10[src_word] for src_word in list(acc_10.keys())]))/N))
    file_matrix_score.write('CharACC:       %f\n' % (float(sum([characc[src_word] for src_word in list(characc.keys())]))/N))
    
    file_matrix_score.close()

    file_error_words = open(wrong_predicted_words_file, 'w')
    error_words_list = []
    for source_word in error_words.keys() :
                
        string = 'S : '+ source_word
        string +='\t ref : '
        string += ','.join(error_words[source_word]['ref'])
        string += '\t candidates : ['
        string += ','.join(error_words[source_word]['candidates'])
        string += ']'

        error_words_list.append(string)

    # error_words_list = list(set(error_words_list))
    file_error_words.write('\n'.join(error_words_list))
    file_error_words.close()

    file_correct_words = open(correct_predicted_words_file, 'w')
    correct_words_list = []
    for source_word in correct_words.keys() :
                
        string = 'S : '+ source_word
        string +='\t ref : '
        string += ','.join(correct_words[source_word]['ref'])
        string += '\t candidates : ['
        string += ','.join(correct_words[source_word]['candidates'])
        string += ']'

        correct_words_list.append(string)

    # correct_words_list = list(set(correct_words_list))
    file_correct_words.write('\n'.join(correct_words_list))
    file_correct_words.close()

def test():
    stdout = codecs.getwriter('utf-8')(sys.stdout)
    input_header, input_data, is_result = parse_xml('news_results.xml', max_targets=10)
    test_header, test_data, is_result = parse_xml('news_test.xml')
    acc, f, f_best_match, mrr, map_ref = evaluate(input_data, test_data)
    for src_word in list(test_data.keys()):
        stdout.write('%10s ACC=%f\tF-score=%f (%s)\tMRR=%f\tMAP_ref=%f\n' % (src_word, acc[src_word], f[src_word], f_best_match[src_word], mrr[src_word], map_ref[src_word]))

if __name__ == '__main__':
    main()
    #test()
