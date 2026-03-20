import matplotlib.pyplot as plt
import matplotlib.animation as animation

def esegui_animazione(nodi, coords, percorso, titolo):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(titolo)
    ax.axis('off')

    # Disegna tutti gli archi del grafo completo in grigio chiaro
    for i in nodi:
        for j in nodi:
            if i < j:
                xi, yi = coords[i]
                xj, yj = coords[j]
                ax.plot([xi, xj], [yi, yj], color='lightgray', linewidth=0.8, zorder=0)

    # Disegna i nodi
    for i, (x_c, y_c) in coords.items():
        color = 'red' if i == 0 else 'blue'
        ax.scatter(x_c, y_c, s=300, color=color, zorder=2)
        ax.text(x_c, y_c, str(i), color='white', ha='center', va='center', fontweight='bold')

    line, = ax.plot([], [], color='red', linewidth=2, zorder=1)

    def update(frame):
        sub_tour = percorso[:frame+1]
        x_tour = [coords[nodo][0] for nodo in sub_tour]
        y_tour = [coords[nodo][1] for nodo in sub_tour]
        line.set_data(x_tour, y_tour)
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(percorso), interval=500, repeat=False)
    plt.show()