# Math-Programming-Teaching

Una raccolta di esempi didattici di **Ricerca Operativa** e **Programmazione Matematica**, pensata per accompagnare lezioni e laboratori. Ogni esempio affronta un problema classico con un modello ILP (o LP) risolto tramite [Gurobi](https://www.gurobi.com/).

---

## Struttura della repo

| Cartella | Problema | Tipo | Output |
|---|---|---|---|
| `knapsack/` | Problema dello zaino | ILP binario | Testo |
| `bin_packing/` | Bin Packing | ILP binario | Testo |
| `cutting_stock/` | Cutting Stock | LP + Column Generation | Testo |
| `tsp/` | Travelling Salesman Problem | ILP + Lazy Constraints (DFJ) | Animazione |
| `knight_tour/` | Giro del Cavallo | ILP + Lazy Constraints (SEC) | Animazione |
| `queens/` | Problema delle N Regine | ILP | Notebook |
| `sudoku/` | Sudoku | ILP | Notebook |
| `chessboard-domino/` | Copertura con domino | ILP | Notebook |
| `color_graph/` | Colorazione di grafi | ILP | Notebook |

---

## Esempi

### Knapsack — `knapsack/knapsack.py`
Il classico problema dello zaino binario: dato un insieme di oggetti con profitto e peso, scegliere quali portare senza superare la capacità massima. Modello ILP diretto con Gurobi.

### Bin Packing — `bin_packing/bin_packing.py`
Distribuzione di pacchi su furgoni minimizzando il numero di veicoli usati. Mostra la formulazione con variabili di attivazione `y[j]` e variabili di assegnazione `x[i,j]`.

### Cutting Stock — `cutting_stock/cutting_stock.py`
Taglio di rotoli di larghezza fissa per soddisfare ordini di misure diverse. Implementa la tecnica di **Column Generation**: il Master Problem rilassato viene risolto iterativamente aggiungendo nuovi pattern di taglio generati da un sub-problem knapsack, fino a convergenza.

### TSP — `tsp/`
Travelling Salesman Problem con tre implementazioni didattiche per affrontare il problema della eliminazione dei subtour:

- **`tsp_lazy.py`**: DFJ (Dantzig-Fleischmann-Johnson) via **Lazy Constraints** nella callback di Gurobi
- **`tsp_dfj.py`**: DFJ con vincoli espliciti aggiunti *a priori* (non lazy)
- **`tsp_mtz.py`**: Formulazione **Miller-Tucker-Zemlin**, che evita i subtour con variabili di posizione ausiliarie

Il tour ottimo viene mostrato con un'animazione passo-passo su grafo completo con tutti gli archi visibili.

### Giro del Cavallo — `knight_tour/knight_tour.py`
Il percorso hamiltoniano del cavallo su una scacchiera 8×8 formulato come ILP su grafo. Usa anch'esso Lazy Constraints per eliminare i sottocicli (SEC). Il percorso viene animato sulla scacchiera.

### N Regine — `queens/queens_game.ipynb`
Posizionamento di N regine su una scacchiera N×N senza che si minaccino. Classico esempio di problema di soddisfacimento di vincoli (CSP) visto come ILP.

### Sudoku — `sudoku/sudoku.ipynb`
Risoluzione di un puzzle Sudoku modellato come ILP: variabili binarie `x[i,j,k]` per indicare la presenza del valore `k` nella cella `(i,j)`.

### Copertura con Domino — `chessboard-domino/`
Copertura di una scacchiera (eventualmente con celle rimosse) tramite tessere domino. Include il file `.lp` del modello e un'analisi di infeasibility (IIS).

### Colorazione di Grafi — `color_graph/`
Assegnazione del minimo numero di colori ai nodi di un grafo tale che nodi adiacenti abbiano colori diversi, modellato come ILP.

---

## Requisiti

```bash
pip install -r requirements.txt
```

> **Nota:** Gurobi richiede una licenza valida. Per uso accademico è disponibile una [licenza accademica gratuita](https://www.gurobi.com/academia/academic-program-and-licenses/).
Per problemi con una dimensione ridotta non è necessario installare una licenza.

---

## Come eseguire

Script Python:
```bash
python knapsack/knapsack.py
python tsp/tsp_lazy.py
```