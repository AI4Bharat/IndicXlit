import csv
lang_abr_list = ['as','bn', 'gu', 'hi', 'kn', 'mr','or','pa', 'ta', 'te']
lang_list = ['Assamese','Bangla', 'Gujarati', 'Hindi', 'Kannada', 'Marathi', 'Oriya','Punjabi', 'Tamil', 'Telugu']


for lang,lang_abr in zip(lang_list,lang_abr_list):

    with open('/home/yashmadhani1997/Indic_xlit/validation/en-'+lang_abr+'/1-1.'+lang_abr+'-en.mined-pairs', 'r', encoding='utf-8') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\t") for line in stripped if line)
        with open('/home/yashmadhani1997/Indic_xlit/validation/output/mined-pairs/'+lang_abr+'-en.csv', 'w', encoding='utf-8', newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerow((lang, 'English'))
            writer.writerows(lines)
