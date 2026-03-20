import gurobipy as gp
from gurobipy import GRB

# --- DATI ---
W = 100  # Larghezza rotolo grande
ordini = [20, 45, 35]  # Larghezze richieste
domanda = [15, 20, 25]  # Quanti pezzi per ogni larghezza
n = len(ordini)

# 1. GENERAZIONE INITIAL PATTERNS (Casi base: un pezzo per rotolo)
# Ogni colonna è un pattern di taglio
patterns = []
for i in range(n):
    p = [0] * n
    p[i] = int(W / ordini[i])
    patterns.append(p)

# --- LOOP DI COLUMN GENERATION ---
while True:
    # 2. RISOLVIAMO IL MASTER PROBLEM (Rilassato)
    master = gp.Model("Master")
    master.Params.OutputFlag = 0
    
    # Variabili: quante volte uso il pattern j
    x = master.addVars(len(patterns), obj=1.0, vtype=GRB.CONTINUOUS, name="x")
    
    # Vincoli di domanda: la somma dei pezzi prodotti deve coprire la domanda
    constrs = master.addConstrs(
        (gp.quicksum(patterns[j][i] * x[j] for j in range(len(patterns))) >= domanda[i]
         for i in range(n)), name="Demand"
    )
    
    master.optimize()
    
    # 3. PRENDIAMO I VALORI DUALI (Prezzi Ombra)
    # Ci dicono quanto "pagheremmo" per un pezzo in più di quella misura
    duali = [constrs[i].Pi for i in range(n)]
    
    # 4. RISOLVIAMO IL SUB-PROBLEM (Knapsack)
    # Vogliamo massimizzare il valore dei pezzi che mettiamo nel rotolo
    # Valore di ogni pezzo = il suo valore duale
    sub = gp.Model("Sub")
    sub.Params.OutputFlag = 0
    y = sub.addVars(n, vtype=GRB.INTEGER, name="y")
    
    sub.setObjective(gp.quicksum(duali[i] * y[i] for i in range(n)), GRB.MAXIMIZE)
    sub.addConstr(gp.quicksum(ordini[i] * y[i] for i in range(n)) <= W)
    
    sub.optimize()
    
    # 5. CONTROLLO REDUCED COST
    # Se il valore trovato è > 1, il nuovo pattern è conveniente!
    if sub.ObjVal > 1.0001:
        nuovo_pattern = [int(y[i].X) for i in range(n)]
        patterns.append(nuovo_pattern)
        print(f"Trovato nuovo pattern: {nuovo_pattern} (Reduced cost: {sub.ObjVal - 1:.4f})")
    else:
        break # Non ci sono più pattern migliorativi

# --- RISULTATO FINALE (INTERO) ---
# Risolviamo il Master finale come intero (MIP) con le colonne trovate
for v in master.getVars():
    v.vtype = GRB.INTEGER
master.optimize()

print(f"\nRotoli totali necessari: {int(master.ObjVal)}")
for j in range(len(patterns)):
    if x[j].X > 0.1:
        print(f"Usa il pattern {patterns[j]} per {int(x[j].X)} volte")