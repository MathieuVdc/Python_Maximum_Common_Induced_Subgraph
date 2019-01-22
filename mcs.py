# Mathieu VANDECASTEELE 2018
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import warnings
import itertools as it
import matplotlib.cbook
from utils import *
from graph import *
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

   
def combinations(liste,k):
    return list(it.combinations(liste, k))


def combinations_recursive(graph,min_nombre_vertex):
    nodes = graph.nodes
    length = len(nodes)
    combinaisons = []
    for i in range(min_nombre_vertex,length+1):
        combinaisons.extend(combinations(nodes,i))
    return combinaisons
    

def find_K(laplacian, min_energy = 0.9):
   
    parcours_total = 0.0
    total = sum(laplacian)
    
    if total == 0.0:
        
        return len(laplacian)
    
    for i in range(len(laplacian)):
        parcours_total += laplacian[i]
        if parcours_total/total >= min_energy:
            return i+1
        
    return len(laplacian)


def eigenvector_similarity(graph1, graph2):
    
    # Calcul des valeurs propres des laplaciens des graphs : 
    laplacien_1 = nx.spectrum.laplacian_spectrum(graph1)
    laplacien_2 = nx.spectrum.laplacian_spectrum(graph2)
    
    # On trouve le meilleur K pour les deux graphs
    K_1 = find_K(laplacien_1)
    K_2 = find_K(laplacien_2)
    
    K = min(K_1, K_2)

    distance = sum((laplacien_1[:K]-laplacien_2[:K])**2)
    return distance


def extract_induced_subgraph(graph, list_nodes_tokeep):
    subgraph = graph.copy()
    listnodes = [x for x in subgraph.nodes if x not in list_nodes_tokeep]
    subgraph.remove_nodes_from(listnodes)
    return subgraph


def extract_all_induced_subgraphs(graph,combinaisons):
    subgraphs = []
    for combinaison in combinaisons:
        subgraphs.append(extract_induced_subgraph(graph,combinaison))
    return subgraphs

def mcs(G1,G2, min_nombre_vertex = 1):
    
    # Combinaisons
    print("Combinaisons en construction...")
    nodesG1 = len(G1.nodes)
    nodesG2 = len(G2.nodes)
    combinaisons1 = combinations_recursive(G1,min_nombre_vertex)
    print("Nombre de combinaisons Graph 1 :")    
    print(len(combinaisons1))
    combinaisons2 = combinations_recursive(G2,min_nombre_vertex)
    print("Nombre de combinaisons Graph 2 :")    
    print(len(combinaisons2))
    print("Terminé!")
    
    # Construction et Stockage des Sous-Graphes Induits
    print("Extraction des Induced Subgraphs...")    
    subgraphs1 = []
    for combinaison in combinaisons1:
        graph_extracted = extract_induced_subgraph(G1,combinaison) 
        if nx.is_connected(graph_extracted):
            subgraphs1.append(graph_extracted)      
    subgraphs2 = []
    for combinaison in combinaisons2:
        graph_extracted = extract_induced_subgraph(G2,combinaison) 
        if nx.is_connected(graph_extracted):
            subgraphs2.append(graph_extracted)   
    print("Terminé!")    
    
    # Distances et stockage des sous graphs communs
    communs = []
    print("Distances...")
    for sub1 in subgraphs1:
        for sub2 in subgraphs2:
            if (len(sub1.nodes) == len(sub2.nodes)):
                distance = eigenvector_similarity(sub1,sub2)
                if (distance == 0.0):
                    communs.append((sub1,sub2,len(sub1.nodes)))                               
    print("Terminé!")
    return communs