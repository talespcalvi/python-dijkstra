import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import heapq

class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.vertices:
            self.vertices[origem] = {}
        if destino not in self.vertices:
            self.vertices[destino] = {}
        self.vertices[origem][destino] = peso


    def dijkstra(self, inicio):
        distancias = {vertice: float('infinity') for vertice in self.vertices}
        distancias[inicio] = 0
        anteriores = {vertice: None for vertice in self.vertices}
        fila = [(0, inicio)]

        while fila:
            distancia_atual, vertice_atual = heapq.heappop(fila)

            if distancia_atual > distancias[vertice_atual]:
                continue

            for vizinho, peso in self.vertices[vertice_atual].items():
                distancia = distancia_atual + peso
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    anteriores[vizinho] = vertice_atual
                    heapq.heappush(fila, (distancia, vizinho))

        return distancias, anteriores

    def mostrar_caminho(self, anteriores, destino):
        caminho = []
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            atual = anteriores[atual]
        return caminho

class App:
    def __init__(self, root):
        self.grafo = Grafo()

        root.title("Algoritmo de Dijkstra - Interface Gráfica")

        self.text_output = scrolledtext.ScrolledText(root, width=60, height=20)
        self.text_output.pack(pady=10)

        tk.Button(root, text="Adicionar Aresta", command=self.adicionar_aresta).pack(pady=5)
        tk.Button(root, text="Executar Dijkstra", command=self.executar_dijkstra).pack(pady=5)
        tk.Button(root, text="Sair", command=root.quit).pack(pady=5)

    def adicionar_aresta(self):
        origem = simpledialog.askstring("Origem", "Digite o vértice de origem:")
        destino = simpledialog.askstring("Destino", "Digite o vértice de destino:")
        try:
            peso = float(simpledialog.askstring("Peso", "Digite o peso da aresta:"))
            self.grafo.adicionar_aresta(origem, destino, peso)
            self.text_output.insert(tk.END, f"Aresta adicionada: {origem} -> {destino} (Peso: {peso})\n")
        except:
            messagebox.showerror("Erro", "Peso inválido!")

    def executar_dijkstra(self):
        inicio = simpledialog.askstring("Vértice inicial", "Digite o vértice inicial:")
        if inicio not in self.grafo.vertices:
            messagebox.showerror("Erro", "Vértice inicial não encontrado no grafo.")
            return

        distancias, anteriores = self.grafo.dijkstra(inicio)
        self.text_output.insert(tk.END, f"\nResultados do Dijkstra a partir de {inicio}:\n")
        for destino in self.grafo.vertices:
            if distancias[destino] == float('infinity'):
                self.text_output.insert(tk.END, f"Sem caminho de {inicio} para {destino}\n")
            else:
                caminho = self.grafo.mostrar_caminho(anteriores, destino)
                self.text_output.insert(tk.END, f"Menor caminho para {destino}: {' -> '.join(caminho)} (Custo: {distancias[destino]})\n")
        self.text_output.insert(tk.END, "-"*50 + "\n")

# ========= Execução =========
root = tk.Tk()
app = App(root)
root.mainloop()
