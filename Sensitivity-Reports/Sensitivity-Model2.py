import math
from gurobipy import *
import sys
import gurobipy as gp

# Read model

model = gp.read("../Modelos/P2.lp")

# Solve model
model.optimize()

if model.status != GRB.OPTIMAL:
    print('Optimization ended with status %d' % model.status)
    sys.exit(0)

# Generate Sensitivity Report
print('\n\n--- SENSITIVITY REPORT ---\n\n')

print('Valor da Função Objetivo = {}\n'.format(model.objVal))

# Variables
print('Variables\nName\tFinal Value\tReduced cost\tObjective Coefficient\tAllowable Decrease\tAllowable Increase')
for v in model.getVars():
    print('{}\t{}\t{}\t{}\t{}\t{}'.format(v.varName, v.x, v.RC, v.Obj, v.SAObjLow, v.SAObjUp))

# Constraints
print('\nConstraints\nName\tShadow Price\tSlack\tRHS\tRHS Up\tRHS Low')
for c in model.getConstrs():
    print('{}\t{}\t{}\t{}\t{}\t{}'.format(c.ConstrName, c.Pi, c.Slack, c.RHS, c.SARHSUp, c.SARHSLow))
