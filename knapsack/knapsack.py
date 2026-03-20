import gurobipy as gp
from gurobipy import GRB

# Dati del problema
oggetti = ["Corona d'oro", "Spadone", "Scudo", "Elisir raro", "Tomo antico"]
profitti = [100, 120, 80, 50, 70]
pesi = [5, 8, 6, 2, 4]
capacita_massima = 15

# Inizializzazione Modello
m = gp.Model("Knapsack_Drago")

# Variabili di decisione: x[i] = 1 se prendo l'oggetto, 0 altrimenti
x = m.addVars(len(oggetti), vtype=GRB.BINARY, name="x")

# Funzione Obiettivo: Massimizzare il profitto totale
m.setObjective(gp.quicksum(profitti[i] * x[i] for i in range(len(oggetti))), GRB.MAXIMIZE)

# Vincolo: Non superare il peso massimo (W)
m.addConstr(gp.quicksum(pesi[i] * x[i] for i in range(len(oggetti))) <= capacita_massima, "Capacita")

# Ottimizzazione
m.optimize()

# Stampa dei risultati
if m.status == GRB.OPTIMAL:
    print(f"\nProfitto Totale Ottimo: {m.ObjVal} monete")
    print("Oggetti scelti:")
    for i in range(len(oggetti)):
        if x[i].X > 0.5: # Se la variabile è 1
            print(f"- {oggetti[i]} (Peso: {pesi[i]} kg)")