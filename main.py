#Sydnee Boothby CPTS350 Project

#Step 3.1 complete 03.28

#required prereqs before doing boolean simplifications
from pyeda.inter import *
from pyeda.boolalg.bdd import BDDONE, BDDZERO

#set constants
zero = expr(0)
one = expr(1)

#2^5=32, need 5 bits to rep all nodes (dest & src)
xvars = [bddvar('x', i) for i in range(5)]
yvars = [bddvar('y', i) for i in range(5)]

R = BDDZERO

#for testing, check if a single node bdd exists (mod of check_edge)
def check_node(bdd, i):
    point = {}
    for k in range(5):
        point[xvars[k]] = (i >> k) & 1
    return bdd.restrict(point) == BDDONE

#restricter function to check if edge exists
def check_edge(bdd, i, j):
    point = {}
    for k in range(5):
        point[xvars[k]] = (i >> k) & 1
        point[yvars[k]] = (j >> k) & 1
    return bdd.restrict(point) == BDDONE

def int_to_bdd(n, vars): #determine bool representation of number (if each bit is on or off)
    result = BDDONE
    for i in range(5):
       bit =  (n>>i) & 1
       if bit == 1:
           result = result & vars[i]
       else:
           result = result & ~vars[i]
           
    return result

#1. Determine RR (all nodes)
#determine if edge exists between i and j nodes
for i in range(32):
    for j in range(32):
        if (i+3)%32 == j or (i+8)%32 == j:
            R = R | int_to_bdd(i, xvars) & int_to_bdd(j, yvars) #add new node connections to R
    #return?

#2. Determine BDD of EVEN subset
EvenBDD = BDDZERO

for i in range(32):
    if i%2 == 0:
        EvenBDD = EvenBDD | int_to_bdd(i, xvars)

#3. Determine BDD of PRIME subset
PrimeBDD = BDDZERO
primeSet = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31} 

for i in range(32):
    if i in primeSet:
        PrimeBDD = PrimeBDD | int_to_bdd(i, xvars)

#test cases for 3.1
""" print("RR(27,3):", check_edge(R, 27, 3))    # should be True
print("RR(16,20):", check_edge(R, 16, 20))  # should be False
print("EVEN(14):", check_node(EvenBDD, 14)) # should be True
print("EVEN(13):", check_node(EvenBDD, 13)) # should be False
print("PRIME(7):", check_node(PrimeBDD, 7)) # should be True
print("PRIME(2):", check_node(PrimeBDD, 2)) # should be False """

#3.2 Compute BDD RR2, node pairs that can reach eachother in up to 2 steps
zvars = [bddvar('z', i) for i in range(5)] #need intermediate z variable for x->z z->y

#use the R BDD determined from part 3.1
RXY = R.compose({yvars[i]: zvars[i] for i in range(5)}) #replace Y connections with Z
RYZ = R.compose({xvars[i]:zvars[i] for i in range(5)}) #replace X connections with Z

combinedBDD = RXY & RYZ 
#create final BDD with x->y connections, including those with intermediary z edge
RR2 = combinedBDD.smoothing(frozenset(zvars[i] for i in range(5))) 

#test cases for 3.2
print("RR2(27, 6):", check_edge(RR2, 27, 6)) #should be true
print("RR2(27, 9):", check_edge(RR2, 27,9)) #should be false

#3.3 Compute BDD RR2*, nodes can reach within any positive steps

#use exit() to end terminal
#run with pyeda3

