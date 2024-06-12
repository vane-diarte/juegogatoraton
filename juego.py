import tkinter as tk
from tkinter import messagebox
import random

class JuegoGatoRaton: 
    def __init__(self, raiz, tamaño=8): 
        self.tamaño = tamaño
        self.raiz = raiz 
        self.tablero = [[0] * tamaño for _ in range(tamaño)] 
        self.gato_pos = (0, 0) 
        self.raton_pos = (tamaño - 1, tamaño - 1) 
        self.pos_inicial_gato = self.gato_pos 
        self.obstaculos = self.generar_obstaculos()
        self.turno_raton = True
        self.canvas = tk.Canvas(raiz, width=400, height=400)
        self.canvas.pack()
        self.historial = HistorialMovimientos()
        self.historial.agregar_movimiento(self.gato_pos, self.raton_pos)
        self.dibujar_tablero()
        self.canvas.bind("<Button-1>", self.seleccionar_celda)

         

    def generar_obstaculos(self):
        obstaculos = set()
        while len(obstaculos) < (self.tamaño * self.tamaño) // 5:  
            x = random.randint(0, self.tamaño - 1)
            y = random.randint(0, self.tamaño - 1)

            
            if (x, y) != self.gato_pos and (x, y) != self.raton_pos and (x, y) not in self.posiciones_iniciales():
                obstaculos.add((x, y))
        return obstaculos
    

    
# metodo para que los obstaculos no se agreguen en las direcciones posibles de movimiento inicial
    def posiciones_iniciales(self):
        posiciones = set()
        
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Direcciones posibles: arriba, abajo, izquierda, derecha
        for dx, dy in direcciones:
            nuevo_x_gato = self.gato_pos[0] + dx
            nuevo_y_gato = self.gato_pos[1] + dy
            
             # Verificar si la nueva posición está dentro del tablero
            if 0 <= nuevo_x_gato < self.tamaño and 0 <= nuevo_y_gato < self.tamaño:
                posiciones.add((nuevo_x_gato, nuevo_y_gato))
                
            # Posiciones posibles para el ratón
            nuevo_x_raton = self.raton_pos[0] + dx
            nuevo_y_raton = self.raton_pos[1] + dy            
            
            # Verificar si la nueva posición está dentro del tablero
            # que no sea menor que cero y al mismo tiempo que sea menor que el tamanho del tablero
            if 0 <= nuevo_x_raton < self.tamaño and 0 <= nuevo_y_raton < self.tamaño:
                posiciones.add((nuevo_x_raton, nuevo_y_raton)) #se agrega los valores a la nueva posicion del gato y del raton
                
        return posiciones
  

    def dibujar_tablero(self):
        self.canvas.delete("all")
        tamaño_celda = 400 // self.tamaño
        for i in range(self.tamaño):
            for j in range(self.tamaño):
                x1, y1 = i * tamaño_celda, j * tamaño_celda
                x2, y2 = x1 + tamaño_celda, y1 + tamaño_celda
                color = "white"
                if (i, j) in self.obstaculos:
                    color = "pink"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.actualizar_posiciones()



    def actualizar_posiciones(self):
        tamaño_celda = 400 // self.tamaño
        gato_x, gato_y = self.gato_pos
        raton_x, raton_y = self.raton_pos
        self.canvas.create_oval(gato_x * tamaño_celda, gato_y * tamaño_celda,
                                (gato_x + 1) * tamaño_celda, (gato_y + 1) * tamaño_celda,
                                fill="gold")
        self.canvas.create_oval(raton_x * tamaño_celda, raton_y * tamaño_celda,
                                (raton_x + 1) * tamaño_celda, (raton_y + 1) * tamaño_celda,
                                fill="purple")

    def seleccionar_celda(self, evento):
        tamaño_celda = 400 // self.tamaño
        x, y = evento.x // tamaño_celda, evento.y // tamaño_celda
        if self.turno_raton and (x, y) in self.movimientos_posibles(self.raton_pos):
            self.raton_pos = (x, y)
            self.historial.agregar_movimiento(self.gato_pos, self.raton_pos)
            self.dibujar_tablero()
            
            
            if self.raton_pos == self.pos_inicial_gato:
                self.mostrar_mensaje_ganaste()
                
            else: 
                self.turno_raton = False 
                self.mover_gato() 


    def mover_gato(self):
        _, mejor_movimiento = self.minimax(self.tablero, self.gato_pos, self.raton_pos, 8, True, float('-inf'), float('inf'))
        self.gato_pos = mejor_movimiento
        self.historial.agregar_movimiento(self.gato_pos, self.raton_pos)
        self.dibujar_tablero()

        if self.gato_pos == self.raton_pos: 
            self.mostrar_mensaje_perdido()
        self.turno_raton = True 


   
    def mostrar_mensaje_perdido(self):
        messagebox.showinfo("Juego Terminado", "¡Perdiste! El gato atrapó al ratón.")
        self.raiz.quit() 
    
    
    def mostrar_mensaje_ganaste(self):
        messagebox.showinfo("Juego Terminado", "¡Ganaste! El ratón llegó a la posición inicial del gato.")
        self.raiz.quit() 





    """ ------------------- funcion de evaluacion ----------------------"""    
    
    def evaluar_estado(self, gato_pos, raton_pos):
        if gato_pos == raton_pos:
            return float('inf')  
        
        distancia = abs(gato_pos[0] - raton_pos[0]) + abs(gato_pos[1] - raton_pos[1])
        return -distancia  
                           
    
   



    """ ------------------- Metodo para el minimax ----------------------"""    

    def minimax(self, tablero, gato_pos, raton_pos, profundidad, max_jugador, alpha, beta):
        if gato_pos == raton_pos or profundidad == 0:
            return self.evaluar_estado(gato_pos, raton_pos), gato_pos
        
        if max_jugador:
            max_eval = float('-inf')
            mejor_movimiento = gato_pos
            for mov in self.movimientos_posibles(gato_pos):
                eval, _ = self.minimax(tablero, mov, raton_pos, profundidad - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    mejor_movimiento = mov
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                
            return max_eval, mejor_movimiento
        else:
            min_eval = float('inf')
            mejor_movimiento = raton_pos
            for mov in self.movimientos_posibles(raton_pos):
                eval, _ = self.minimax(tablero, gato_pos, mov, profundidad - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    mejor_movimiento = mov
                beta = min(beta, eval)

               
                if beta <= alpha:
                    break
            return min_eval, mejor_movimiento

    def movimientos_posibles(self, pos):
        x, y = pos
        posibles = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nuevo_x, nuevo_y = x + dx, y + dy
            if 0 <= nuevo_x < len(self.tablero) and 0 <= nuevo_y < len(self.tablero) and (nuevo_x, nuevo_y) not in self.obstaculos:
                posibles.append((nuevo_x, nuevo_y))
        return posibles


""" ------------------- crear nodo del arbol ----------------------"""

class Nodo:
    def __init__(self, gato_pos, raton_pos):
        self.gato_pos = gato_pos
        self.raton_pos = raton_pos
        self.siguiente = None 
        self.anterior = None 



""" ------------------- crear Historial de Movimientos ----------------------"""

class HistorialMovimientos:
    def __init__(self):
        self.cabeza = None
        self.cola = None

   
    def agregar_movimiento(self, gato_pos, raton_pos):
        nuevo_nodo = Nodo(gato_pos, raton_pos)
        if self.cola:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        else:
            self.cabeza = self.cola = nuevo_nodo

    
    def deshacer_movimiento(self):
        if self.cola and self.cola.anterior:
            self.cola = self.cola.anterior
            self.cola.siguiente = None
        elif self.cola:
            self.cabeza = self.cola = None

if __name__ == "__main__":
    raiz = tk.Tk()
    juego = JuegoGatoRaton(raiz)
    raiz.mainloop()
