from tkinter import *
from tkinter import ttk, font
import getpass

import pandas as pd
import networkx as nx
import graphviz as gv
import random


class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('800x500')
        self.raiz.title("Algoritmo")

        self.df = None
        self.res = None
        self.res_dos = None
        self.Categoria = ("Hotel", "Hostal", "Hospedaje")
        self.Establecimientos=[]
        self.texto_info=[]
        self.Grafo = nx.Graph()

        # fuente = font.Font(weight='bold')
        self.etiq1 = ttk.Label(self.raiz, text="Distrito:", padding=(5, 5))
        self.etiq2 = ttk.Label(self.raiz, text="Costo Inicial:", padding=(5, 5))
        self.etiq3 = ttk.Label(self.raiz, text="Costo Final:", padding=(5, 5))

        self.distrito = StringVar()
        self.costoInicial = IntVar()
        self.costoFinal = IntVar()

        self.ctext1 = ttk.Entry(self.raiz, textvariable=self.distrito, width=30 )
        self.ctext2 = ttk.Entry(self.raiz, textvariable=self.costoInicial, width=30)
        self.ctext3 = ttk.Entry(self.raiz, textvariable=self.costoFinal, width=30)
        self.listbox = Listbox(self.raiz,width=50 )

        self.scrollbar = Scrollbar(self.raiz)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.boton1 = ttk.Button(self.raiz, text="Buscar", command=self.aceptar, padding=(5, 5))
        self.boton2 = ttk.Button(self.raiz, text="Salir", command=quit, padding=(5, 5))
        self.boton3 = ttk.Button(self.raiz, text="Aplicar Factor", command=self.aplicarFactor, padding=(5, 5))

        self.etiq1.grid(column=0, row=0)
        self.etiq2.grid(column=0, row=1)
        self.etiq3.grid(column=0, row=3)
        self.ctext1.grid(column=1, row=0, columnspan=2)
        self.ctext2.grid(column=1, row=1, columnspan=2)
        self.ctext3.grid(column=1, row=3, columnspan=2)
        self.boton1.grid(column=1, row=5)
        self.boton2.grid(column=2, row=5)
        self.boton3.grid(column=3, row=5)

        self.listbox.grid(column=1, row=7, columnspan=5)
        self.scrollbar.grid(column=7, row=7, sticky=NS )
        self.ctext1.focus_set()

        self.raiz.mainloop()

    def cargarDatos(self):
        self.df = pd.read_csv("establecimiento.csv", sep=';', comment='#' ,encoding='utf-8')
        self.res = self.df[self.df["Distrito"] == self.ctext1.get()]

    def crearGrafo(self):
        self.Grafo = nx.path_graph(len(self.Grafo))
        e = list(self.Grafo.nodes)
        self.Grafo.remove_nodes_from(e)

        self.Grafo.add_node(0)
        self.Grafo.nodes[0]["Costo"] = None
        for tipo in self.Categoria:#Hotel; Hostales, Hospedaje
            self.res_dos = self.res[self.res["Categoria"] == tipo]
            total = len(self.res_dos)
            if total > 0:
                self.Grafo.add_edge(0,self.res_dos.iloc[0]['Codigo'])
                for indice in range(total):
                    codigo = self.res_dos.iloc[indice]["Codigo"]
                    costo = self.res_dos.iloc[indice]["Costo"]
                    nombre = self.res_dos.iloc[indice]['Nombre']
                    distrito = self.res_dos.iloc[indice]['Distrito']
                    categoria = self.res_dos.iloc[indice]['Categoria']
                    estrellas = self.res_dos.iloc[indice]['Estrellas']

                    self.Grafo.add_node(codigo)
                    self.Grafo.nodes[codigo]["Codigo"] = codigo
                    self.Grafo.nodes[codigo]["Costo"] = costo
                    self.Grafo.nodes[codigo]["Nombre"] = nombre
                    self.Grafo.nodes[codigo]["Distrito"] = distrito
                    self.Grafo.nodes[codigo]["Categoria"] = categoria
                    self.Grafo.nodes[codigo]["Estrellas"] = estrellas

                    if (indice+1) < total:
                        codigo_relacionado = self.res_dos.iloc[indice+1]['Codigo']
                        self.Grafo.add_edge(codigo, codigo_relacionado)


    def recorrido_dfs(self, grafo, origen, ruta=[]):
        if origen not in ruta:
            ruta.append(origen)
            self.consultar_costo(origen)
            if origen not in grafo:
                return ruta
            for vecino in grafo:
                ruta = self.recorrido_dfs(grafo, vecino, ruta)
        return ruta

    def consultar_costo(self,nodo):
        valorCosto = self.Grafo.nodes[nodo]["Costo"]
        if (valorCosto is not None):
            if int(valorCosto) >= int( self.ctext2.get())  and int(valorCosto) <= int( self.ctext3.get()):
                self.Establecimientos.append(nodo)

    def reducir_costo(self,costo, descuento):
        if costo is None:
            return None
        descuento = 1 - (descuento / 100)
        return costo * descuento

    def dfs(self, grafo, origen, ruta=[]):
        if origen not in ruta:
            ruta.append(origen)
            self.consultar_costo(origen)
            if origen not in grafo:
                return ruta
            for vecino in grafo:
                ruta = self.recorrido_dfs(grafo, vecino, ruta)
        return ruta

    def aplicar_factor_descuento(self, descuento):
        for i in self.Grafo.nodes:
            costo = self.reducir_costo(self.Grafo.nodes[i]["Costo"], descuento)
            self.Grafo.nodes[i]["Costo"] = costo

    def aplicarFactor(self):
        for indice in range(len(self.res)):
            costo = self.res.iloc[indice, 5]
            self.res.iloc[indice, 5] = self.reducir_costo(costo,30)

        self.crearGrafo()
        dato = self.Grafo.adj
        rutas = self.recorrido_dfs(dato,0,[])
        GrafoNuevo = self.nuevo_grafo()
        self.imprimir_data_grafo(GrafoNuevo)
        self.Establecimientos=[]

    def imprimir_data_grafo(self, Grafo):
        self.texto_info=[]
        for nodo in Grafo:
            if nodo > 0:
                texto = str(nodo) + " :"
                texto +=  str(Grafo.nodes[nodo]["Codigo"] )
                texto += str(Grafo.nodes[nodo]["Nombre"])
                texto += str(Grafo.nodes[nodo]["Costo"])
                self.texto_info.append(texto)
        self.listbox.delete(0, END)
        for i in range(len(self.texto_info)):
            self.listbox.insert(i, self.texto_info[i])

    def nuevo_grafo(self):
        GrafoNuevo = nx.Graph()
        for i in range(len(self.Establecimientos)):
            GrafoNuevo.add_node(i)
            GrafoNuevo.nodes[i]["Codigo"] = self.Grafo.nodes[self.Establecimientos[i]]["Codigo"]
            GrafoNuevo.nodes[i]["Nombre"] = self.Grafo.nodes[self.Establecimientos[i]]["Nombre"]
            GrafoNuevo.nodes[i]["Categoria"] = self.Grafo.nodes[self.Establecimientos[i]]["Categoria"]
            GrafoNuevo.nodes[i]["Estrellas"] = self.Grafo.nodes[self.Establecimientos[i]]["Estrellas"]
            GrafoNuevo.nodes[i]["Costo"] = self.Grafo.nodes[self.Establecimientos[i]]["Costo"]
            if (i + 1) < len(self.Establecimientos):
                GrafoNuevo.add_edge(i, i + 1)
        return GrafoNuevo

    def aceptar(self):
        self.cargarDatos()
        self.crearGrafo()
        dato = self.Grafo.adj
        rutas = self.recorrido_dfs(dato, 0,[])
        GrafoNuevo = self.nuevo_grafo()
        self.imprimir_data_grafo(GrafoNuevo)
        self.Establecimientos=[]

def main():
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
     main()
