#Program czyta plik data.json i zwraca forest.json który jest nauczonym modelem na podstawie danych
import random
import sys
import DecisionTree
import json

if len(sys.argv) != 7:
    print("Podaj w tej kolejności jako argumenty:\ndata.json, <pozycje szukanej wartości>, <maks głębokość drzewa>, <minimalną ilość elementów w liściu>, <ilość przykładów na drzewo>, <maksymalna ilość drzew>")
    sys.exit(0)

TREE_ARR = []
TREE1 = DecisionTree
data = []

try:                            #wczytanie data.json
    with open(sys.argv[1], 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Podany plik json nie istnieje.")
    sys.exit(0)
except Exception as e:
    print("Wystąpił błąd podczas odczytu pliku json:", e)
    sys.exit(0)

empty_data = []
for i in range(len(data)):
    empty_data.append(0)

TREE1.LookingFor = int(sys.argv[2])  #pozycja szukanej wartości

empty_Arr = []                  #maksymalna głębokość
for i in range(2**int(sys.argv[3])):
    empty_Arr.append(0)
TREE1.TREE = empty_Arr.copy()
TREE1.Depth_Max = 2**int(sys.argv[3])

TREE1.Minimum_Elems = int(sys.argv[4])   #minimalna ilość elementów

d_per_tree = int(sys.argv[5])        #ilość przykłaów na drzewo
maks_tree_amm = int(sys.argv[6])     #maksymalna ilość drzew


elementy = random.choices(data,k=d_per_tree)    #pierwsze drzewo bez wag
TREE1.Make_node(elementy,1)
TREE_ARR.append(TREE1.TREE.copy())


while len(TREE_ARR) < maks_tree_amm :

    mean_arr = empty_data.copy()

    for t in range(len(TREE_ARR)):
        TREE1.TREE = TREE_ARR[t]

        for i in range(len(data)):
            mean_arr[i] += TREE1.calculate(data[i])
            
    for i in range(len(data)):
        mean_arr[i] = mean_arr[i]/len(TREE_ARR)
    print(mean_arr[0]," ",mean_arr[1]," ",mean_arr[2]," ",mean_arr[3]," ",mean_arr[4])
    elementy = random.choices(data, weights=mean_arr ,k=d_per_tree)
    
    TREE1.TREE = empty_Arr.copy()
    TREE1.Make_node(elementy,1)
    TREE_ARR.append(TREE1.TREE.copy())

try:
    with open('forest.json', 'w') as json_file:
            json.dump(TREE_ARR, json_file)
except Exception as e:
    print("Wystąpił błąd podczas zapisywania danych do pliku:", e)
