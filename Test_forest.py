import sys
import DecisionTree
import json

if len(sys.argv) != 2:
    print("Provide as an argument a .json file with examples to test the tree on.")
    sys.exit(0)

data = []

try:
    with open(sys.argv[1], 'r') as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Provided JSON file doesn't exist.")
    sys.exit(0)
except Exception as e:
    print("Encountered an error while reading the JSON file: ", e)
    sys.exit(0)

forest = []

try:
    with open("forest.json", 'r') as json_file:
        forest = json.load(json_file)
except FileNotFoundError:
    print("Couldn't find a forest.json file in this folder.")
    sys.exit(0)
except Exception as e:
    print("Encountered an error while reading the forest.json file: ", e)
    sys.exit(0)

TREE1 = DecisionTree

mean_arr = []
for i in range(len(data)):
    mean_arr.append(0)

for t in forest:
    TREE1.TREE = t

    for i in range(len(data)):
        mean_arr[i] += TREE1.calculate(data[i])
            

mean_err = []
for i in range(len(data)):

    mean_arr[i] = mean_arr[i]/len(forest)
    mean_err.append(((abs(mean_arr[i]-data[i][2]))/data[i][2])*100)
    print("Res: ",mean_arr[i],"\t Exp: ",data[i][2],"\t Err: ", mean_err[i])
print("Mean: ",sum(mean_err)/len(data),"\t Min: ",min(mean_err),"\t Max: ",max(mean_err))

