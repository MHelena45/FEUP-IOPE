import math
from gurobipy import *

d={}
d={ ("Doce","Doce"):  0,  ("Doce","Bom"):math.inf,  ("Doce","Sky"):6000, ("Doce","Moon"):5000, ("Doce","Mars"):5500,
    ("Bom","Doce"):math.inf,  ("Bom","Bom"):0,  ("Bom","Sky"): 6000, ("Bom","Moon"): 5800, ("Bom","Mars"):4800,
    ("Sky","Doce"): 6000, ("Sky","Bom"): 6000, ("Sky","Sky"): 0, ("Sky","Moon"): 500 , ("Sky","Mars"): 2000,
    ("Moon","Doce"):5000, ("Moon","Bom"):5800,  ("Moon","Sky"): 500, ("Moon","Moon"): 0, ("Moon","Mars"): 1000,
    ("Mars","Doce"):5500, ("Mars","Bom"):4800, ("Mars","Sky"): 2000, ("Mars","Moon"): 1000, ("Mars","Mars"): 0}

'''
ID Route                Vessel type Product
1 Doce – Moon – Doce        1   Corn e Copper
2 Doce – Moon - Mars - Doce 1   Corn e Iron
3 Doce – Moon - Sky - Doce  1   Corn e Copper
4 Doce – Moon - Sky - Doce  1   Corn e Iron
5 Doce – Mars – Moon – Doce 1   Corn e Copper
6 Doce – Mars – Doce        1 e 2 Corn e Iron
7 Doce – Mars – Sky – Doce  1 e 2 Corn e Copper
8 Doce – Mars – Sky – Doce  1 e 2 Corn e Iron
9 Bom – Sky – Bom           1 e 2 Wheat e Iron
10 Bom – Mars – Bom         1 e 2 Wheat e Iron
11 Bom – Sky - Mars – Bom   1 e 2 Wheat e Iron
12 Bom – Mars - Sky - Bom   1 e 2 Wheat e Iron
'''

t={}

# Doce – Moon – Doce
t[1, 1] = d["Doce","Moon"]/25 * 2 # time needed to perform de trip

# Doce – Moon - Mars - Doce
t[2, 1] = d["Doce","Moon"]/25 + d["Moon","Mars"]/30 + d["Mars","Doce"]/25

# Doce – Moon - Sky - Doce
t[3, 1] = d["Doce","Moon"]/25 + d["Moon","Sky"]/30 + d["Sky","Doce"]/25
t[4, 1] = d["Doce","Moon"]/25 + d["Moon","Sky"]/30 + d["Sky","Doce"]/25

# Doce – Mars – Moon – Doce
t[5, 1] = d["Doce","Mars"]/25 + d["Mars","Moon"]/30 + d["Moon","Doce"]/25

# Doce – Mars – Doce
t[6, 1] = d["Doce","Mars"]/25 * 2
t[6, 2] = d["Doce","Mars"]/20 * 2

# Doce – Mars – Sky – Doce
t[7, 1] = d["Doce","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Doce"]/25
t[7, 2] = d["Doce","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Doce"]/20
t[8, 1] = d["Doce","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Doce"]/25
t[8, 2] = d["Doce","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Doce"]/20

# Bom – Sky – Bom
t[9, 1] = d["Bom","Sky"]/25 * 2
t[9, 2] = d["Bom","Sky"]/20 * 2

# Bom – Mars – Bom
t[10, 1] = d["Bom","Mars"]/25 * 2
t[10, 2] = d["Bom","Mars"]/20 * 2

# Bom – Sky - Mars – Bom
t[11, 1] = d["Bom","Sky"]/25 + d["Sky","Mars"]/30 + d["Mars","Bom"]/25
t[11, 2] = d["Bom","Sky"]/20 + d["Sky","Mars"]/24 + d["Mars","Bom"]/20

# Bom – Mars - Sky - Bom
t[12, 1] = d["Bom","Mars"]/25 + d["Mars","Sky"]/30 + d["Sky","Bom"]/25
t[12, 2] = d["Bom","Mars"]/20 + d["Mars","Sky"]/24 + d["Sky","Bom"]/20


type2Trips = [i for i in range(6, 13)] # the range is [6, 13[
type1Trips = [i for i in range(1, 13)] # the range is [1, 13[
M = 200; # Value greater than the number of needed vehicles for sure
model = Model("P2")

# number of ships of type 1 needed
vessel1 = model.addVar(vtype="I", name="vessel1")
# number of ships of type 2 needed
vessel2 = model.addVar(vtype="I", name="vessel2")

x = {}
a = {} # assignment of trips
for vessel in range(1, M):
    x[vessel,1] = model.addVar(vtype="B", name="x(%s,%s)"% (vessel,1))
    x[vessel,2] = model.addVar(vtype="B", name="x(%s,%s)"% (vessel,2))
    for tripType in type1Trips: 
        a[vessel,tripType,1] = model.addVar(vtype="I", name="a(%s,%s,%s)" % (vessel,tripType,1))
    for type in type2Trips: 
        a[vessel,type,2] = model.addVar(vtype="I", name="a(%s,%s,%s)" % (vessel,type,2))

# distance traveled with the type 1 vessel in Loaded
dLoaded1 = model.addVar(vtype="I", name="dLoaded(%s)" % (1))
# distance traveled with the type 2 vessel in Loaded
dLoaded2 = model.addVar(vtype="I", name="dLoaded(%s)" % (2))

# distance traveled with the type 1 vessel empty
dEmpty1 = model.addVar(vtype="I", name="dEmpty(%s)" % (1))
# distance traveled with the type 2 vessel empty
dEmpty2 = model.addVar(vtype="I", name="dEmpty(%s)" % (2))

trips = {}
# number of trips made by ship type 1 of trip 1 to 12
for tripType in type1Trips: 
    trips[tripType,1] = model.addVar(vtype="I", name="trips(%s,%s)" % (tripType,1))

# number of trips made by ship type 1 of trip 6 to 12
for type in type2Trips: 
    trips[type,2] = model.addVar(vtype="I", name="trips(%s,%s)" % (type,2))

model.update()

# Wheat
model.addConstr(quicksum(a[vessel,trip,1] for trip in range(9,13) for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,trip,2] for trip in range(9,13) for vessel in range(1, M)) * 70 >= 50000, "c1")

# Corn
model.addConstr(quicksum(a[vessel,trip,1] for trip in range(1,9) for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,trip,2] for trip in range(6,9) for vessel in range(1, M)) * 70 >= 40000, "c2")

# Iron of BOM
model.addConstr(quicksum(a[vessel,trip,1] for trip in range(9,13) for vessel in range(1, M)) * 35 
                + ( quicksum(a[vessel,trip,2] for trip in range(9,13) for vessel in range(1, M)))* 70 >= 50000, "c3")

# Copper
model.addConstr(quicksum(a[vessel,1,1] + a[vessel,3,1] + a[vessel,5,1] + a[vessel,7,1] for vessel in range(1, M)) * 35 + 
                quicksum(a[vessel,7,2] for vessel in range(1, M))* 70 >= 20000, "c4")

# Iron
model.addConstr(quicksum(a[vessel,2,1] + a[vessel,4,1] + a[vessel,6,1] + a[vessel,8,1] for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,6,2] + a[vessel,8,2] for vessel in range(1, M))* 70 >= 20000, "c5")

# Iron - Mars
model.addConstr(quicksum(a[vessel,2,1] + a[vessel,6,1] + a[vessel,10,1] + a[vessel,11,1] for vessel in range(1, M)) * 35 +
    quicksum(a[vessel,6,2] + a[vessel,10,2] + a[vessel,11,2] for vessel in range(1, M))* 70 >= 30000, "c6")

# Wheat - Mars
model.addConstr(quicksum(a[vessel,10,1] + a[vessel,12,1]for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,10,2] + a[vessel,12,2] for vessel in range(1, M))* 70 >= 20000, "c7")

# Corn - Mars
model.addConstr(quicksum(a[vessel,trip,1] for trip in range(5,9) for vessel in range(1, M)) * 35 
                + ( quicksum(a[vessel,trip,2] for trip in range(6,9) for vessel in range(1, M)))* 70 >= 10000, "c8")

# Copper - Sky
model.addConstr(quicksum(a[vessel,3,1] + a[vessel,7,1] for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,7,2] for vessel in range(1, M))* 70 >= 10000, "c9")

# Iron - Sky
model.addConstr(quicksum(a[vessel,4,1] + a[vessel,8,1] + a[vessel,9,1] + a[vessel,12,1] for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,8,2] + a[vessel,9,2] + a[vessel,12,2] for vessel in range(1, M))* 70 >= 40000, "c10")

# Wheat - Sky
model.addConstr(quicksum(a[vessel,9,1] + a[vessel,11,1] for vessel in range(1, M)) * 35 + 
    quicksum(a[vessel,9,2] + a[vessel,11,2] for vessel in range(1, M))* 70 >= 30000, "c11")

# Copper - Moon
model.addConstr(quicksum(a[vessel,1,1] + a[vessel,5,1] for vessel in range(1, M)) * 35 >= 10000, "c12")

# Corn - Moon
model.addConstr(quicksum(a[vessel,trip,1] for trip in range(1,5) for vessel in range(1, M)) * 35 >= 30000, "c13")

# for each vehicle
for vessel in range(1, M):
    #makes sure that the trips assignee last less than the operation time
    model.addConstr(quicksum(t[tripType,1] * a[vessel,tripType,1] for tripType in type1Trips) <= 345 * 24, "c14")
    model.addConstr(quicksum(t[tripType,2] * a[vessel,tripType,2] for tripType in type2Trips) <= 345 * 24, "c15")

# for each vehicle
for vessel in range(1, M):
    # if a trip is assignee to a boot, it is used
    model.addConstr(quicksum(a[vessel,tripType,1] for tripType in type1Trips) 
        >= x[vessel,1], "c20(%s,%s)" % (vessel,1)) # if nothing is assigned, the value is 0
    model.addConstr(x[vessel,1] * quicksum(a[vessel,tripType,1] for tripType in type1Trips) 
        >= quicksum(a[vessel,tripType,1] for tripType in type1Trips), "c21(%s,%s)" % (vessel,1)) # if something is assigned, the value is 1
    
    model.addConstr(quicksum(a[vessel,tripType,2]  for tripType in type2Trips) 
        >= x[vessel,2], "c22(%s,%s)" % (vessel,2)) # if nothing is assigned, the value is 0
    model.addConstr(x[vessel,2] * quicksum(a[vessel,tripType,2]  for tripType in type2Trips) 
        >= quicksum(a[vessel,tripType,2]  for tripType in type2Trips), "c23(%s,%s)" % (vessel,2)) # if something is assigned, the value is 1
    # ensure that a boot x can only be use if the boot x-1 has been used
    if vessel >=2:
        model.addConstr(x[vessel,1] <= x[vessel-1,1], "c24(%s,%s)" % (vessel,1))
        model.addConstr(x[vessel,2] <= x[vessel-1,2], "c25(%s,%s)" % (vessel,2))



model.addConstr(dLoaded1 == quicksum(a[vessel,1, 1] * d["Doce","Moon"] * 2    +               # Doce – Moon – Doce
a[vessel,2, 1] * (d["Doce","Moon"] + d["Mars","Doce"]) +                           # Doce – Moon - Mars - Doce
(a[vessel,4, 1] + a[vessel,3, 1]) * (d["Doce","Moon"] + d["Sky","Doce"]) +            # Doce – Moon - Sky - Doce
a[vessel,4, 1] * (d["Doce","Moon"] +  d["Sky","Doce"]) +                           # Doce – Moon - Sky - Doce
a[vessel,5, 1] * (d["Doce","Mars"]  + d["Moon","Doce"]) +                          # Doce – Mars – Moon – Doce
a[vessel,6, 1] * d["Doce","Mars"] * 2 +                                            # Doce – Mars – Doce
(a[vessel,7, 1] + a[vessel,8, 1]) * (d["Doce","Mars"] + d["Sky","Doce"]) +            # Doce – Mars – Sky – Doce
a[vessel,9, 1] * d["Bom","Sky"] * 2 +                                              # Bom – Sky – Bom
a[vessel,10, 1] * d["Bom","Mars"] * 2  +                                           # Bom – Mars – Bom
a[vessel,11, 1] * (d["Bom","Sky"] + d["Mars","Bom"]) +                             # Bom – Sky - Mars – Bom
a[vessel,12, 1] * (d["Bom","Mars"]  + d["Sky","Bom"]) for vessel in range(1, M)),"c16")                       # Bom – Mars - Sky - Bom

model.addConstr(dLoaded2 == quicksum(a[vessel,6, 2] * d["Doce","Mars"] * 2 +                  # Doce – Mars – Doce
(a[vessel,7, 2] + a[vessel,8, 2]) * (d["Doce","Mars"] + d["Sky","Doce"]) +            # Doce – Mars – Sky – Doce
a[vessel,9, 2] * d["Bom","Sky"] * 2 +                                              # Bom – Sky – Bom
a[vessel,10, 2] * d["Bom","Mars"] * 2 +                                            # Bom – Mars – Bom
a[vessel,11, 2] * (d["Bom","Sky"] + d["Mars","Bom"]) +                             # Bom – Sky - Mars – Bom
a[vessel,12, 2] * (d["Bom","Mars"] + d["Sky","Bom"]) for vessel in range(1, M)),"c17")                        # Bom – Mars - Sky - Bom

model.addConstr(dEmpty1 == quicksum(a[vessel,2, 1] *  d["Moon","Mars"] +                    # Doce – Moon - Mars - Doce
(a[vessel,3, 1] + a[vessel,4, 1]) *  d["Moon","Sky"] +                                # Doce – Moon - Sky - Doce
a[vessel,5, 1] * d["Mars","Moon"] +                                                # Doce – Mars – Moon – Doce
(a[vessel,7, 1] + a[vessel,8, 1]) *  d["Mars","Sky"] +                                # Doce – Mars – Sky – Doce
a[vessel,11, 1] * d["Sky","Mars"] +                                                # Bom – Sky - Mars – Bom
a[vessel,12, 1] * d["Mars","Sky"] for vessel in range(1, M)), "c18")                                          # Bom – Mars - Sky - Bom

model.addConstr(dEmpty2 == quicksum((a[vessel,7, 2] + a[vessel,8, 2] + a[vessel,12, 2]) * d["Mars","Sky"] +      # Doce – Mars – Sky – Doce && Bom – Mars - Sky - Bom
a[vessel,11, 2] * d["Sky","Mars"] for vessel in range(1, M)), "c19") # Bom – Mars - Sky - Bom

model.addConstr(vessel1 == quicksum(x[vessel,1] for vessel in range(1, M)), "c20")
model.addConstr(vessel2 == quicksum(x[vessel,2] for vessel in range(1, M)), "c21")

for tripType in type1Trips:
    model.addConstr(trips[tripType,1] == quicksum(a[vessel,tripType, 1] for vessel in range(1, M)), "c22")
for tripType in type2Trips:
    model.addConstr(trips[tripType,2] == quicksum(a[vessel,tripType, 2] for vessel in range(1, M)), "c23")

# 0,1 * (número de veículos do tipo 1 *  1 000 000 + número de veículos do tipo 2 *  1 500  000) +  
# ((número de veículos do tipo 1 *  1 000 000 + número de veículos do tipo 2 *  1500 000) / 25) + 
# número de veículos do tipo 1 * 70 000 + 
# número de veículos do tipo 2 * 75 000 + 
# ( distância percorrida cheio pelo veículo tipo 1/1000 * 50 + distância percorrida vazio pelo veículo tipo 1/1000 * 42)* custo de combustível + 
# ( distância percorrida cheio pelo veículo tipo 2/1000 * 40 + distância percorrida vazio pelo veículo tipo 2/1000 * 30)* custo de combustível 

model.setObjective(0.1 * (vessel1 * 1000000 + vessel2 * 1500000) +  (vessel1 * 1000000 + vessel2 * 1500000) / 25 +  vessel1 * 70000 + vessel2 * 75000 + 
 ((dLoaded1/1000) * 50 + (dEmpty1/1000) * 42 + (dLoaded2/1000) * 40 + (dEmpty2/1000) * 30) * 0.8, GRB.MINIMIZE)

model.update()
    
model.optimize()

# generates the file with the solution
model.write("../Resultados/Solution-P2-Exact.sol")
# generates the file with the constraints
model.write("../Resultados/constraints-P2-Exact.lp")