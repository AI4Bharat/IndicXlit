from itertools import chain, islice
import cld3

def chunks(iterable, n):
   iterable = iter(iterable)
   while True:
       yield chain([next(iterable)], islice(iterable, n - 1))

lang = 'hi'
l =  3 * 10**6
count = 0
file_large = f'/home/cs20m050/Text/{lang}/{lang}.txt'
lines_stats = f'/home/cs20m050/Text/{lang}/{lang}_lines_reduced_after_cld3.txt'
with open(file_large, encoding='utf-8') as bigfile:
    with open(lines_stats, 'w', encoding='utf-8') as stats:
        for i, lines in enumerate(chunks(bigfile, l)):
            file_split = '{}.{}'.format(file_large, i)
            with open(file_split, 'w', encoding='utf-8') as f:
                count = 0
                for line in lines:
                    p = cld3.get_language(line)
                    if p.language == lang: 
                        f.write(line)
                        count += 1
                stats.write('File '+ str(i) + ' Total lines: '+str(l)+ ' Reduced_to: '+str(count)+ ' Reduction: '+str(l-count) +'\n')
