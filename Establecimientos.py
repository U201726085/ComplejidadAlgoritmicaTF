import pandas as pd
import networkx as nx
import graphviz as gv
import random

df = pd.read_csv("establecimiento.csv", sep=';', comment='#')
Categoria = ("Hotel", "Hostal", "Hospedaje")
Establecimientos = []

Grafo = nx.Graph()
def crear_grafo(Categoria):
    if len(Grafo) > 0:
        return
    Grafo.add_node(0)
    Grafo.nodes[0]["Costo"] = None
    for i in Categoria:
        res_dos = res[res["Categoria"] == i]
        total = len(res_dos)
        if total > 0:
            Grafo.add_edge(0, res_dos.iloc[0]['Codigo'])
            for i in range(total):
                codigo = res_dos.iloc[i]['Codigo']
                costo = res_dos.iloc[i]['Costo']
                nombre = res_dos.iloc[i]['Nombre']
                distrito = res_dos.iloc[i]['Distrito']
                categoria = res_dos.iloc[i]['Categoria']
                estrellas = res_dos.iloc[i]['Estrellas']
                # Creamos el nodo
                Grafo.add_node(codigo)
                # Agregamos atributos al nodo creado
                Grafo.nodes[codigo]["Codigo"] = codigo
                Grafo.nodes[codigo]["Nombre"] = nombre
                Grafo.nodes[codigo]["Distrito"] = distrito
                Grafo.nodes[codigo]["Categoria"] = categoria
                Grafo.nodes[codigo]["Estrellas"] = estrellas
                Grafo.nodes[codigo]["Costo"] = costo
                if (i + 1) < total:
                    codigo_relacionado = res_dos.iloc[i + 1]['Codigo']
                    Grafo.add_edge(codigo, codigo_relacionado)

# backtracking.
def busqueda_recorrido_dfs(grafo, origen, ruta=[]):
    if origen not in ruta:
        ruta.append(origen)
        consultar_costo(origen)
        if origen not in grafo:
            return ruta
        for vecino in grafo:
            ruta = busqueda_recorrido_dfs(grafo, vecino, ruta)
    return ruta

def recorrido_dfs(grafo, origen, ruta=[]):
    if origen not in ruta:
        ruta.append(origen)
        consultar_costo(origen)
        if origen not in grafo:
            return ruta
        for vecino in grafo:
            ruta = recorrido_dfs(grafo, vecino, ruta)
    return ruta

def consultar_costo(nodo):
    valorCosto = Grafo.nodes[nodo]["Costo"]
    if (valorCosto is not None):
        if valorCosto >= Costo_desde and valorCosto <= Costo_hasta:
            Establecimientos.append(nodo)

def nuevo_grafo():
    GrafoNuevo = nx.Graph()
    for i in range(len(Establecimientos)):
        GrafoNuevo.add_node(i)
        GrafoNuevo.nodes[i]["Codigo"] = Grafo.nodes[Establecimientos[i]]["Codigo"]
        GrafoNuevo.nodes[i]["Nombre"] = Grafo.nodes[Establecimientos[i]]["Nombre"]
        GrafoNuevo.nodes[i]["Categoria"] = Grafo.nodes[Establecimientos[i]]["Categoria"]
        GrafoNuevo.nodes[i]["Estrellas"] = Grafo.nodes[Establecimientos[i]]["Estrellas"]
        GrafoNuevo.nodes[i]["Costo"] = Grafo.nodes[Establecimientos[i]]["Costo"]
        if (i + 1) < len(Establecimientos):
            GrafoNuevo.add_edge(i, i + 1)
    return GrafoNuevo

def dibuja_Grafo(A):
    dot = gv.Graph("Establecimiento")
    dot.node(str(0), Distrito)
    n = len(A)
    nodoPadre = True
    for i in range(n):
        if nodoPadre:
            dot.edge(str(0), str(i + 1))
            nodoPadre = False
        dot.node(str(i + 1), A.nodes[i]['Nombre'] + str(A.nodes[i]['Costo']))
        if (i + 1) < n:
            dot.edge(str(i + 1), str(i + 2))
    return dot

def reducir_costo(costo, descuento):
    if costo is None:
        return None
    descuento = 1 - (descuento / 100)
    return costo * descuento

def aplicar_factor_descuento(descuento):
    for i in Grafo.nodes:
        costo = reducir_costo(Grafo.nodes[i]["Costo"], descuento)
        Grafo.nodes[i]["Costo"] = costo

def ejecutar():
    crear_grafo(Categoria)
    listaAdyacencia = Grafo.adj
    rutaNodos = busqueda_recorrido_dfs(listaAdyacencia, 0)
    grafo_A_mostrar = nuevo_grafo()
    file = random.randint(0, 1000)
    dibuja_Grafo(grafo_A_mostrar).render('resultado' + str(file) + '.gv', view=True)

def imprimir_data_grafo():
    for nodo in Grafo:
        if nodo > 0:
            print(Grafo.nodes[nodo]["Codigo"], Grafo.nodes[nodo]["Nombre"], Grafo.nodes[nodo]["Costo"])


Distrito = input("Ingresar distrito: ")
Costo_desde = int(input("Ingresar rango Inicial: "))
Costo_hasta = int(input("Ingresar rango Final: "))
if not Distrito:
   print("ingrese texto mas largo")
else:
    res = df[df["Distrito"] == Distrito]
    ejecutar()
    imprimir_data_grafo()

Descuento = int(input("Aplicar descuento: 0=No ; 1=Si :"))
if Descuento >0:
    aplicar_factor_descuento(30)
    Establecimientos=[]
    crear_grafo(Categoria)
    listaAdyacencia = Grafo.adj
    crear_grafo=recorrido_dfs(listaAdyacencia,0)
    grafo_A_mostrar = nuevo_grafo()
    file = random.randint(0, 1000)
    dibuja_Grafo(grafo_A_mostrar).render('resultado' + str(file) + '.gv', view=True)
    imprimir_data_grafo()
else:
    print("No Aplicar descuento")