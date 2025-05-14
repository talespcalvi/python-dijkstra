import tkinter as tk
from tkinter import simpledialog, messagebox
import math

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.posicoes = {}

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.vertices:
            self.vertices[origem] = {}
        if destino not in self.vertices:
            self.vertices[destino] = {}
        self.vertices[origem][destino] = peso

    def dijkstra(self, inicio):
        distancias = {}
        anteriores = {}
        for v in self.vertices:
            distancias[v] = float('inf')
            anteriores[v] = None
        distancias[inicio] = 0

        fila = []
        fila.append((0, inicio))

        while fila:
            fila.sort()
            distancia_atual, vertice_atual = fila.pop(0)
            for vizinho in self.vertices[vertice_atual]:
                nova_distancia = distancia_atual + self.vertices[vertice_atual][vizinho]
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = vertice_atual
                    fila.append((nova_distancia, vizinho))
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
        self.root = root
        self.caminho_destaque = []
        root.title("Grafo Direcionado com Dijkstra")

        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(pady=10)

        tk.Button(root, text="Adicionar Aresta", command=self.adicionar_aresta).pack(pady=5)
        tk.Button(root, text="Executar Dijkstra", command=self.executar_dijkstra).pack(pady=5)
        tk.Button(root, text="Limpar Grafo", command=self.limpar_grafo).pack(pady=5)

    def adicionar_aresta(self):
        origem = simpledialog.askstring("Origem", "Digite o vértice de origem:")
        destino = simpledialog.askstring("Destino", "Digite o vértice de destino:")
        try:
            peso = float(simpledialog.askstring("Peso", "Digite o peso da aresta:"))
            self.grafo.adicionar_aresta(origem, destino, peso)
            self.desenhar_grafo()
        except:
            messagebox.showerror("Erro", "Peso inválido!")

    def executar_dijkstra(self):
        inicio = simpledialog.askstring("Vértice inicial", "Digite o vértice inicial:")
        destino = simpledialog.askstring("Vértice destino", "Digite o vértice destino:")

        if inicio not in self.grafo.vertices or destino not in self.grafo.vertices:
            messagebox.showerror("Erro", "Vértice inicial ou destino não encontrado.")
            return

        distancias, anteriores = self.grafo.dijkstra(inicio)
        if distancias[destino] == float('inf'):
            messagebox.showinfo("Resultados Dijkstra", f"Sem caminho de {inicio} para {destino}")
            self.caminho_destaque.clear()
        else:
            caminho = self.grafo.mostrar_caminho(anteriores, destino)
            resultado = f"{inicio} -> {destino}: {' -> '.join(caminho)} (Custo: {distancias[destino]})"
            self.caminho_destaque = caminho
            messagebox.showinfo("Resultados Dijkstra", resultado)

        self.desenhar_grafo()

    def desenhar_grafo(self):
        self.canvas.delete("all")
        vertices = list(self.grafo.vertices.keys())
        num_vertices = len(vertices)

        # Ajuste inteligente do raio e centro baseados na tela
        largura_canvas = int(self.canvas['width'])
        altura_canvas = int(self.canvas['height'])
        margem = 50

        centro_x, centro_y = largura_canvas / 2, altura_canvas / 2
        raio_grafo = min(largura_canvas, altura_canvas) / 2 - margem

        angulo_offset = 2 * math.pi / max(num_vertices, 1)
        raio_vertice = 20

        for i, vertice in enumerate(vertices):
            angulo = i * angulo_offset
            x = centro_x + raio_grafo * math.cos(angulo)
            y = centro_y + raio_grafo * math.sin(angulo)
            self.grafo.posicoes[vertice] = (x, y)

        desenhadas = set()
        for origem, vizinhos in self.grafo.vertices.items():
            x1, y1 = self.grafo.posicoes[origem]
            for destino, peso in vizinhos.items():
                x2, y2 = self.grafo.posicoes[destino]

                if origem == destino:
                    # Auto-loop
                    self.canvas.create_oval(x1 + raio_vertice, y1 - raio_vertice,
                                            x1 + 3 * raio_vertice, y1 + raio_vertice,
                                            outline='black')
                    self.canvas.create_text(x1 + 2 * raio_vertice, y1, text=str(peso), fill='blue')
                else:
                    dx = x2 - x1
                    dy = y2 - y1
                    dist = math.hypot(dx, dy)
                    if dist == 0:
                        continue

                    offset_x = dx / dist * raio_vertice
                    offset_y = dy / dist * raio_vertice

                    start_x = x1 + offset_x
                    start_y = y1 + offset_y
                    end_x = x2 - offset_x
                    end_y = y2 - offset_y

                    deslocamento = 0
                    if (destino, origem) in desenhadas:
                        deslocamento = 10

                    perpx = -dy / dist * deslocamento
                    perpy = dx / dist * deslocamento

                    cor_linha = 'red' if self.esta_no_caminho(origem, destino) else 'black'
                    largura_linha = 4 if cor_linha == 'red' else 2

                    self.canvas.create_line(start_x + perpx, start_y + perpy,
                                            end_x + perpx, end_y + perpy,
                                            arrow=tk.LAST, width=largura_linha, fill=cor_linha)

                    mx = (start_x + end_x) / 2 + perpx
                    my = (start_y + end_y) / 2 + perpy
                    self.canvas.create_text(mx, my, text=str(peso), fill='blue', font=('Arial', 12, 'bold'))

                desenhadas.add((origem, destino))

        for vertice, (x, y) in self.grafo.posicoes.items():
            self.canvas.create_oval(x - raio_vertice, y - raio_vertice, x + raio_vertice, y + raio_vertice,
                                    fill='lightgreen', outline='black', width=2)
            self.canvas.create_text(x, y, text=vertice, font=('Arial', 12, 'bold'))

    def esta_no_caminho(self, origem, destino):
        if not self.caminho_destaque:
            return False
        for i in range(len(self.caminho_destaque) - 1):
            if self.caminho_destaque[i] == origem and self.caminho_destaque[i + 1] == destino:
                return True
        return False

    def limpar_grafo(self):
        self.grafo = Grafo()
        self.caminho_destaque.clear()
        self.canvas.delete("all")

root = tk.Tk()
app = App(root)
root.mainloop()
