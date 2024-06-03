# Program przyjmuje jako argument plik .csv i zwraca data.json
# Zwrócony plik jest tabelą intą zrozumiałą przez nasz program

import csv
import sys
import json
from datetime import datetime

base_date = datetime(2022, 1, 1)
provided_mapping = False
mapping_update = False

if len(sys.argv) == 3:
    provided_mapping = True
elif len(sys.argv) != 2:
    print("Podaj ścieżkę do pliku CSV jako argument.")
    sys.exit(0)

csv_file_path = sys.argv[1]
data_read = []


try:
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        for row in reader:
             data_read.append(row)
except FileNotFoundError:
    print("Podany plik csv nie istnieje.")
except Exception as e:
    print("Wystąpił błąd podczas odczytu pliku csv:", e)

if len(data_read) < 1 or len(data_read[0]) < 1:
     print("Plik jest pusty.")
     sys.exit(0)

mapping = []
types = []
data_to_save = []

elem_len = len(data_read[0])

if provided_mapping:
    try:
        with open(sys.argv[2], 'r') as json_file:
            data = json.load(json_file)
            types = data[0]
            mapping = data[1]
    except FileNotFoundError:
        print("Podany plik json nie istnieje.")
        sys.exit(0)
    except Exception as e:
        print("Wystąpił błąd podczas odczytu pliku json:", e)
        sys.exit(0)

else:

    for i in range(elem_len):
        mapping.append([])

    for i in data_read[0]:
        if len(i) == 10 and i[4] == '-':
            types.append('d')
        elif i.isnumeric():
            types.append('i')
        else:
            types.append('s')


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
                    print(i)
    
     data_to_save.append(temp)
          

#print(data_to_save,'\n=====\n',types,'\n=====\n',mapping)


try:
    if provided_mapping:
        with open('data.json', 'w') as json_file:
            json.dump(data_to_save, json_file)
        print("Dane zostały zapisane do pliku data.json\n")
        if mapping_update:
            with open('mapping.json', 'w') as json_file:
                json.dump([types,mapping], json_file)
        print("Uwaga! Wśród danych były niespodziewane wartości. Plik mapping.json został napisany.")
    else:
        with open('data.json', 'w') as json_file:
            json.dump(data_to_save, json_file)
        with open('mapping.json', 'w') as json_file:
            json.dump([types,mapping], json_file)
        print("Dane zostały zapisane do pliku data.json \nJeżeli chcesz użyć takiego samego przypisania dla innych danych zostało ono zapisane jako mapping.json")
except Exception as e:
    print("Wystąpił błąd podczas zapisywania danych do pliku:", e)


sys.exit(0)
