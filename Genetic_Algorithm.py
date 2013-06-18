'''
Created on 28 de Abr de 2013

@author: josemiguelmalaca
'''
from functions import *
from operator import itemgetter

def VehicleRoutingProblem(N_Clientes, N_Veiculos, Capacidade, Mapa, Pedidos, Geracoes, N_Start_Individuos, Elite, Prob_Mutacao, Sp, Prob_Recombinacao, algoritmoRec, Distancias):
    #print "N_Clientes: ",N_Clientes
    #print "N_Veiculos: ",N_Veiculos
    #print "Capacidade: ",Capacidade
    #print "Mapa: ",Mapa
    #print "Pedidos: ",Pedidos
    #print_Mapa(Mapa, Pedidos)
    
    Bests = []
    
    #populacao random
    populacao = []
    i = 0
    while i < N_Start_Individuos:
        individuo = Gen_Ran_Individuo(N_Clientes, N_Veiculos)
        populacao.append(individuo)
        i = i + 1
    #print "Populacao Inicial"
    #print_populacao(populacao)
    
    #start...
    i = 0
    while i < Geracoes:
        #ordenar esta...
        custos = calcular_custoViagens_E_Capacidade(Distancias, populacao, Pedidos, Capacidade)
        # Assign fitness, valor 0 para o pior e aumento ate ao melhor
        fitnesses = ranking(custos, Sp)
        #print "\nFitnesses: ",fitnesses
        #ordenar a populacao, quicksort, versao do maior para o mais pequeno, visto que o com maior fitness, melhor o individou, posicao 0
        populacao = ordenar_pela_fitness(populacao, fitnesses)
        #print "\nPopulacao Ordenada pela Fitness: "
        #print_populacao(populacao)
        
        #populacao com os 100 ind da nova populacao mais os 80 pais escolhidas da geracao anterior ordenados pelos melhores, escolher os 100
        #populacao = populacao[:N_Start_Individuos]
        
        pop = []
        pop.append(populacao[0])
        Best = [populacao[0], calcular_custoViagens(Distancias, pop)]
        print "Algoritmo:",algoritmoRec,"Geracao[",i,"],Best: ",Best
        Bests.append(Best)
        
        #recombinacoes...
        populacao = recombinacao(populacao, Elite, Prob_Recombinacao, Distancias, algoritmoRec, Pedidos, Capacidade, Sp)
        
        #mutacoes...
        populacao = mutacoes(populacao, Elite, Prob_Mutacao)
        
        i = i+1
        
    return Bests
    
    