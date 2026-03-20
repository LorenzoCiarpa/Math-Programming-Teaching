import gurobipy as gp
from gurobipy import GRB
from animazione_tsp import esegui_animazione

coords = {0: (50, 80), 1: (10, 10), 2: (90, 10), 3: (30, 40), 4: (70, 40)}
nodi = list(coords.keys()); n = len(nodi)
dist = {(i, j): ((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)**0.5 
        for i in nodi for j in nodi if i != j}

m = gp.Model(); x = m.addVars(dist.keys(), vtype=GRB.BINARY)
u = m.addVars(nodi[1:], lb=1, ub=n-1, vtype=GRB.CONTINUOUS) # Variabili ordine

m.setObjective(x.prod(dist))
m.addConstrs(x.sum(i,'*')==1 for i in nodi); m.addConstrs(x.sum('*',i)==1 for i in nodi)

# Vincoli MTZ
for i in nodi[1:]:
    for j in nodi[1:]:
        if i != j:
            m.addConstr(u[i] - u[j] + n*x[i,j] <= n-1)

m.optimize()
tour = [0]; curr = 0
for _ in range(len(nodi)):
    curr = [j for i,j in dist.keys() if i==curr and x[i,j].X > 0.5][0]
    tour.append(curr)

esegui_animazione(nodi, coords, tour, "TSP: Formulazione MTZ")