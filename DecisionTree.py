import sys

#stores the tree as a binary tree of decisions
TREE = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

Depth_Max = 32  #maximum depth (last index of TREE array)
Maksimum_Elems = 2   #maximum number of examples in a leaf

LookingFor = 2  #position of the result

#quality of division
def SSR(Data,a,b):
    SUM_yes = 0
    SUM_no = 0
    AMM_yes = 0
    AMM_no = 0
    res = 0

    #calculating the average
    for i in range(len(Data)):
        if Data[i][a] < b:
            SUM_yes += Data[i][LookingFor]
            AMM_yes += 1
        else:
            SUM_no += Data[i][LookingFor]
            AMM_no += 1
    
    #calculating the sum of squered residuals
    for i in range(len(Data)):
        if Data[i][a] < b:
            res += (Data[i][LookingFor]-(SUM_yes/AMM_yes))**2.0
        else:
            res += (Data[i][LookingFor]-(SUM_no/AMM_no))**2.0
    
    return res

#recursive creation of nodes
def Make_node(Data_Arr, Index):
    #print(Index," - ",Data_Arr,"\n")

    #stop condition
    if len(Data_Arr) <= Maksimum_Elems or (Index*2)+1 > Depth_Max:

        if len(Data_Arr) == 0: #this shouldn't happen
            TREE[Index] = -1
            return

        sum = 0
        for i in Data_Arr:
            sum += i[LookingFor]
        
        TREE[Index] = sum/len(Data_Arr)
        return
    
    S = sys.maxsize
    A = 0
    B = 0

    #find a division with lowest SSR
    for a in range(len(Data_Arr[0])):
        if a != LookingFor:

            Data_Arr.sort(key=lambda x: x[a])

            for b in range(0,len(Data_Arr)-1):

                if Data_Arr[b][a] != Data_Arr[b+1][a]:

                    s = SSR(Data_Arr, a, (Data_Arr[b][a] + Data_Arr[b+1][a])/2 )
                    if s < S:
                        S = s
                        A = a
                        B = (Data_Arr[b][a] + Data_Arr[b+1][a])/2
                    
                    pass
    
    #divide and run for children
    TREE[Index] = [A,B]

    Left_Arr = []
    Right_Arr = []
    
    #divide using the calculated best division
    for i in range(len(Data_Arr)):
        if Data_Arr[i][A] < B:
            Left_Arr.append(Data_Arr[i])
        else:
            Right_Arr.append(Data_Arr[i])
    
    Make_node(Left_Arr,Index*2)
    Make_node(Right_Arr,(Index*2)+1)
    return

    #oblicz wynik
def calculate(wal) -> int:
    curr = 1
    while True:
        if( type(TREE[curr]) is list ):
            if( wal[ TREE[curr][0] ] < TREE[curr][1] ):
                curr = curr*2
            else:
                curr = (curr*2) +1
        else:
            return TREE[curr]



#not very good visualisation but you can see the first 4 levels
def show_tree():

    l = 30
    r = 1
    pos = 2
    print((l-3)*" ",TREE[1])
    for i in range(4):
        l = int(l*0.6)
        v = l*" "
        r = r*2
        for j in range(r):
            v += str(TREE[pos])
            t = l-int(len(str(TREE[pos]))/2)
            if t > 0: v += t * " "
            pos += 1
        print(v)
        

    pass
#it works :>
if __name__ == "__main__":

    ARR = [
        [3,1,3],
        [0,2,5],
        [3,2,8],
        [1,1,1],
        [1,2,6],
        [4,1,4],
        [3,1,3],
        [1,2,6]
    ]
    Make_node(ARR,1)
    print(TREE)

    show_tree()
    print( calculate([2,1,7]) )
    


