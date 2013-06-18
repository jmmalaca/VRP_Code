'''
Created on 28 de Abr de 2013

@author: josemiguelmalaca
'''
from numpy import * 
from functions import *
from Genetic_Algorithm import *

print "\nProjecto CE: Vehicle Routing Problem"
DadosProblema = ler_Dados_Teste('teste.vrp','solucao.opt')

N_Clientes = DadosProblema[0]
N_Veiculos = DadosProblema[1]
Capacidade = DadosProblema[2]
Optimo = DadosProblema[3]
Mapa = DadosProblema[4]
Pedidos = DadosProblema[5]

#calcular distancias de todos a todos
Distancias = CalcularDistancias(Mapa)

Geracoes = 1000
N_Start_Individuos = 100
Num_Individous_Elite = N_Start_Individuos/5

Sp = 2
Prob_Mutacao = (1 - 1./Sp)*0.8
Prob_Recombinacao = 0.7

numTestes = 1

for i in range(numTestes):
    #OX -> Ordered CrossOver 
    algoritmoRec = "OX"
    BestsOX = VehicleRoutingProblem(N_Clientes, N_Veiculos, Capacidade, Mapa, Pedidos, Geracoes, N_Start_Individuos, Num_Individous_Elite, Prob_Mutacao, Sp, Prob_Recombinacao, algoritmoRec, Distancias)
    
    #CX -> Cyclic crossover
    algoritmoRec = "CX"
    BestsCX = VehicleRoutingProblem(N_Clientes, N_Veiculos, Capacidade, Mapa, Pedidos, Geracoes, N_Start_Individuos, Num_Individous_Elite, Prob_Mutacao, Sp, Prob_Recombinacao, algoritmoRec, Distancias)
        
    #PMX -> Partially-matched crossover
    algoritmoRec = "PMX"
    BestsPMX = VehicleRoutingProblem(N_Clientes, N_Veiculos, Capacidade, Mapa, Pedidos, Geracoes, N_Start_Individuos, Num_Individous_Elite, Prob_Mutacao, Sp, Prob_Recombinacao, algoritmoRec, Distancias)
    
    #EX -> Edges crossover
    algoritmoRec = "EX"
    BestsEX = VehicleRoutingProblem(N_Clientes, N_Veiculos, Capacidade, Mapa, Pedidos, Geracoes, N_Start_Individuos, Num_Individous_Elite, Prob_Mutacao, Sp, Prob_Recombinacao, algoritmoRec, Distancias)
    
    #Sbr -> geometric crossover
    algoritmoRec = "SbR"
    BestsSbR = VehicleRoutingProblem(N_Clientes, N_Veiculos, Capacidade, Mapa, Pedidos, Geracoes, N_Start_Individuos, Num_Individous_Elite, Prob_Mutacao, Sp, Prob_Recombinacao, algoritmoRec, Distancias)
    
    #mostrar os resultados...
    show_compare_results(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa, Pedidos, Distancias, Optimo, i)
    
    #guardar os resultados para verifica-los no fim...
    save_compare_results(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa, Pedidos, Distancias, Optimo)
    
