import math
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


# Number of possible trips
S1 = [i for i in range(1, 19)]
S2 = [i for i in range(1, 9)]
M = 50; # Value greater than the number of needed vehicles for sure
PT = ["Wheat", "Corn","Copper","Iron"]

model = Model("IOPE")

a={} 
# Number of vehicles of type 2
for vessel in range(1, M):
    for importType in PT:
        for export in PT:
            for tripType in S1:
                a[vessel,tripType,1,importType, export]=model.addVar(vtype="I", name="a(%s,%s,%s,%s,%s)" % (vessel,tripType,1,importType, export))
            for tripType in S2:
                a[vessel,tripType,2,importType, export]=model.addVar(vtype="I", name="a(%s,%s,%s,%s,%s)" % (vessel,tripType,2,importType, export))
model.update()  # vars were added

tripNumber = {}
for vessel in range(1, M):
    tripNumber[vessel,1]=model.addVar(vtype="I", name="tripNumber(%s,1)" % (vessel))
    tripNumber[vessel,2]=model.addVar(vtype="I", name="tripNumber(%s,2)" % (vessel))
x1 = model.addVar(vtype="I", name="x1")
x2 = model.addVar(vtype="I", name="x2")

# distance traveled with the type 1 vessel in full
dFull1 = model.addVar(vtype="I", name="dFull(%s)" % (1))
# distance traveled with the type 2 vessel in full
dFull2 = model.addVar(vtype="I", name="dFull(%s)" % (2))

# distance traveled with the type 1 vessel empty
dEmpty1 = model.addVar(vtype="I", name="dEmpty(%s)" % (1))
# distance traveled with the type 2 vessel empty
dEmpty2 = model.addVar(vtype="I", name="dEmpty(%s)" % (2))

model.update()


model.addConstr(dFull1 == quicksum(a[vessel,1,1,importType, export] * d["Doce","Sky"] * 2  +    # trip: Doce – Sky – Doce
    a[vessel,2,1,importType, export] * d["Doce","Mars"] * 2   +     # trip: Doce – Mars – Doce
    a[vessel,3,1,importType, export] * (d["Doce","Sky"] + d["Mars","Doce"])  +       # trip: Doce – Sky – Mars - Doce
    a[vessel,4,1,importType, export] * (d["Doce","Mars"] + + d["Sky","Doce"]) +         # trip: Doce – Mars – Sky – Doce
    a[vessel,5,1,importType, export] * d["Bom","Sky"] * 2 +                           # trip: Bom – Sky – Bom
    a[vessel,6,1,importType, export] * d["Bom","Mars"] * 2 +                          # trip: Bom – Mars – Bom
    a[vessel,7,1,importType, export] * (d["Bom","Sky"] + d["Mars","Bom"]) +           # trip: Bom – Sky - Mars – Bom
    a[vessel,8,1,importType, export] * (d["Bom","Mars"] +  + d["Sky","Bom"]) +          # trip: Bom – Mars - Sky - Bom
    a[vessel,9,1,importType, export] * d["Doce","Moon"] * 2 +                         # trip: Doce – Moon – Doce
    a[vessel,10,1,importType, export] * (d["Doce","Sky"] + d["Moon","Doce"]) +       # trip: Doce – Sky - Moon – Doce
    a[vessel,11,1,importType, export] * (d["Doce","Moon"] + d["Mars","Doce"]) +       # trip: Doce – Moon - Mars - Doce
    a[vessel,12,1,importType, export] * (d["Doce","Moon"] + d["Sky","Doce"]) +        # trip: Doce – Moon - Sky - Doce
    a[vessel,13,1,importType, export] * (d["Doce","Mars"] + d["Moon","Doce"]) +      # trip: Doce – Mars – Moon – Doce
    a[vessel,14,1,importType, export] * d["Bom","Moon"] * 2 +                         # trip: Bom – Moon – Bom
    a[vessel,15,1,importType, export] * (d["Bom","Sky"] + d["Moon","Bom"]) +            # trip: Bom – Sky - Moon – Bom
    a[vessel,16,1,importType, export] * (d["Bom","Moon"] + d["Mars","Bom"]) +        # trip: Bom - Moon – Mars - Bom
    a[vessel,17,1,importType, export] * (d["Bom","Moon"] + d["Sky","Bom"]) +         # trip: Bom - Moon – Sky - Bom
    a[vessel,18,1,importType, export] * (d["Bom","Mars"] + d["Moon","Bom"])         # trip: Bom – Mars - Moon - Bom
for vessel in range(1, M) for importType in PT for export in PT),"c1")

model.addConstr(dFull2 == quicksum(a[vessel,1,2,importType, export] * d["Doce","Sky"] * 2  +           # trip: Doce – Sky – Doce
    a[vessel,2,2,importType, export] * d["Doce","Mars"] * 2  +                   # trip: Doce – Mars – Doce
    a[vessel,3,2,importType, export] * (d["Doce","Sky"] + d["Mars","Doce"])  +         # trip: Doce – Sky – Mars - Doce
    a[vessel,4,2,importType, export] * (d["Doce","Mars"] + + d["Sky","Doce"]) +         # trip: Doce – Mars – Sky – Doce
    a[vessel,5,2,importType, export] * d["Bom","Sky"] * 2 +                           # trip: Bom – Sky – Bom
    a[vessel,6,2,importType, export] * d["Bom","Mars"] * 2 +                          # trip: Bom – Mars – Bom
    a[vessel,7,2,importType, export] * (d["Bom","Sky"] + d["Mars","Bom"]) +           # trip: Bom – Sky - Mars – Bom
    a[vessel,8,2,importType, export] * (d["Bom","Mars"] + d["Sky","Bom"])           # trip: Bom – Mars - Sky - Bom
for vessel in range(1, M) for importType in PT for export in PT),"c2")

model.addConstr(dEmpty1 == quicksum(a[vessel,3,2,importType, export] * d["Sky","Mars"] +        # trip: Doce – Sky – Mars - Doce
    a[vessel,4,2,importType, export] * d["Mars","Sky"] +        # trip: Doce – Mars – Sky – Doce
    a[vessel,7,2,importType, export] * d["Sky","Mars"] +        # trip: Bom – Sky - Mars – Bom
    a[vessel,8,2,importType, export] * d["Mars","Sky"] +        # trip: Bom – Mars - Sky - Bom
    a[vessel,10, 1,importType, export] * d["Sky","Moon"]  +            # Doce – Sky - Moon – Doce
    a[vessel,11, 1,importType, export] * d["Moon","Mars"] +            # Doce – Moon - Mars - Doce
    a[vessel,12, 1,importType, export] * d["Moon","Sky"] +             # Doce – Moon - Sky - Doce
    a[vessel,13, 1,importType, export] * d["Mars","Moon"] +            # Doce – Mars – Moon – Doce
    a[vessel,15, 1,importType, export] * d["Sky","Moon"]  +            # Bom – Sky - Moon – Bom
    a[vessel,16, 1,importType, export] * d["Moon","Mars"] +            # Bom - Moon – Mars - Bom
    a[vessel,17, 1,importType, export] * d["Moon","Sky"] +             # Bom - Moon – Sky - Bom
    a[vessel,18, 1,importType, export] * d["Mars","Moon"]              # Bom – Mars - Moon - Bom
    for vessel in range(1, M) for importType in PT for export in PT))

model.addConstr(dEmpty2 == quicksum(a[vessel,3,2,importType, export] * d["Sky","Mars"] +        # trip: Doce – Sky – Mars - Doce
    a[vessel,4,2,importType, export] * d["Mars","Sky"] +        # trip: Doce – Mars – Sky – Doce
    a[vessel,7,2,importType, export] * d["Sky","Mars"] +        # trip: Bom – Sky - Mars – Bom
    a[vessel,8,2,importType, export] * d["Mars","Sky"]          # trip: Bom – Mars - Sky - Bom
    for vessel in range(1, M) for importType in PT for export in PT))




## Bom export of Wheat: 50 000 
# 20 000 go to Mars 
# Bom – Mars – Bom [6,1] and [6,2]; Bom – Mars - Moon - Bom [18, 1]; Bom – Mars - Sky - Bom [8, 1] and [8, 2]
model.addConstr(quicksum(a[vessel,6,1,importType,"Wheat"] + a[vessel,18,1,importType,"Wheat"] + a[vessel,8,1,importType,"Wheat"] 
    for vessel in range(1, M) for importType in PT)* 35000 + 
    quicksum(a[vessel,6,2,importType,"Wheat"] + a[vessel,8,2,importType,"Wheat"] for vessel in range(1, M) for importType in PT) * 70000 >= 20000, "c7")

# 30 000 go to Sky 
# Bom – Sky – Bom [5, 1] and [5, 2]; Bom – Sky - Moon – Bom [15, 1]; Bom – Sky - Mars – Bom [7, 1] and [7, 2]
model.addConstr(quicksum(a[vessel,5,1,importType,"Wheat"] + a[vessel,15,1,importType,"Wheat"] + a[vessel,7,1,importType,"Wheat"] for importType in PT for vessel in range(1, M))* 35000 
    + quicksum(a[vessel,5,2,importType,"Wheat"] + a[vessel,7,2,importType,"Wheat"] for importType in PT for vessel in range(1, M)) * 70000 >= 30000, "c8")


## Bom import of iron: 50 000 
model.addConstr(quicksum(a[vessel,5,1,"Iron",export] + a[vessel,17,1,"Iron",export] + a[vessel,8,1,"Iron",export] + a[vessel,6,1,"Iron",export] + a[vessel,7,1,"Iron",export] + a[vessel,16,1,"Iron",export] for vessel in range(1, M) for export in PT)* 35000 
    + quicksum(a[vessel,5,2,"Iron",export] + a[vessel,8,2,"Iron",export] + a[vessel,6,2,"Iron",export] + a[vessel,7,2,"Iron",export] for vessel in range(1, M) for export in PT) * 70000 >= 50000, "c9")


# 30 000 comes from Mars
# Bom – Mars – Bom [6,1] and [6,2]; Bom – Sky - Mars – Bom [7,1] and [7,2]; Bom - Moon – Mars - Bom [16,1]
#model.addConstr(quicksum(a[vessel,6,1] + a[vessel,7,1] + a[vessel,16,1])* 35000 + quicksum(a[vessel,6,2] + a[vessel,7,2]) * 70000 >= c[3,1], "c9")
# 40 000 comes from Sky
# Bom – Sky – Bom [5,1] and [5, 2]; Bom - Moon – Sky - Bom [17, 1]; Bom – Mars - Sky - Bom [8, 1] and [8, 2]
#model.addConstr(quicksum(a[vessel,5,1] + a[vessel,17,1] + a[vessel,8,1])* 35000 + quicksum(a[vessel,5,2] + a[vessel,8,2]) * 70000 >= 40000, "c10")

# Doce export of Corn: 40 000

# 10 000 go to Mars 
# Doce – Mars – Doce [2, 1] and [2, 2]; Doce – Mars – Moon – Doce [13, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[vessel,2,1,importType,"Corn"] + a[vessel,13,1,importType,"Corn"] + a[vessel,4,1,importType,"Corn"] for vessel in range(1, M) for importType in PT)* 35000
    + quicksum(a[vessel,2,2,importType,"Corn"] + a[vessel,4,2,importType,"Corn"] for vessel in range(1, M) for importType in PT) * 70000 >= 10000, "c10")

# 30 000 go to Moon
# Doce – Moon – Doce [9, 1]; Doce – Moon - Mars - Doce [11, 1]; Doce – Moon - Sky - Doce [12, 1]
model.addConstr(quicksum(a[vessel,9,1,importType,"Corn"] + a[vessel,11,1,importType,"Corn"] + a[vessel,12,1,importType,"Corn"] for vessel in range(1, M) for importType in PT)* 35000 <= 30000, "c11")


## Doce import of Copper: 20 000 

# 10 000 comes from Sky
# Doce – Sky – Doce [1, 1] and [1, 2]; Doce – Moon - Sky - Doce [12, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[vessel,1,1,"Copper",export] + a[vessel,12,1,"Copper",export] + a[vessel,4,1,"Copper",export] for vessel in range(1, M) for export in PT)* 35000 
    + quicksum(a[vessel,1,2,"Copper",export] + a[vessel,4,2,"Copper",export] for vessel in range(1, M) for export in PT) * 70000 >= 10000, "c12")

# 10 000 comes from Moon
# Doce – Moon – Doce [9, 1]; Doce – Sky - Moon – Doce [10, 1]; Doce – Moon - Mars - Doce [11, 1]
model.addConstr(quicksum(a[vessel,9,1,"Copper",export] + a[vessel,10,1,"Copper",export] + a[vessel,11,1,"Copper",export] for vessel in range(1, M) for export in PT)* 35000 >= 10000, "c13")


# Doce import of Iron: 20 000 
# 30 000 comes from Mars
# 40 000 comes from Sky
# Doce – Mars – Doce [2, 1] and [2, 2]; Doce – Sky – Mars - Doce [3, 1] and [3, 2]; Doce – Moon - Mars - Doce  [11, 1]
# Doce – Sky – Doce [1, 1] and [1, 2]; Doce – Moon - Sky - Doce [12, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[vessel,1,1,"Iron",export] + a[vessel,2,1,"Iron",export] + a[vessel,3,1,"Iron",export] + a[vessel,11,1,"Iron",export] + a[vessel,12,1,"Iron",export] + a[vessel,4,1,"Iron",export] for vessel in range(1, M) for export in PT)* 35000 + 
    quicksum(a[vessel,1,2,"Iron",export] + a[vessel,2,2,"Iron",export] + a[vessel,3,2,"Iron",export] + a[vessel,4,2,"Iron",export] for vessel in range(1, M)  for export in PT) * 70000 >= 20000, "c14")

# Import of Mars
# 20 000 de Wheat  - Redundant

# 10 000 of Corn 
# Doce – Mars – Doce [2, 1] and [2, 2]; Doce – Mars – Moon – Doce [13, 1]; Doce – Mars – Sky – Doce [4, 1] and [4, 2]
model.addConstr(quicksum(a[vessel,2,1,"Corn",export] + a[vessel,13,1,"Corn",export] + a[vessel,4,1,"Corn",export] for export in PT for vessel in range(1, M) )* 35000 
    + quicksum(a[vessel,2,2,"Corn",export] + a[vessel,4,2,"Corn",export] for export in PT for vessel in range(1, M) ) * 70000 >= 10000, "c15")

# Sky export Iron: 40000 
# Doce – Sky – Doce [1, 1] and [1, 2]; Doce – Moon - Sky - Doce [12, 1]; Doce – Mars – Sky – Doce  [4, 1] and [4, 2];
# Bom – Sky – Bom [5,1] and [5, 2]; Bom - Moon – Sky - Bom [17, 1]; Bom – Mars - Sky - Bom [8, 1] and [8, 2]
model.addConstr(quicksum(a[vessel,1,1,importType,"Iron"] + a[vessel,4,1,importType,"Iron"] + a[vessel,5,1,importType,"Iron"] + a[vessel,8,1,importType,"Iron"] + a[vessel,12,1,importType,"Iron"] + a[vessel,17,1,importType,"Iron"]  for vessel in range(1, M) for importType in PT)* 35000 + 
    quicksum(a[vessel,1,2,importType,"Iron"] + a[vessel,4,2,importType,"Iron"] + a[vessel,5,2,importType,"Iron"] + a[vessel,8,2,importType,"Iron"] for vessel in range(1, M)  for importType in PT) * 70000 >= 40000, "c16")


# Acabam em Sky – Wheat: 30 000
# Bom – Sky – Bom [5,1] and [5, 2]; Bom – Sky - Moon – Bom [15, 1]; Bom – Sky - Mars – Bom [7,1] and [7,2]
model.addConstr(quicksum(a[vessel,5,1,"Wheat",export] + a[vessel,15,1,"Wheat",export] + a[vessel,7,1,"Wheat",export] for export in PT for vessel in range(1, M) )* 35000 + 
        quicksum(a[vessel,5,2,"Wheat",export] + a[vessel,7,2,"Wheat",export] for export in PT for vessel in range(1, M)) * 70000 >= 30000, "c17")

# Export of Moon -  Copper: 10000
# Doce – Moon – Doce [9, 1]; Doce – Sky - Moon – Doce [10, 1]; Doce – Mars – Moon – Doce [13, 1]
model.addConstr(quicksum(a[vessel,9,1,"Copper", export] + a[vessel,10,1,"Copper", export] + a[vessel,13,1,"Copper", export] for vessel in range(1, M)  for export in PT)* 35000 >= 10000, "c18")

# Chegam a Moon – Corn: 30 000
# Doce – Moon – Doce [9, 1]; Doce – Moon - Mars - Doce [11, 1]; Doce – Moon - Sky - Doce [12, 1]
model.addConstr(quicksum(a[vessel,9,1,"Corn", export] + a[vessel,11,1,"Corn", export] + a[vessel,12,1,"Corn", export] for vessel in range(1, M) for export in PT)* 35000 >= 10000, "c19")


# for each vehicle
for vessel in range(1, M):
    model.addConstr(tripNumber[vessel,1] == quicksum(a[vessel,i,1,importType, export] for i in S1 for export in PT for importType in PT), "c20")
    model.addConstr(tripNumber[vessel,2] == quicksum(a[vessel,i,2,importType, export] for i in S2 for export in PT for importType in PT), "c21")
    #makes sure that the trips assignee last less than the operation time
    model.addConstr(quicksum( t[j,1] * a[vessel,j,1,importType,export] for j in S1 for importType in PT for export in PT) <= 345 * 24, "c5(%s,%s)" % (vessel,1))
    #the same for type 2
    model.addConstr(quicksum( t[j,2] * a[vessel,j,2,importType,export] for j in S2 for importType in PT for export in PT) <= 345 * 24, "c6(%s,%s)" % (vessel,2))

# TODO: get the number of vessels for the variable a
# for vessel in range(1, M):
    # if a[vessel,..] = 0 ==> x[1] < vessel
    # model.addConstr(quicksum(a[vessel,i,1,importType, export] for export in PT for importType in PT)  >= x[1] - vessel + 1, "c20") # change
    # if a[vessel,..] > 0 ==> x[1] >= vessel

# model.addConstr(x[1] == min_(quicksum(a[vessel,i,1,importType, export] for export in PT for importType in PT), 1))


# 0,1 * (número de veículos do tipo 1 *  1000 + número de veículos do tipo 2 *  1500) +  
# ((número de veículos do tipo 1 *  1000 + número de veículos do tipo 2 *  1500) / 25) + 
# número de veículos do tipo 1 * 70 + 
# número de veículos do tipo 2 * 75 + 
# ( distância percorrida cheio pelo veículo tipo 1/1000 * 50 + distância percorrida vazio pelo veículo tipo 1/1000 * 42)* custo de combustível + 
# ( distância percorrida cheio pelo veículo tipo 2/1000 * 40 + distância percorrida vazio pelo veículo tipo 2/1000 * 30)* custo de combustível 
model.setObjective((dFull1/1000) * 50 * 0.8 + ((dFull2/1000) * 40 + (dEmpty2/1000) * 30) * 0.8, GRB.MINIMIZE)



# model.setObjective(0.1 * (quicksum(x[i,1] for i in S1) * 1000 + quicksum(x[i,2] for i in S2) * 1500) + 
# (quicksum(x[i,1] for i in S1) * 1000 + quicksum(x[i,2] for i in S2) * 1500) / 25 +  
# (quicksum(x[i,1] for i in S1) * 70) + (quicksum(x[i,2] for i in S2) * 75), GRB.MINIMIZE)
# (dFull1/1000) * 50 * 0.8), GRB.MINIMIZE)
# Falta a distância percorrida !!

model.update()
    
model.optimize()

model.write("out.mst")
model.write("out.sol")

print("Type 1:")
for vessel in range(1, M):
    if tripNumber[vessel,1].X > 0:
        print("tripNumber[",vessel,",",1,"]",tripNumber[vessel,1].X)
    for importType in PT:
        for export in PT:
            for tripType in S1:
                if a[vessel,tripType,1,importType, export].X > 0:
                    print("a[",vessel,",",tripType,",",1,",",importType,",",export,"] = ", a[vessel,tripType,1,importType, export].X)
print("\nType 2:")
for vessel in range(1, M):
    if tripNumber[vessel,2].X > 0:
        print("tripNumber[",vessel,",",2,"]",tripNumber[vessel,2].X)
    for importType in PT:
        for export in PT:
            for tripType in S2:
                if a[vessel,tripType,2,importType, export].X > 0:
                    print("a[",vessel,",",tripType,",",2,",",importType,", ",export,"] = ", a[vessel,tripType,2,importType, export].X)