import math
from gurobipy import *
import sys
import gurobipy as gp

# Read model

model = gp.read("../Modelos/P6.lp")

# Solve model
model.optimize()

if model.status != GRB.OPTIMAL:
    print('Optimization ended with status %d' % model.status)
    sys.exit(0)


print('\n\n--- SENSITIVITY REPORT ---\n\n')

print('Valor da Função Objetivo = {}\n'.format(model.objVal))

print('Variables\nName\tFinal Value\tReduced cost\tObjective Coefficient\tCoefficient Lower Bound\tCoefficient Upper Bound')
for v in model.getVars():
    print('{}\t{}\t{}\t{}\t{}\t{}'.format(v.varName, v.x, v.RC, v.Obj, v.SAObjLow, v.SAObjUp))


print('\nConstraints\nName\tShadow Price\tSlack\tRHS\tRHS Up\tRHS Low')
for c in model.getConstrs():
    print('{}\t{}\t{}\t{}\t{}\t{}'.format(c.ConstrName, c.Pi, c.Slack, c.RHS, c.SARHSUp, c.SARHSLow))
