import gurobipy as gp
from gurobipy import GRB
from animazione_tsp import esegui_animazione

coords = {0: (50, 80), 1: (10, 10), 2: (90, 10), 3: (30, 40), 4: (70, 40)}
nodi = list(coords.keys())
dist = {(i, j): ((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)**0.5 
        for i in nodi for j in nodi if i != j}

def subtour_elim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        selected = gp.tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
        # (Logica semplificata per trovare subtour)
        unvisited = list(nodi)
        while unvisited:
            cycle = []
            neighbors = [unvisited[0]]
            while neighbors:
                curr = neighbors.pop(); cycle.append(curr)
                unvisited.remove(curr)
                next_n = [j for i,j in selected.select(curr, '*') if j in unvisited]
                neighbors.extend(next_n)
            if len(cycle) < len(nodi):
                model.cbLazy(gp.quicksum(model._vars[i,j] for i in cycle for j in cycle if i!=j) <= len(cycle)-1)

m = gp.Model(); x = m.addVars(dist.keys(), vtype=GRB.BINARY); m._vars = x
m.setObjective(x.prod(dist)); m.addConstrs(x.sum(i,'*')==1 for i in nodi); m.addConstrs(x.sum('*',i)==1 for i in nodi)
m.Params.LazyConstraints = 1; m.optimize(subtour_elim)

# Ricostruzione tour
tour = [0]; curr = 0
for _ in range(len(nodi)):
    curr = [j for i,j in dist.keys() if i==curr and x[i,j].X > 0.5][0]
    tour.append(curr)

esegui_animazione(nodi, coords, tour, "TSP: Lazy Constraints (DFJ)")