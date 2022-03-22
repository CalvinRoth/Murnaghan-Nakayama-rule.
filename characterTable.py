
from itertools import combinations
import re
from tkinter import W
import numpy as np 
import networkx as nx 
from math import factorial as fact 
import pandas as pd

parts6 = [
    [1,1,1,1,1,1],
    [2,1,1,1,1],
    [3,1,1,1],
    [4,1,1],
    [5,1],
    [6],
    [2,2,1,1],
    [3,2,1],
    [3,3],
    [4,2],
    [2,2,2]
]
parts5 =  [
    [1,1,1,1,1],
    [2,1,1,1],
    [2,2,1],
    [3,2],
    [3,1,1],
    [4,1],
    [5]
]


parts4 = [
    [1,1,1,1],
    [2,1,1],
    [2,2],
    [3,1],
    [4]
]
parts3 = [
    [1,1,1],
    [2,1],
    [3]
]

# we generate square arrays because they are easier to work with that true tableaux
# an entry with value -1 indicates off limits and 0 indiciates unassigned 
def genShapes(parts):
    shapes = [] 
    for part in parts:
        m = max(part)
        m = max(m, len(part))
        mat = np.zeros( (m,m) , dtype=int)
        mat.fill(-1)
        for i in range(len(part)):
            for j in range(part[i]):
                mat[i,j] = 0
        shapes.append(mat)
    return shapes
     
def getEmptys(arr):
    res = []
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if( arr[i,j] == 0):
                res.append(  (i,j))
    return res

def fillShape(shap, coordinates, val):
    for coord in coordinates:
        shap[coord[0]][coord[1]] = val 

def copyArr(arr):
    res = []
    for i in arr:
        r = []
        for j in i:
            r.append(j)
        res.append(r)
    return res 

def guessShape(pool, next_val, res):
    if(len(pool) == 0): return res
    old = res.copy()
    new_one = []
    for i in old:
        emptys = getEmptys(i)
        combos = combinations(emptys, pool[0])

        for combo in combos:
            #arr = copyArr(i)
            arr = i.copy()
            fillShape(arr, combo, next_val)
            new_one.append( arr)
    pool.pop(0)
    #print(next_val)
    return guessShape(pool, next_val+1, new_one)




def squareCheck(guess):
    n = len(guess)
    for i in range(1,n):
        for j in range(1, n):
            if(guess[i,j] == -1): continue 
            b1 = guess[i-1,j] == guess[i,j]
            b2 = guess[i,j-1] == guess[i,j]
            b3 = guess[i-1, j-1] == guess[i,j]
            if(b1 and b2 and b3):
                return False 
    return True 




def stripCheckhelper(guess,val):
    d = dict()
    for i in range(len(guess)):
        for j in range(len(guess)):
            if(guess[i,j] != val): continue 
            d[(i,j)] =  []
            if(i > 0 and guess[i-1,j] == val): 
                d[(i,j)] += (i-1,j)
            if(i <= len(guess)-2 and guess[i+1, j] == val ):
                d[(i,j)] += (i+1, j)
            if(j > 0 and guess[i,j-1] == val): 
                d[(i,j)] += (i,j-1)
            if(j <= len(guess)-2 and guess[i, j+1] == val ):
                d[(i,j)] += (i, j+1)   
    g =   nx.to_networkx_graph(d)
    b = nx.is_connected(g)
    return b

def stripCheck(guess):
    m = np.max(guess)
    for val in range(1, m+1):
        if( not stripCheckhelper(guess, val) ): return False
    return True 

def columnCheck(guess):
    return rowCheck(guess.T)

def rowCheck(guess):
    j = 0 
    for row in guess:
        for i in range(1, len(row)):
            if(guess[j][i] == -1): continue
            if(guess[j][i-1] > guess[j][i]):
                return False
        j += 1
    return True 
        
def height(tab):
    total = 0
    m = np.max(tab)
    for val in range(1, m+1):
        locations = np.argwhere(tab==val)
        rows = {i[0] for i in locations}
        total += len(rows)-1
    return total
        


def nonEmpty(guess):
    for row in guess:
        for col in row:
            if( col != -1):
                return True
    return False
def filter(guess):
    return rowCheck(guess) and columnCheck(guess) and squareCheck(guess) and nonEmpty(guess) and stripCheck(guess)
     


    

# change qparts to eval a different sym group 
qparts = parts4
str_parts = [str(i) for i in qparts]
n = len(qparts)
parts = genShapes(qparts)
res = np.zeros((n,n))
amounts = np.zeros((n,n))
s = 0
i = 0
j = 0
for i in range(n):
    lamb = parts[i]
    for j in range(n):
        rho = qparts[j]
        guesses = guessShape(
            rho.copy(), 
            1, 
            [lamb]
        )
        
        total = 0 
        bsts = [i for i in guesses if filter(i)]
        s += len(bsts)
        for guess in bsts:
            h = height(guess)
            total += (-1)**(h)
        res[i,j] = total 
        amounts[i,j] = len(bsts)

df = pd.DataFrame(res, columns=str_parts)
df.insert(0, "Shape", str_parts)
print(df.to_latex())
