# takes in as an argument a .csv file and optionally a mapping.json
# it returns data.json and mapping.json
# data.json is a table of ints understandable by our program, ready for training
# mapping.json is used if you have multeaple files that need converting, it keeps the convertion sonsistant

import csv
import sys
import json
from datetime import datetime

#change to the earliest date in your dataset with the correct date format
base_date = datetime(2022, 1, 1)
#make sure the date format is YYYY-MM-DD (with dashes)

provided_mapping = False
mapping_update = False

if len(sys.argv) == 3:
    provided_mapping = True
elif len(sys.argv) != 2:
    print("Provide a CSV file as an argument.")
    sys.exit(0)

csv_file_path = sys.argv[1]
data_read = []

#read csv
try:
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        for row in reader:
             data_read.append(row)
except FileNotFoundError:
    print("Provided CSV file doesn't exist.")
except Exception as e:
    print("Encountered an error while reading the CSV file: ", e)

if len(data_read) < 1 or len(data_read[0]) < 1:
     print("The CSV file is empty.")
     sys.exit(0)

mapping = []
types = []
data_to_save = []

elem_len = len(data_read[0])

#if json was provided
if provided_mapping:
    try:
        with open(sys.argv[2], 'r') as json_file:
            data = json.load(json_file)
            types = data[0]
            mapping = data[1]
    except FileNotFoundError:
        print("Provided JSON file doesn't exist.")
        sys.exit(0)
    except Exception as e:
        print("Encountered an error while reading the JSON file: ", e)
        sys.exit(0)

else:
    #else init mappings
    for i in range(elem_len):
        mapping.append([])

    for i in data_read[0]:
        if len(i) == 10 and i[4] == "-":
            types.append('d')
        elif i.isnumeric():
            types.append('i')
        else:
            types.append('s')

#replace data with mapping
for i in data_read:
     temp = []
     for j in range(elem_len):
        match types[j]:
            case 'd':
                datetime_str = datetime.strptime(i[j],"%Y-%m-%d")
                diff = datetime_str - base_date
                minutes = int(diff.total_seconds() / 86400)
                temp.append(minutes)
            case 's':
                if i[j] in mapping[j]:
                    for a in range(len(mapping[j])):
                        if mapping[j][a] == i[j]:
                            temp.append(a)
                else:
                    mapping_update = True
                    mapping[j].append(i[j])
                    temp.append(len(mapping[j])-1)
            case _:
                try:
                    temp.append(int(i[j]))
                except Exception as e:
                    print("Unexpected error: ", i)
    
     data_to_save.append(temp)
          

#print(data_to_save,'\n=====\n',types,'\n=====\n',mapping)

#make files
try:
    if provided_mapping:
        with open('data.json', 'w') as json_file:
            json.dump(data_to_save, json_file)
        print("Data was saved to data.json\n")
        if mapping_update:
            with open('mapping.json', 'w') as json_file:
                json.dump([types,mapping], json_file)
            print("Warning! There were new values - mapping.json was overwritten.")
    else:
        with open('data.json', 'w') as json_file:
            json.dump(data_to_save, json_file)
        with open('mapping.json', 'w') as json_file:
            json.dump([types,mapping], json_file)
        print("Data was saved to data.json\nIf you want to use the same mapping for other files a mapping.json was created.")
except Exception as e:
    print("Encountered an error while saving files: ", e)


sys.exit(0)
