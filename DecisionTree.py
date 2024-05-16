import sys


TREE = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

Depth_Max = 32
Minimum_Elems = 2

LookingFor = 2

def SSR(Data,a,b):
    SUM_Tak = 0
    SUM_Nie = 0
    AMM_Tak = 0
    AMM_Nie = 0
    wyn = 0

    #obliczanie średniej
    for i in range(len(Data)):
        if Data[i][a] < b:
            SUM_Tak += Data[i][LookingFor]
            AMM_Tak += 1
        else:
            SUM_Nie += Data[i][LookingFor]
            AMM_Nie += 1
    
    #obliczanie różnicy kwadratów
    for i in range(len(Data)):
        if Data[i][a] < b:
            wyn += (Data[i][LookingFor]-(SUM_Tak/AMM_Tak))**2.0
        else:
            wyn += (Data[i][LookingFor]-(SUM_Nie/AMM_Nie))**2.0
    
    return wyn


def Make_node(Data_Arr, Index):
    #print(Index," - ",Data_Arr,"\n")

    #warunek stopu
    if len(Data_Arr) <= Minimum_Elems or (Index*2)+1 > Depth_Max:

        if len(Data_Arr) == 0: #to nie powinno sie dziać
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

    #znajdź podział o najniższym SSR
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
    
    #dokonaj podziału i wykonaj się dla dzieci
    TREE[Index] = [A,B]

    Left_Arr = []
    Right_Arr = []

    for i in range(len(Data_Arr)):
        if Data_Arr[i][A] < B:
            Left_Arr.append(Data_Arr[i])
        else:
            Right_Arr.append(Data_Arr[i])
    
    Make_node(Left_Arr,Index*2)
    Make_node(Right_Arr,(Index*2)+1)
    return



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




if __name__ == "__main__":

    ARR = [
        [3,1,3],
        [0,2,5],
        [3,2,8],
        [1,1,1],
        [1,2,6],
        [4,1,4],
        [3,1,3],
        [1,2,6],
        [2,2,7]
    ]
    Make_node(ARR,1)
    print(TREE)

    show_tree()
    


