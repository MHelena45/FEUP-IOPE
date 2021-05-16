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
model = Model("P4")

# number of ships of type 1 needed
vessel1 = model.addVar(vtype="C", name="vessel1")
# number of ships of type 2 needed
vessel2 = model.addVar(vtype="C", name="vessel2")

trips = {}
# number of trips made by ship type 1 of trip 1 to 12
for tripType in type1Trips: 
    trips[tripType,1] = model.addVar(vtype="C", name="trips(%s,%s)" % (tripType,1))

# number of trips made by ship type 1 of trip 6 to 12
for tripType in type2Trips: 
    trips[tripType,2] = model.addVar(vtype="C", name="trips(%s,%s)" % (tripType,2))

# distance traveled with the type 1 vessel in Loaded
dLoaded1 = model.addVar(vtype="C", name="dLoaded(%s)" % (1))
# distance traveled with the type 2 vessel in Loaded
dLoaded2 = model.addVar(vtype="C", name="dLoaded(%s)" % (2))

# distance traveled with the type 1 vessel empty
dEmpty1 = model.addVar(vtype="C", name="dEmpty(%s)" % (1))
# distance traveled with the type 2 vessel empty
dEmpty2 = model.addVar(vtype="C", name="dEmpty(%s)" % (2))

model.update()

# Wheat
model.addConstr(quicksum(trips[trip,1] for trip in range(9,13)) * 35 + quicksum(trips[trip,2] for trip in range(9,13)) * 70 >= 50000, "c1")

# Corn
model.addConstr(quicksum(trips[trip,1] for trip in range(1,9)) * 35 + quicksum(trips[trip,2] for trip in range(6,9)) * 70 >= 40000, "c2")

# Iron of BOM
model.addConstr(quicksum(trips[trip,1] for trip in range(9,13)) * 35 
                + ( quicksum(trips[trip,2] for trip in range(9,13)))* 70 >= 50000, "c3")

# Copper arriving in Doce
model.addConstr((trips[1,1] + trips[3,1] + trips[5,1] + trips[7,1]) * 35 + (trips[7,2] )* 70 >= 20000, "c4")

# Iron arriving in Doce
model.addConstr((trips[2,1] + trips[4,1] + trips[6,1] + trips[8,1]) * 35 + (trips[6,2] + trips[8,2])* 70 >= 20000, "c5")

# export Iron - Mars
model.addConstr((trips[2,1] + trips[6,1] + trips[10,1] + trips[11,1]) * 35 + (trips[6,2] + trips[10,2] + trips[11,2])* 70 >= 30000, "c6")

# import Wheat - Mars
model.addConstr((trips[10,1] + trips[12,1]) * 35 + (trips[10,2] + trips[12,2])* 70 >= 20000, "c7")

# import Corn - Mars
model.addConstr(quicksum(trips[trip,1] for trip in range(5,9)) * 35 
                + ( quicksum(trips[trip,2] for trip in range(6,9)))* 70 >= 10000, "c8")

# export Copper - Sky
model.addConstr((trips[3,1] + trips[7,1]) * 35 + trips[7,2]* 70 >= 10000, "c9")

# export Iron - Sky
model.addConstr((trips[4,1] + trips[8,1] + trips[9,1] + trips[12,1]) * 35 + (trips[8,2] + trips[9,2] + trips[12,2])* 70 >= 40000, "c10")

# import Wheat - Sky
model.addConstr((trips[9,1] + trips[11,1]) * 35 + (trips[9,2] + trips[11,2])* 70 >= 30000, "c11")

# export Copper - Moon
model.addConstr((trips[1,1] + trips[5,1]) * 35 >= 10000, "c12")

# import Corn - Moon
model.addConstr(quicksum(trips[trip,1] for trip in range(1,5)) * 35 >= 30000, "c13")


model.addConstr(quicksum(t[tripType,1] * trips[tripType,1] for tripType in type1Trips) <= vessel1 * 345 * 24, "c14")
model.addConstr(quicksum(t[tripType,2] * trips[tripType,2] for tripType in type2Trips) <= vessel2 * 345 * 24, "c15")

model.addConstr(dLoaded1 == trips[1, 1] * d["Doce","Moon"] * 2    +               # Doce – Moon – Doce
trips[2, 1] * (d["Doce","Moon"] + d["Mars","Doce"]) +                           # Doce – Moon - Mars - Doce
(trips[4, 1] + trips[3, 1]) * (d["Doce","Moon"] + d["Sky","Doce"]) +            # Doce – Moon - Sky - Doce
trips[4, 1] * (d["Doce","Moon"] +  d["Sky","Doce"]) +                           # Doce – Moon - Sky - Doce
trips[5, 1] * (d["Doce","Mars"]  + d["Moon","Doce"]) +                          # Doce – Mars – Moon – Doce
trips[6, 1] * d["Doce","Mars"] * 2 +                                            # Doce – Mars – Doce
(trips[7, 1] + trips[8, 1]) * (d["Doce","Mars"] + d["Sky","Doce"]) +            # Doce – Mars – Sky – Doce
trips[9, 1] * d["Bom","Sky"] * 2 +                                              # Bom – Sky – Bom
trips[10, 1] * d["Bom","Mars"] * 2  +                                           # Bom – Mars – Bom
trips[11, 1] * (d["Bom","Sky"] + d["Mars","Bom"]) +                             # Bom – Sky - Mars – Bom
trips[12, 1] * (d["Bom","Mars"]  + d["Sky","Bom"]),"c16")                       # Bom – Mars - Sky - Bom

model.addConstr(dLoaded2 == trips[6, 2] * d["Doce","Mars"] * 2 +                  # Doce – Mars – Doce
(trips[7, 2] + trips[8, 2]) * (d["Doce","Mars"] + d["Sky","Doce"]) +            # Doce – Mars – Sky – Doce
trips[9, 2] * d["Bom","Sky"] * 2 +                                              # Bom – Sky – Bom
trips[10, 2] * d["Bom","Mars"] * 2 +                                            # Bom – Mars – Bom
trips[11, 2] * (d["Bom","Sky"] + d["Mars","Bom"]) +                             # Bom – Sky - Mars – Bom
trips[12, 2] * (d["Bom","Mars"] + d["Sky","Bom"]),"c17")                        # Bom – Mars - Sky - Bom

model.addConstr(dEmpty1 == trips[2, 1] *  d["Moon","Mars"] +                    # Doce – Moon - Mars - Doce
(trips[3, 1] + trips[4, 1]) *  d["Moon","Sky"] +                                # Doce – Moon - Sky - Doce
trips[5, 1] * d["Mars","Moon"] +                                                # Doce – Mars – Moon – Doce
(trips[7, 1] + trips[8, 1]) *  d["Mars","Sky"] +                                # Doce – Mars – Sky – Doce
trips[11, 1] * d["Sky","Mars"] +                                                # Bom – Sky - Mars – Bom
trips[12, 1] * d["Mars","Sky"], "c18")                                          # Bom – Mars - Sky - Bom

model.addConstr(dEmpty2 == (trips[7, 2] + trips[8, 2] + trips[12, 2]) * d["Mars","Sky"] +      # Doce – Mars – Sky – Doce && Bom – Mars - Sky - Bom
trips[11, 2] * d["Sky","Mars"], "c19") # Bom – Mars - Sky - Bom

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

model.write("Solution-P4.sol")
model.write("constraints-P4.lp")

print(model.SolCount) # returns 8

print('Z = {}'.format(model.objVal))
for v in model.getVars():
    print('{} = {}\tReduced cost {} \tSAObjLow {} \tSAObjUp {} '.format(v.varName, v.x, v.RC, v.SAObjLow, v.SAObjUp))

print('\nSensitivity Analysis\nConstraint\tShadow Price\tSlack')
for c in model.getConstrs():
    print('{}: \t\t{}\t\t{}'.format(c.ConstrName, c.Pi, c.Slack))