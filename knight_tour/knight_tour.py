import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# --- 1. Configurazione Scacchiera e Grafo ---
N = 8  # Dimensione scacchiera 8x8
CELLA_INIZIALE = (0, 0)  # Cella di partenza (riga, colonna), es. (0,0) = angolo in basso a sinistra

nodi = [(r, c) for r in range(N) for c in range(N)]

### Per ottenere soluzioni diverse, puoi modificare questa variabile (1 = prima soluzione, 2 = seconda soluzione, ecc.)
# E devi impostare NO_GOOD_CUT = True
NO_GOOD_CUT = False
NUMERO_SOLUZIONE = 1

def get_mosse_cavallo(r, c):
    """Restituisce le mosse valide del cavallo da una cella (r, c)"""
    mosse = []
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
               (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in offsets:
        if 0 <= r + dr < N and 0 <= c + dc < N:
            mosse.append((r + dr, c + dc))
    return mosse

# Costruiamo l'insieme degli archi (solo mosse a L)
archi = []
for r, c in nodi:
    for nr, nc in get_mosse_cavallo(r, c):
        archi.append(((r, c), (nr, nc)))

# --- 2. Callback per Subtour Elimination (SEC) ---
def subtour_elim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        edges = [a for a in archi if vals[a] > 0.5]
        
        # Trova il ciclo più corto
        non_visitati = list(nodi)
        ciclo_piu_corto = nodi + [nodi[0]]
        
        while non_visitati:
            ciclo_attuale = []
            vicini = [non_visitati[0]]
            while vicini:
                u = vicini.pop()
                ciclo_attuale.append(u)
                if u in non_visitati: non_visitati.remove(u)
                prossimo = [v for i, v in edges if i == u and v in non_visitati]
                vicini.extend(prossimo)
            
            if len(ciclo_attuale) < len(ciclo_piu_corto):
                ciclo_piu_corto = ciclo_attuale
        
        if len(ciclo_piu_corto) < len(nodi):
            S = ciclo_piu_corto
            model.cbLazy(gp.quicksum(model._vars[i, j] for i in S for j in S if (i, j) in archi) 
                         <= len(S) - 1)

# --- 3. Modello Gurobi ---
m = gp.Model("Knights_Tour")
m.Params.OutputFlag = 0
x = m.addVars(archi, vtype=GRB.BINARY, name="x")

# Vincoli di grado: entra e esce da ogni casella
for n in nodi:
    m.addConstr(gp.quicksum(x[i, j] for i, j in archi if i == n) == 1)
    m.addConstr(gp.quicksum(x[i, j] for i, j in archi if j == n) == 1)

m.Params.LazyConstraints = 1
m._vars = x


if NO_GOOD_CUT: 
    
    print(f"Cercando la soluzione #{NUMERO_SOLUZIONE}... (può richiedere qualche secondo)")
    for k in range(NUMERO_SOLUZIONE):
        m.optimize(subtour_elim)
        if m.status != GRB.OPTIMAL:
            print(f"Nessuna ulteriore soluzione trovata dopo {k} soluzioni.")
            break
        if k < NUMERO_SOLUZIONE - 1:
            # No-good cut: esclude la soluzione corrente e cerca la prossima
            archi_scelti = [a for a in archi if x[a].X > 0.5]
            m.addConstr(gp.quicksum(x[a] for a in archi_scelti) <= len(archi_scelti) - 1)
            print(f"  Soluzione {k+1} trovata, cerco la prossima...")

else:
    print("Cercando il percorso del cavallo... (può richiedere qualche secondo)")
    m.optimize(subtour_elim)

# --- 4. Estrazione del Percorso ---
percorso = [CELLA_INIZIALE]
curr = CELLA_INIZIALE
for _ in range(len(nodi)):
    for nr, nc in get_mosse_cavallo(curr[0], curr[1]):
        if x[curr, (nr, nc)].X > 0.5:
            curr = (nr, nc)
            percorso.append(curr)
            break

# --- 5. Animazione Matplotlib ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xticks(np.arange(-0.5, N, 1), minor=True)
ax.set_yticks(np.arange(-0.5, N, 1), minor=True)
ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

# Disegna la scacchiera base
board = np.zeros((N, N))
for r in range(N):
    for c in range(N):
        if (r + c) % 2 == 0: board[r, c] = 0.1 # Colore alternato leggero
img = ax.imshow(board, cmap='Greys', origin='lower', vmin=0, vmax=1)

# Elementi grafici del cavallo e della scia
cavallo_marker, = ax.plot([], [], 'yo', markersize=15, markeredgecolor='black', label="Cavallo")
linea_percorso, = ax.plot([], [], color='gold', linewidth=2, alpha=0.7)
testo_passi = ax.text(0, N, '', fontsize=12, fontweight='bold', va='bottom')

def update(frame):
    # Aggiorna celle visitate colorandole di rosso
    visitati_finora = percorso[:frame+1]
    temp_board = board.copy()
    for r, c in visitati_finora:
        temp_board[r, c] = 0.8 # Colore rosso (mappa Greys -> grigio scuro/nero)
    
    img.set_data(temp_board)
    
    # Muove il cavallo
    r_c, c_c = percorso[frame]
    cavallo_marker.set_data([c_c], [r_c])
    
    # Disegna la linea
    x_coords = [c for r, c in visitati_finora]
    y_coords = [r for r, c in visitati_finora]
    linea_percorso.set_data(x_coords, y_coords)
    
    testo_passi.set_text(f"Passo: {frame+1}/64")
    return img, cavallo_marker, linea_percorso, testo_passi

ani = animation.FuncAnimation(fig, update, frames=len(percorso), 
                              interval=150, blit=True, repeat=False)

plt.title("Knight's Tour: Soluzione Ottima (PLI)", fontsize=14)
plt.show()