import gurobipy as gp
from gurobipy import GRB

# Dati del problema
pesi = [40, 50, 30, 20, 60, 45, 55]
W = 100
n = len(pesi)
furgoni_max = n # Limite superiore (peggior caso: un pacco per furgone)

# Inizializzazione Modello
m = gp.Model("Bin_Packing_Logistica")

# Variabili di decisione
# y[j] = 1 se il furgone j è utilizzato
y = m.addVars(furgoni_max, vtype=GRB.BINARY, name="y")

# x[i, j] = 1 se il pacco i è messo nel furgone j
x = m.addVars(n, furgoni_max, vtype=GRB.BINARY, name="x")

# Funzione Obiettivo: Minimizzare i furgoni usati
m.setObjective(y.sum(), GRB.MINIMIZE)

# 1. Ogni pacco deve essere assegnato a ESATTAMENTE un furgone
for i in range(n):
    m.addConstr(gp.quicksum(x[i, j] for j in range(furgoni_max)) == 1)

# 2. Vincolo di capacità e attivazione furgone
for j in range(furgoni_max):
    m.addConstr(gp.quicksum(pesi[i] * x[i, j] for i in range(n)) <= W * y[j])

# Ottimizzazione
m.optimize()

# Stampa dei risultati
if m.status == GRB.OPTIMAL:
    print(f"\nNumero minimo di furgoni: {int(m.ObjVal)}")
    for j in range(furgoni_max):
        if y[j].X > 0.5:
            pacci_in_furgone = [pesi[i] for i in range(n) if x[i, j].X > 0.5]
            print(f"Furgone {j+1}: Contiene pacchi {pacci_in_furgone} (Totale: {sum(pacci_in_furgone)})")