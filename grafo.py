import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

class Aresta:
    def __init__(self, destino, peso):
        self.destino = destino
        self.peso = peso

class Vertice:
    def __init__(self, nome):
        self.nome = nome
        self.arestas = []

    def adicionar_aresta(self, destino, peso):
        self.arestas.append(Aresta(destino, peso))

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.posicoes = {}

    def adicionar_vertice(self, nome):
        if nome not in self.vertices:
            self.vertices[nome] = Vertice(nome)

    def adicionar_aresta(self, origem_nome, destino_nome, peso):
        self.adicionar_vertice(origem_nome)
        self.adicionar_vertice(destino_nome)
        origem = self.vertices[origem_nome]
        destino = self.vertices[destino_nome]
        origem.adicionar_aresta(destino, peso)

    def dijkstra(self, inicio_nome):
        distancias = {nome: float('inf') for nome in self.vertices}
        anteriores = {nome: None for nome in self.vertices}
        distancias[inicio_nome] = 0
        fila = [(0, inicio_nome)]
        while fila:
            fila.sort()
            dist_atual, atual_nome = fila.pop(0)
            atual_vertice = self.vertices[atual_nome]
            for aresta in atual_vertice.arestas:
                vizinho_nome = aresta.destino.nome
                nova_dist = dist_atual + aresta.peso
                if nova_dist < distancias[vizinho_nome]:
                    distancias[vizinho_nome] = nova_dist
                    anteriores[vizinho_nome] = atual_nome
                    fila.append((nova_dist, vizinho_nome))
        return distancias, anteriores

    def caminho_para(self, anteriores, destino_nome):
        caminho = []
        atual = destino_nome
        while atual:
            caminho.insert(0, atual)
            atual = anteriores[atual]
        return caminho

class GrafoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Grafos - Dijkstra")
        self.grafo = Grafo()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.vertice_selecionado = None
        self.vertice_inicial = None
        self.vertice_destino = None
        self.distancias = {}
        self.anteriores = {}

        tk.Button(self.frame, text="Adicionar Vértice", command=self.adicionar_vertice).pack(pady=5)
        tk.Button(self.frame, text="Conectar Vértices", command=self.conectar_vertices).pack(pady=5)
        tk.Button(self.frame, text="Escolher Vértice Inicial", command=self.escolher_vertice_inicial).pack(pady=5)
        tk.Button(self.frame, text="Executar Dijkstra", command=self.executar_dijkstra).pack(pady=5)
        tk.Button(self.frame, text="Mostrar Caminho", command=self.mostrar_caminho).pack(pady=5)
        self.lista_distancias = tk.Listbox(self.frame, width=40)
        self.lista_distancias.pack(pady=5)
        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)
        self.redesenhar()

    def adicionar_vertice(self):
        nome = simpledialog.askstring("Adicionar Vértice", "Nome do vértice:")
        if not nome:
            return
        if nome in self.grafo.vertices:
            messagebox.showerror("Erro", "Vértice já existe!")
            return
        self.grafo.adicionar_vertice(nome)
        n = len(self.grafo.vertices)
        ang = 2 * 3.14159 * (n - 1) / max(n, 1)
        x = 0.5 + 0.4 * np.cos(ang)
        y = 0.5 + 0.4 * np.sin(ang)
        self.grafo.posicoes[nome] = (x, y)
        self.redesenhar()

    def conectar_vertices(self):
        if len(self.grafo.vertices) < 2:
            messagebox.showerror("Erro", "Adicione pelo menos dois vértices.")
            return
        nomes = list(self.grafo.vertices.keys())
        origem = simpledialog.askstring("Conectar", f"Vértice de origem ({', '.join(nomes)}):")
        if origem not in self.grafo.vertices:
            messagebox.showerror("Erro", "Vértice de origem inválido.")
            return
        destino = simpledialog.askstring("Conectar", f"Vértice de destino ({', '.join(nomes)}):")
        if destino not in self.grafo.vertices or destino == origem:
            messagebox.showerror("Erro", "Vértice de destino inválido.")
            return
        peso = simpledialog.askinteger("Peso", "Peso da aresta (inteiro >= 0):", minvalue=0)
        if peso is None:
            return
        self.grafo.adicionar_aresta(origem, destino, peso)
        self.redesenhar()

    def escolher_vertice_inicial(self):
        nomes = list(self.grafo.vertices.keys())
        nome = simpledialog.askstring("Vértice Inicial", f"Escolha o vértice inicial ({', '.join(nomes)}):")
        if nome not in self.grafo.vertices:
            messagebox.showerror("Erro", "Vértice inválido.")
            return
        self.vertice_inicial = nome
        self.redesenhar()

    def executar_dijkstra(self):
        if not self.vertice_inicial:
            messagebox.showerror("Erro", "Escolha o vértice inicial primeiro.")
            return
        self.distancias, self.anteriores = self.grafo.dijkstra(self.vertice_inicial)
        self.lista_distancias.delete(0, tk.END)
        for v, d in self.distancias.items():
            self.lista_distancias.insert(tk.END, f"{self.vertice_inicial} → {v}: {d if d != float('inf') else '∞'}")
        self.redesenhar()

    def mostrar_caminho(self):
        if not self.vertice_inicial:
            messagebox.showerror("Erro", "Escolha o vértice inicial primeiro.")
            return
        nomes = list(self.grafo.vertices.keys())
        destino = simpledialog.askstring("Destino", f"Escolha o vértice destino ({', '.join(nomes)}):")
        if destino not in self.grafo.vertices:
            messagebox.showerror("Erro", "Vértice inválido.")
            return
        self.vertice_destino = destino
        self.redesenhar()

    def on_canvas_click(self, event):
        if event.inaxes != self.ax:
            return
        for nome, (x, y) in self.grafo.posicoes.items():
            dx = event.xdata - x
            dy = event.ydata - y
            if dx * dx + dy * dy < 0.01:
                self.vertice_selecionado = nome
                break
        self.redesenhar()

    def redesenhar(self):
        self.ax.clear()
        for origem_nome, origem in self.grafo.vertices.items():
            x0, y0 = self.grafo.posicoes.get(origem_nome, (0, 0))
            for aresta in origem.arestas:
                destino_nome = aresta.destino.nome
                x1, y1 = self.grafo.posicoes.get(destino_nome, (0, 0))
                cor = "gray"
                largura = 1
                if self.vertice_inicial and self.vertice_destino:
                    caminho = self.grafo.caminho_para(self.anteriores, self.vertice_destino)
                    for i in range(len(caminho) - 1):
                        if caminho[i] == origem_nome and caminho[i+1] == destino_nome:
                            cor = "red"
                            largura = 3
                self.ax.annotate("",
                    xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=cor, lw=largura, shrinkA=15, shrinkB=15),
                )
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                self.ax.text(mx, my, str(aresta.peso), color="blue", fontsize=10, ha="center", va="center")
        for nome, (x, y) in self.grafo.posicoes.items():
            cor = "lightblue"
            if nome == self.vertice_inicial:
                cor = "green"
            if nome == self.vertice_destino:
                cor = "red"
            self.ax.plot(x, y, "o", markersize=20, color=cor)
            self.ax.text(x, y, nome, fontsize=12, ha="center", va="center", color="black")
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis("off")
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoApp(root)

    # Encerramento correto ao fechar a janela
    def on_closing():
        plt.close(app.fig)  # Fecha a figura do matplotlib
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
