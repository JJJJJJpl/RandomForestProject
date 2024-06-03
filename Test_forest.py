#plik przyjmuje argument .json i na podstawie pliku forest.json sprawdza wyniki dla każdego testu i je wyświetla + zapisuje do pliku test_log.txt

import sys
import DecisionTree
import json

if len(sys.argv) != 2:
    print("Podaj jako argument plik .json który zawiera dane do przetestowania.")
    sys.exit(0)

data = []

try:                            #wczytanie danych
    with open(sys.argv[1], 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Podany plik json nie istnieje.")
    sys.exit(0)
except Exception as e:
    print("Wystąpił błąd podczas odczytu pliku json:", e)
    sys.exit(0)

forest = []

try:                            #wczytanie forst.json
    with open("forest.json", 'r') as json_file:
        forest = json.load(json_file)
except FileNotFoundError:
    print("Nie znaleziono forst.json w tym folderze.")
    sys.exit(0)
except Exception as e:
    print("Wystąpił błąd podczas odczytu pliku forest.json:", e)
    sys.exit(0)

TREE1 = DecisionTree

mean_arr = []
for i in range(len(data)):
    mean_arr.append(0)

for t in forest:
    TREE1.TREE = t

    for i in range(len(data)):
        mean_arr[i] += TREE1.calculate(data[i])
            
sum = 0
mean_err = []
for i in range(len(data)):
    mean_arr[i] = mean_arr[i]/len(forest)
    mean_err.append(((abs(mean_arr[i]-data[i][2]))/data[i][2])*100)
    print("W: ",mean_arr[i],"\t P: ",data[i][2],"\t E: ", mean_err[i])
    sum += mean_err[i]
print("Śr: ",sum/len(data),"\t Min: ",min(mean_err),"\t Max: ",max(mean_err))

