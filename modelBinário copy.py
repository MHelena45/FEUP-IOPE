import math;
from gurobipy import *

# distance between the ports
d={}
d={ ("Doce","Doce"):  0,  ("Doce","Bom"):math.inf,  ("Doce","Sky"):6000, ("Doce","Moon"):5000, ("Doce","Mars"):5500,
    ("Bom","Doce"):math.inf,  ("Bom","Bom"):0,  ("Bom","Sky"): 6000, ("Bom","Moon"): 5800, ("Bom","Mars"):4800,
    ("Sky","Doce"):    6000, ("Sky","Bom"): 5000, ("Sky","Sky"): 0, ("Sky","Moon"): 500 , ("Sky","Mars"): 2000,
    ("Moon","Doce"):5000, ("Moon","Bom"):500,  ("Moon","Sky"): 500, ("Moon","Moon"): 0, ("Moon","Mars"): 1000,
    ("Mars","Doce"):5500, ("Mars","Bom"):4800, ("Mars","Sky"): 2000, ("Mars","Moon"): 1000, ("Mars","Mars"): 0}

t={}
# Doce – Sky – Doce
t[1, 1] = d["Doce","Sky"]/25 * 2
t[1, 2] = d["Doce","Sky"]/20 * 2

# Doce – Mars – Doce
t[2, 1] = d["Doce","Mars"]/25 * 2
t[2, 2] = d["Doce","Mars"]/20 * 2

# Doce – Sky – Mars - Doce
t[3, 1] = d["Doce","Sky"]/25 + d["Sky","Mars"]/30 + d["Mars","Doce"]/25
t[3, 2] = d["Doce","Sky"]/20 + d["Sky","Mars"]/24 + d["Mars","Doce"]/20

# Doce – Mars – Sky – Doce
t[4, 1] = d["Doce","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Doce"]/25
t[4, 2] = d["Doce","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Doce"]/20

# Bom – Sky – Bom
t[5, 1] = d["Bom","Sky"]/25 * 2
t[5, 2] = d["Bom","Sky"]/20 * 2

# Bom – Mars – Bom
t[6, 1] = d["Bom","Mars"]/25 * 2
t[6, 2] = d["Bom","Mars"]/20 * 2

# Bom – Sky - Mars – Bom
t[7, 1] = d["Bom","Sky"]/25 + d["Sky","Mars"]/30 + d["Mars","Bom"]/25
t[7, 2] = d["Bom","Sky"]/20 + d["Sky","Mars"]/24 + d["Mars","Bom"]/20

# Bom – Mars - Sky - Bom
t[8, 1] = d["Bom","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Bom"]/25
t[8, 2] = d["Bom","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Bom"]/20

# Doce – Moon – Doce
t[9, 1] = d["Doce","Moon"]/25 * 2

# Doce – Sky - Moon – Doce
t[10, 1] = d["Doce","Sky"]/25 + d["Sky","Moon"]/30 + d["Moon","Doce"]/25

# Doce – Moon - Mars - Doce
t[11, 1] = d["Doce","Moon"]/25 + d["Moon","Mars"]/30 + d["Mars","Doce"]/25

# Doce – Moon - Sky - Doce
t[12, 1] = d["Doce","Moon"]/25 + d["Moon","Sky"]/30 + d["Sky","Doce"]/25

# Doce – Mars – Moon – Doce
t[13, 1] = d["Doce","Mars"]/25 + d["Mars","Moon"]/30 + d["Moon","Doce"]/25

# Bom – Moon – Bom
t[14, 1] = d["Bom","Moon"]/25 * 2

# Bom – Sky - Moon – Bom
t[15, 1] = d["Bom","Sky"]/25 + d["Sky","Moon"]/30 + d["Moon","Bom"]/25

# Bom - Moon – Mars - Bom
t[16, 1] = d["Bom","Moon"]/25 + d["Moon","Mars"]/30 + d["Mars","Bom"]/25

# Bom - Moon – Sky - Bom
t[17, 1] = d["Bom","Moon"]/25 + d["Moon","Sky"]/30 + d["Sky","Bom"]/25

# Bom – Mars - Moon - Bom
t[18, 1] = d["Bom","Mars"]/25 + d["Mars","Moon"]/30 + d["Moon","Bom"]/25


# Number of trips
S1 = [i for i in range(1, 19)]
S2 = [i for i in range(1, 9)]
M = 50; # Value greater than the number of needed vehicles for sure
PT = [i for i in range(1, 5)]

model = Model("IOPE")

# Number of vehicles of type 1
x={}
a={}
for i in range(1, M):
    # Binary value: 1 if the vehicle is used, 0 if the vehicle is not used
    x[i,1]=model.addVar(vtype="B", name="x(%s,%s)" % (i,1))
    for j in range(1, S1):
        # a[2,3,1] corresponds to the number trips of type 3 made by the 2º boat of type 1
        a[i,j,1]=model.addVar(vtype="I", name="a(%s,%s,%s)" % (i,j,1))
model.update()  # vars were added
    
# Number of vehicles of type 2
for i in range(1, M):
    # Binary value: 1 if the vehicle is used, 0 if the vehicle is not used
    x[i,2]=model.addVar(vtype="B", name="x(%s,%s)" % (i,2))
    for j in range(1, S2):
        # Wheat
        a[i,j,2,1]=model.addVar(vtype="I", name="a(%s,%s,%s,%s)" % (i,j,2,1))
        # Corn
        a[i,j,2,2]=model.addVar(vtype="I", name="a(%s,%s,%s,%s)" % (i,j,2,2))
        # Copper
        a[i,j,2,3]=model.addVar(vtype="I", name="a(%s,%s,%s,%s)" % (i,j,2,3))
        # Iron
        a[i,j,2,4]=model.addVar(vtype="I", name="a(%s,%s,%s,%s)" % (i,j,2,4))
model.update()  # vars were added

# carga que efetivamente chega parte ou sai
#c = {}
#for port in range(1, 6):
#    c[port,1] = model.addVar(vtype="I", name="c(%s,%s)" % (port,1))
#    c[port,2] = model.addVar(vtype="I", name="c(%s,%s)" % (port,2))

#c[3,1]

# for each vehicle
for i in range(1, M):
    # if a trip is assignee to a boot, it is used
    model.addConstr(quicksum(a[i,j,1] for j in S1) >= x[i,1], "c1(%s,%s)" % (i,1)) # if nothing is assigned, the value is 0
    model.addConstr(x[i,1] * quicksum(a[i,j,1] for j in S1) >= quicksum(a[i,j,1] for j in S1), "c2(%s,%s)" % (i,1)) # if something is assigned, the value is 1
    # ensure that a boot x can only be use if the boot x-1 has been used
    if i >=2:
        model.addConstr(x[i,1] <= x[i-1,1], "c3(%s,%s)" % (i,1))
        model.addConstr(x[i,2] <= x[i-1,2], "c4(%s,%s)" % (i,2))

# for each vehicle
for i in M:
    #makes sure that the trips assignee last less than the operation time
    model.addConstr(quicksum( t[j,1] * a[i,j,1] for j in S1) <= 345 * 24, "c5(%s,%s)" % (i,1))
    #the same for type 2
    model.addConstr(quicksum( t[j,2] * a[i,j,2] for j in S2) <= 345 * 24, "c6(%s,%s)" % (i,2))

# Bom export of Wheat: 50 000 

# 20 000 go to Mars 
# Bom – Mars – Bom [6,1] and [6,2]; Bom – Mars - Moon - Bom [18, 1]; Bom – Mars - Sky - Bom [8, 1] and [8, 2]
model.addConstr(quicksum(a[i,6,1,1] + a[i,18,1,1] + a[i,8,1,1] for i in S1)* 35000 + quicksum(a[i,6,2,1] + a[i,8,2,1] for i in S1) * 70000 >= 20000, "c7")

# 30 000 go to Sky 
# Bom – Sky – Bom [5, 1] and [5, 2]; Bom – Sky - Moon – Bom [15, 1]; Bom – Sky - Mars – Bom [7, 1] and [7, 2]
model.addConstr(quicksum(a[i,5,1,1] + a[i,15,1,1] + a[i,7,1,1] for i in S1)* 35000 + quicksum(a[i,5,2,1] + a[i,7,2,1] for i in S1) * 70000 >= 30000, "c8")


# Bom import of iron: 50 000  # TODO add constraint that does import more than 50 000
model.addConstr(quicksum(a[i,5,1,4] + a[i,17,1,4] + a[i,8,1,4] + a[i,6,1,4] + a[i,7,1,4] + a[i,16,1] for i in S1)* 35000 
+ quicksum(a[i,5,2] + a[i,8,2] + a[i,6,2] + a[i,7,2] for i in S1) * 70000 >= 50000, "c9")


# 30 000 comes from Mars
# Bom – Mars – Bom [6,1] and [6,2]; Bom – Sky - Mars – Bom [7,1] and [7,2]; Bom - Moon – Mars - Bom [16,1]
#model.addConstr(quicksum(a[i,6,1] + a[i,7,1] + a[i,16,1] for i in S1)* 35000 + quicksum(a[i,6,2] + a[i,7,2] for i in S1) * 70000 >= c[3,1], "c9")
# 40 000 comes from Sky
# Bom – Sky – Bom [5,1] and [5, 2]; Bom - Moon – Sky - Bom [17, 1]; Bom – Mars - Sky - Bom [8, 1] and [8, 2]
#model.addConstr(quicksum(a[i,5,1] + a[i,17,1] + a[i,8,1] for i in S1)* 35000 + quicksum(a[i,5,2] + a[i,8,2] for i in S1) * 70000 >= 40000, "c10")

# Doce export of Corn: 40 000

# 10 000 go to Mars 
# Doce – Mars – Doce [2, 1] and [2, 2]; Doce – Mars – Moon – Doce [13, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[i,2,1] + a[i,13,1] + a[i,4,1] for i in S1)* 35000 + quicksum(a[i,2,2] + a[i,4,2] for i in S1) * 70000 >= 10000, "c10")

# 30 000 go to Moon
# Doce – Moon – Doce [9, 1]; Doce – Moon - Mars - Doce [11, 1]; Doce – Moon - Sky - Doce [12, 1]
model.addConstr(quicksum(a[i,9,1] + a[i,11,1] + a[i,12,1] for i in S1)* 35000 <= 30000, "c11")


## Doce import of Copper: 20 000 

# 10 000 comes from Sky
# Doce – Sky – Doce [1, 1] and [1, 2]; Doce – Moon - Sky - Doce [12, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[i,1,1] + a[i,12,1] + a[i,4,1] for i in S1)* 35000 + quicksum(a[i,1,2] + a[i,4,2] for i in S1) * 70000 >= 10000, "c12")

# 10 000 comes from Moon
# Doce – Moon – Doce [9, 1]; Doce – Sky - Moon – Doce [10, 1]; Doce – Moon - Mars - Doce [11, 1]
model.addConstr(quicksum(a[i,9,1] + a[i,10,1] + a[i,11,1] for i in S1)* 35000 >= 10000, "c13")


# Doce import of Iron: 20 000 
# 30 000 comes from Mars
# 40 000 comes from Sky
# Doce – Mars – Doce [2, 1] and [2, 2]; Doce – Sky – Mars - Doce [3, 1] and [3, 2]; Doce – Moon - Mars - Doce  [11, 1]
# Doce – Sky – Doce [1, 1] and [1, 2]; Doce – Moon - Sky - Doce [12, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[i,1,1] + a[i,2,1] + a[i,3,1] + a[i,11,1] + a[i,12,1] + a[i,4,1] for i in S1)* 35000 + 
    quicksum(a[i,1,2] + a[i,2,2] + a[i,3,2] + a[i,4,2] for i in S1) * 70000 >= 20000, "c14")

# Import of Mars

# 20 000 de Wheat  - Redundant

# 10 000 of Corn 
# Doce – Mars – Doce [2, 1] and [2, 2]; Doce – Mars – Moon – Doce [13, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[i,2,1] + a[i,13,1] + a[i,4,1] for i in S1)* 35000 + quicksum(a[i,2,2] + a[i,4,2] for i in S1) * 70000 >= 10000, "c15")

# Sky export Iron: 40000 
# Doce – Sky – Doce [1, 1] and [1, 2]; Doce – Moon - Sky - Doce [12, 1]; Doce – Mars – Sky – Doce  [4, 1] and [4, 2];
# Bom – Sky – Bom [5,1] and [5, 2]; Bom - Moon – Sky - Bom [17, 1]; Bom – Mars - Sky - Bom [8, 1] and [8, 2]
model.addConstr(quicksum(a[i,1,1] + a[i,4,1] + a[i,5,1] + a[i,8,1] + a[i,12,1] + a[i,17,1] for i in S1)* 35000 + 
    quicksum(a[i,1,2] + a[i,4,2] + a[i,5,2] + a[i,8,2] for i in S1) * 70000 >= 40000, "c16")


# Acabam em Sky – Wheat: 30 000
# Bom – Sky – Bom [5,1] and [5, 2]; Bom – Sky - Moon – Bom [15, 1]; Bom – Sky - Mars – Bom [7,1] and [7,2]
model.addConstr(quicksum(a[i,5,1] + a[i,15,1] + a[i,7,1] for i in S1)* 35000 + 
    quicksum(a[i,5,2] + a[i,7,2] for i in S1) * 70000 >= 30000, "c17")

# Export of Moon -  Copper: 10000
# Doce – Moon – Doce [9, 1]; Doce – Sky - Moon – Doce [10, 1]; Doce – Mars – Moon – Doce [13, 1]
model.addConstr(quicksum(a[i,9,1] + a[i,10,1] + a[i,13,1] for i in S1)* 35000 >= 10000, "c18")

# Chegam a Moon – Corn: 30 000
# Doce – Moon – Doce [9, 1]; Doce – Moon - Mars - Doce [11, 1]; Doce – Moon - Sky - Doce [12, 1]
model.addConstr(quicksum(a[i,9,1] + a[i,11,1] + a[i,12,1] for i in S1)* 35000 >= 10000, "c19")


# 0,1 * (número de veículos do tipo 1 *  1000 + número de veículos do tipo 2 *  1500) +  
# ((número de veículos do tipo 1 *  1000 + número de veículos do tipo 2 *  1500) / 25) + 
# número de veículos do tipo 1 * 70 + 
# número de veículos do tipo 2 * 75 + 
# ( distância percorrida cheio pelo veículo tipo 1/1000 * 50 + distância percorrida vazio pelo veículo tipo 1/1000 * 42)* custo de combustível + 
# ( distância percorrida cheio pelo veículo tipo 2/1000 * 40 + distância percorrida vazio pelo veículo tipo 2/1000 * 30)* custo de combustível 



model.setObjective(quicksum(0,1 * (quicksum(x[i,1] for i in S1) * 1000 + quicksum(x[i,2] for i in S2) * 1500) + 
(quicksum(x[i,1] for i in S1) * 1000 + quicksum(x[i,2] for i in S2) * 1500) / 25 + 
(quicksum(x[i,1] for i in S1) * 70 + quicksum(x[i,2] for i in S2) * 75)), GRB.MINIMIZE)
# Falta a distância percorrida !!

model.update() 
    
model.optimize()