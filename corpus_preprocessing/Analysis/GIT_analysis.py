import http.client
import os
import glob
import csv
from Offset import *

path = '/Users/priyankabedekar/Downloads/drive-download-20210930T061113Z-001/'
outpath = '/Users/priyankabedekar/Desktop/SSKLS-P3/'
csv_files = glob.glob(os.path.join(path, "*.csv"))

def request(input):
    conn = http.client.HTTPSConnection('inputtools.google.com')
    conn.request('GET', '/request?text=' + input + '&itc=' + lang + '-t-i0-und' + '&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test')
    res = conn.getresponse()
    return res

def driver(input_indic, input):
    output = ''
    res = request(input = input)
    res = res.read()
    output = str(res, encoding = 'utf-8')[14 + 4 + len(input): -31]
    if input_indic == output: return True
    return False

for inputfile in csv_files:
    file = os.path.basename(inputfile)
    lang = os.path.splitext(file)[0].split('_',1)[0]
    offset = globals()[lang.upper()]
    # if (lang == 'as'):
    #     lang = 'bn'
    # if (lang == 'kok'):
    #     lang = 'mr'
    # elif(lang == 'mai' or lang == 'doi' or lang == 'ks' or lang == 'brx'):
    #     lang = 'hi'
    outputfile = outpath + 'stats-' + file
    with open(inputfile, 'r') as in_file:
        csv_file_in = csv.reader(in_file)
        length = 0
        with open(outputfile, 'w') as out_file:
            avg_avg = 0.0
            total_true_valid = 0
            total_true_invalid = 0
            csv_file_out = csv.writer(out_file)
            for i, temp_row in enumerate(csv_file_in):
                row = temp_row[1:]
                length += 1
                avg = 0.0
                true_valid = 0
                true_invalid = 0
                R = []
                temp_indic = ""
                R.append(row[0])
                for i in row[0]:
                    temp_indic += str(chr(ord(i) - int(offset)))
                R.append(temp_indic)
                for i in range(1, int((len(row) + 1) / 2)):
                    temp = driver(row[0], row[(2 * i) - 1])
                    R.append(row[(2 * i) - 1])
                    R.append(row[(2 * i)])
                    R.append(temp)
                    if row[(2 * i)] == "VALID" and temp == True:
                        true_valid += 1
                    elif row[(2 * i)] == "INVALID" and temp == True:
                        true_invalid += 1
                csv_file_out.writerow(R)
                avg = true_valid / ((len(row) - 1) / 2)
                total_true_invalid += true_invalid
                total_true_valid += true_valid
                avg_avg += avg 
            avg_avg = avg_avg / length
            csv_file_out.writerow(["True Valid XLits", total_true_valid])
            csv_file_out.writerow(["True Invalid XLits", total_true_invalid])
            csv_file_out.writerow(["Average True XLits / Word", avg_avg])
                

        