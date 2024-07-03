import random
import sys
import DecisionTree
import json

if len(sys.argv) != 7:
    print("Provide arguments:\ndata.json, <position of result value>, <max tree depth>, <max examples in leaf>, <number of examples per tree>, <number of trees>")
    sys.exit(0)

TREE_ARR = []
TREE1 = DecisionTree
data = []

try:                            #wczytanie data.json
    with open(sys.argv[1], 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Provided JSON file doesn't exist.")
    sys.exit(0)
except Exception as e:
    print("Encountered an error while reading the JSON file: ", e)
    sys.exit(0)

empty_data = []
for i in range(len(data)):
    empty_data.append(0)

TREE1.LookingFor = int(sys.argv[2])  #position of result value

empty_Arr = []                  #max depth
for i in range(2**int(sys.argv[3])):
    empty_Arr.append(0)
TREE1.TREE = empty_Arr.copy()
TREE1.Depth_Max = 2**int(sys.argv[3])

TREE1.Maksimum_Elems = int(sys.argv[4])   #max examples in leaf

d_per_tree = int(sys.argv[5])        #examples per tree
maks_tree_amm = int(sys.argv[6])     #number of trees


subset_data = random.choices(data,k=d_per_tree)    #make the first tree
TREE1.Make_node(subset_data,1)
TREE_ARR.append(TREE1.TREE.copy())

#untill we have all the trees
while len(TREE_ARR) < maks_tree_amm :
    
    #calculate the errors for all examples
    mean_arr = empty_data.copy()
    mean_err = empty_data.copy()

    for t in range(len(TREE_ARR)):
        TREE1.TREE = TREE_ARR[t]

        for i in range(len(data)):
            mean_arr[i] += TREE1.calculate(data[i])
            
    for i in range(len(data)):
        mean_arr[i] = mean_arr[i]/len(TREE_ARR)
        mean_err[i] = ((abs(mean_arr[i]-data[i][TREE1.LookingFor]))/data[i][TREE1.LookingFor])*100

    print("Mean: ",sum(mean_err)/len(mean_err),"\t Min: ",min(mean_err),"\t Max: ",max(mean_err))
    
    #choose examples the model is more wrong on
    subset_data = random.choices(data, weights=mean_err ,k=d_per_tree)
    
    #make next tree
    TREE1.TREE = empty_Arr.copy()
    TREE1.Make_node(subset_data,1)
    TREE_ARR.append(TREE1.TREE.copy())

try:
    with open('forest.json', 'w') as json_file:
            json.dump(TREE_ARR, json_file)
except Exception as e:
    print("Encountered an error while saving files: ", e)
