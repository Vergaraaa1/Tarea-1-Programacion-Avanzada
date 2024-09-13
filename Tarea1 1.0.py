import time
import matplotlib.pyplot as plt

#funcion del decorador para medir el tiempo
def decorador_tiempo(funcion):
    def decorador(*args, **kwargs):
        inicio_tiempo = time.time()
        resultado = funcion(*args, **kwargs)
        fin_tiempo = time.time()
        tiempo_transcurrido = fin_tiempo - inicio_tiempo
        return tiempo_transcurrido, resultado
    return decorador

#clase con solucion programacion dinamica
class CaminosPCBDinamica:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

    @decorador_tiempo
    def contar_caminos(self):
        dp = [[0] * self.columnas for x in range(self.filas)]
        for i in range(self.filas):
            dp[i][0] = 1
        for j in range(self.columnas):
            dp[0][j] = 1 #se inicia la primera fila y columna con 1 como "caso base"
        for i in range(1, self.filas):
            for j in range(1, self.columnas):
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1] #se va llenando la tabla con recurrencia
        return dp[-1][-1] #entrega el numero de caminos



#clase con solucion arboles binarios
class CaminosPCBBinario:
    class Nodo:
        def __init__(self, fila, columna):
            self.fila = fila
            self.columna = columna
            self.izquierda = None #moverse para abajo
            self.derecha = None #moverse a la derecha

    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas

    @decorador_tiempo
    def contar_caminos(self, nodo):
        if nodo.fila == self.filas - 1 and nodo.columna == self.columnas - 1:
            return 1 #caso base, si ya se llego a la esquina derecha
        if nodo.fila >= self.filas or nodo.columna >= self.columnas:
            return 0 #caso en el que quede afuera de la PCB
        if nodo.izquierda is None:
            nodo.izquierda = self.Nodo(nodo.fila + 1, nodo.columna)
        if nodo.derecha is None:
            nodo.derecha = self.Nodo(nodo.fila, nodo.columna + 1)
        return self.contar_caminos(nodo.izquierda) + self.contar_caminos(nodo.derecha) #cuenta los caminos en los arboles y subarboles



#funcion que genera los tiempos de ejecucion de ambos metodos
def generar_tiempos_ejecucion():
    tiempos_dinamica = []
    tiempos_binario = []
    tamaños = range(2, 11) #aqui se eligen los tamaños de la grilla (esta es desde una 2x2 hasta una 10x10)

    for tamaño in tamaños:
        pcb_dinamica = CaminosPCBDinamica(tamaño, tamaño) #sol dinamica
        dinamica_con_tiempo = decorador_tiempo(pcb_dinamica.contar_caminos)
        tiempo_dinamica, _ = dinamica_con_tiempo()
        tiempos_dinamica.append(tiempo_dinamica)

        pcb_binario = CaminosPCBBinario(tamaño, tamaño) #sol arbol binario
        nodo_raiz = pcb_binario.Nodo(0, 0)
        binario_con_tiempo = decorador_tiempo(pcb_binario.contar_caminos)
        tiempo_binario, _ = binario_con_tiempo(nodo_raiz)
        tiempos_binario.append(tiempo_binario)

    return tamaños, tiempos_dinamica, tiempos_binario


#funcion para generar los graficos 
def graficar_tiempos_ejecucion(tamaños, tiempos_dinamica, tiempos_binario):
    plt.plot(tamaños, tiempos_dinamica, label="Programación Dinámica", marker='o')
    plt.plot(tamaños, tiempos_binario, label="Árbol Binario", marker='o')
    plt.xlabel("Tamaño de la Grilla (NxM)")
    plt.ylabel("Tiempo de Ejecución (segundos)")
    plt.title("Comparación de Tiempos de Ejecución")
    plt.legend()
    plt.grid(True)
    plt.show()


tamaños, tiempos_dinamica, tiempos_binario = generar_tiempos_ejecucion()
graficar_tiempos_ejecucion(tamaños, tiempos_dinamica, tiempos_binario)
