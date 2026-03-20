import gurobipy as gp
from gurobipy import GRB
import itertools
from animazione_tsp import esegui_animazione

coords = {0: (50, 80), 1: (10, 10), 2: (90, 10), 3: (30, 40), 4: (70, 40)}
nodi = list(coords.keys())
dist = {(i, j): ((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)**0.5 
        for i in nodi for j in nodi if i != j}

m = gp.Model(); x = m.addVars(dist.keys(), vtype=GRB.BINARY)
m.setObjective(x.prod(dist))
m.addConstrs(x.sum(i,'*')==1 for i in nodi)
m.addConstrs(x.sum('*',i)==1 for i in nodi)

# SEC Espliciti
for r in range(2, len(nodi)):
    for S in itertools.combinations(nodi, r):
        m.addConstr(gp.quicksum(x[i,j] for i in S for j in S if i!=j) <= len(S)-1)

m.optimize()
tour = [0]; curr = 0
for _ in range(len(nodi)):
    curr = [j for i,j in dist.keys() if i==curr and x[i,j].X > 0.5][0]
    tour.append(curr)

esegui_animazione(nodi, coords, tour, "TSP: SEC Espliciti (Tutti i sottoinsiemi)")