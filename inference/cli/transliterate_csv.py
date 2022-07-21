import numpy
import pandas as pd
import csv
import os
import sys
import argparse

parser=argparse.ArgumentParser(description='Transliterates words from English-Hindi ')
parser.add_argument("input", help= "csv file name")

args = parser.parse_args()


def input_csv_exception():
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Input CSV not passed: Please specify a file name")
        sys.exit(1)

def main():
    input_csv_exception()

    input_csv = sys.argv[1]

    # reading the csv file
    df = pd.read_csv(input_csv)

    #save as txt
    df.to_csv('/datadrive/translit/IndicXlit/IndicXlit/inference/cli/cycles_clean.txt', index = False)

    text_file = open('cycles_clean.txt', 'r')
    text = text_file.read()
    text = text.lower()
    words = text.split()
    #only for 91cycles example, delete later 
    #words = [word.lower() for word in words]
    words = [word.strip('0123456789') for word in words]


    #for word in words:
    #    if word.isnumeric():
    #        raise ValueError("No numeric values should eb present in csv")

    

    for i in words:
        if i.isnumeric():
            print("Incorrect values: Numeric values found")
            return("Incorrect values: Numeric values found")


    #finding unique
    unique = []
    for word in words:
        if word not in unique:
            unique.append(word)

    #sort
    unique.sort()

    #add spaces
    unique_with_space = []
    for i in unique:
        my_str = i
        result = ' '.join(my_str)
        unique_with_space.append(result)

    #write csv file with spaces
    with open('cycles_with_space.csv', mode='w') as outfile:
        out_writer = csv.writer(outfile, delimiter = ' ')
        for i in unique_with_space:
            out_writer.writerow([i])

    df = pd.read_csv('cycles_with_space.csv')

    #save in txt source file
    df.to_csv('/datadrive/translit/IndicXlit/IndicXlit/inference/cli/source/source.txt', index = False)

    #bash commands
    #!bash transliterate_word.sh 'hi' 
    # !cat output/final_transliteration.txt 

    cmd = "bash transliterate_word.sh 'hi' "
    returned_value = os.system(cmd)  # returns the exit code in unix


    eng_dictionary = {}
    with open("output/final_transliteration.txt") as file:
        for line in file:
            (key, value) = line.split()
            eng_dictionary[str(key).replace(':', '')] = value
    

    #latest
    filename = input_csv
    input_list = []
    output_list = []


    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            input_list.append(row[0])
            input = row[0].split()

            # print(input)
            
            combine = []
            for i in input:
                lower_input = i.lower()
                # print(lower_input)
                if lower_input in eng_dictionary:
                    combine.append(eng_dictionary[lower_input])
                    # print(i, ':', eng_dictionary[lower_input])      
            output_list.append(' '.join(combine))

    with open('final_stitched_output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(input_list, output_list))


if __name__ == "__main__":
    main()
