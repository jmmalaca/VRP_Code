
'''
Created on 28 de Abr de 2013

@author: josemiguelmalaca
'''
from pylab import *
from matplotlib import *
import random
from itertools import groupby

def ler_Dados_Teste(FicheiroTeste, FicheiroSolucao):
    dadosTeste = []
    f = open(FicheiroTeste,'r')
    for line in f:
        dadosTeste.append( line.translate(None, ',\n)').split(" ") )
    f.close
    #print dadosTeste
    
    dadosResultado = []
    f = open(FicheiroSolucao,'r')
    for line in f:
        dadosResultado.append( line )
    f.close
    #print dadosResultado
    
    DadosProblema = []
    
    N_Clientes = int(dadosTeste[3][2])
    DadosProblema.append(N_Clientes)
    #print "N_Clientes: ",N_Clientes
    
    N_Veiculos = int(dadosTeste[1][8])
    DadosProblema.append(N_Veiculos)
    #print "N_Veiculos: ",N_Veiculos
    
    Capacidade = int(dadosTeste[5][2])
    DadosProblema.append(Capacidade)
    #print "Capacidade: ",Capacidade

    Optimo = int(dadosTeste[1][11])
    DadosProblema.append(Optimo)
    #print "Resultado Optimo: ",Optimo
    
    dadosMapa = dadosTeste[7:7+N_Clientes]
    Mapa = []
    for dados in dadosMapa:
        strs = dados[2:4]
        nums = []
        for elem in strs:
            nums.append(int(elem))
        Mapa.append(nums)
    DadosProblema.append(Mapa)
    #print Mapa
    
    dadosSolucao = dadosTeste[7+N_Clientes+1:7+2*N_Clientes+1]
    #print "Solucao: ",dadosSolucao
    Mapa = []
    for dados in dadosSolucao:
        strs = dados[1]
        Mapa.append(int(strs))
    DadosProblema.append(Mapa)    
    return DadosProblema
    
def print_Mapa(ax, Mapa, Pedidos):
    x = [row[0] for row in Mapa]
    y = [row[1] for row in Mapa]
    ax.plot(x, y, 'o')
    for i, label in enumerate(Pedidos): 
        if(i == 0):
            pyplot.text (x[i], y[i], 'Base' ) 
        else:
            pyplot.text (x[i], y[i], label )
     
    plot(x[0], y[0], "o", color='r')
    
def print_Percurso(Percurso):
    x = [row[0] for row in Percurso]
    y = [row[1] for row in Percurso]
    title('Mapa')
    xlabel('X')
    ylabel('Y')
    plot(x, y)
    plot(x[0], y[0], "o", color='r', linestyle='--')
    pyplot.show()
    
def CalcularDistancias(Mapa):
    #print "Mapa: ",Mapa
    Distancias = []
    i = 0
    for i in range(len(Mapa)):
        j = 0
        DistanciasDeste = []
        for j in range(len(Mapa)):
            pontoA = Mapa[i]
            pontoB = Mapa[j]
            distancia = sqrt(pow((pontoB[0]-pontoA[0]), 2)+pow((pontoB[1]-pontoA[1]), 2))
            DistanciasDeste.append(int(distancia))
        #print "i:",i," - ",DistanciasDeste
        Distancias.append(DistanciasDeste)
    return Distancias

def Gen_Ran_Individuo(N_Clientes, N_Veiculos):
    indices = [i for i in range(N_Clientes)]
    #print "indices",indices
    
    idasDeposito = 90
    
    individuo = []
    individuo.append(idasDeposito)
    idasDeposito = idasDeposito + 1
    indices.remove(0)
    
    #numVeiculos = randint(1,N_Veiculos)
    numVeiculos = N_Veiculos
    #print "numVeiculos",numVeiculos
    for i in range(numVeiculos):
        if (i == numVeiculos-1):
            map(individuo.append, permutation(indices))
            individuo.append(idasDeposito)
        else:
            numVisitasCliente = randint(1,len(indices)/numVeiculos)
            for j in range(numVisitasCliente):
                cliente = random.choice(indices)
                individuo.append(cliente)
                indices.remove(cliente)
            individuo.append(idasDeposito)
            idasDeposito = idasDeposito + 1
        #print "numVeiculos: ",numVeiculos,"numVisitasCliente: ",numVisitasCliente
        #print "individuo",individuo,"indices: ",indices
    return individuo

def print_populacao(populacao):
    for elemt in populacao:
        print elemt

def verificarCarga(individuo, Pedidos):
    #print "Individuo",individuo
    #print "Pedidos",Pedidos
    carga = 0
    cargasPercursos = []
    for i in range(len(individuo)):
        elem = individuo[i]
        
        if i > 0:
            if elem >= 90:
                cargasPercursos.append(carga)
                carga = 0
            else:
                carga = carga + Pedidos[elem]
            
    #print "cargasPercursos",cargasPercursos
    return cargasPercursos

def calcular_custoViagens_E_Capacidade(Distancias, populacao, Pedidos, Capacidade):
    custosTotais = []
    
    for i in range(len(populacao)):
        individuo = populacao[i]
        #print "Individuo",individuo
        
        total = []
        
        carga = 0
        cargasPercurso = []
        cost = 0
        custosPercurso = []
        for j in range(len(individuo)):
            elem = individuo[j]
            
            if j > 0:
                if elem >= 90:
                    cargasPercurso.append(carga)
                    custosPercurso.append(cost)
                    carga = 0
                    cost = 0
                else:
                    #carga
                    carga = carga + Pedidos[elem]
                    #percurso
                    A = individuo[j]
                    B = individuo[j-1]
                    if A >= 90:
                        A = 0
                    if B >= 90:
                        B = 0
                    cost = cost + Distancias[A][B]
            
        #print "cargasPercurso",cargasPercurso
        #print "custosPercurso",custosPercurso
        total.append(cargasPercurso)
        total.append(custosPercurso)
        custosTotais.append(total)
    
    custos = []
    Imposto = 100
    
    for elem in custosTotais:
        i = 0
        for elem2 in elem[0]:
            if elem2 > Capacidade:
                #capacidade
                i = i + (elem2-Capacidade)*(Imposto)
                #percursos
                i = i + 0.1*sum(elem[1])
            else:
                #capacidade
                #i = i + (Capacidade-elem2)
                #percursos
                i = i + 0.1*sum(elem[1])
        #print "cargasPercurso",elem[0],"custosPercurso",elem[1],"cost",i
        custos.append(i)
        
    return custos
    
def calcular_custoViagens(Distancias, populacao):
    custos = []
    for individuo in populacao:
        cost = 0
        i = 1
        while i < len(individuo):
            A = individuo[i]
            B = individuo[i-1]
            
            if A >= 90:
                A = 0
            if B >= 90:
                B = 0
            
            cost = cost + Distancias[A][B]
            i = i + 1
        custos.append(cost)
    return custos

def ranking(custos, Sp):
    numero_individuos = len(custos)
    
    fitness = numpy.empty(numero_individuos, float)
    
    #ix = indices do array ordenado de forma crescente
    ix = numpy.argsort(custos)
    #reverse = ix[::-1]
    #print "reverse",reverse
    
    fitness[ix] = Sp - (Sp-1.) * 2. * numpy.arange(numero_individuos) / (numero_individuos-1.)
    return fitness

def samplePopulacao(fitness):
    numero_individuos = len(fitness)
    fitness_cumulativo = numpy.cumsum(fitness)
    fitness_cumulativo = fitness_cumulativo * numero_individuos / fitness_cumulativo[-1]
    #print "fitness_cumulativo",fitness_cumulativo
    #random de valores para cada
    ptr = numpy.arange(numero_individuos) + numpy.random.random()
    #print "ptr",ptr
    #verificar em que janela comulativa o valor random escolhido entra
    ix = numpy.sum(ptr[:, numpy.newaxis] >= fitness_cumulativo, -1)
    #print "ix",ix
    #shuffle os valores do array ix
    numpy.random.shuffle(ix)
    #print "ix",ix
    return ix

def ordenar_pela_fitness(populacao, fitnesses):
    
    if len(populacao) <= 1:
        return populacao # uma lista vazia ou com 1 elemento ja esta ordenada
    
    lessPop, equalPop, greaterPop = [], [], [] # cria as sublistas dos maiores, menores e iguais ao pivo
    lessFit, greaterFit = [], []
    
    pivot = fitnesses[0] # escolhe o pivo. neste caso, o primeiro elemento da lista de fitnesses
    
    i=0
    for x in populacao:
        # adiciona o elemento x a lista corespondeste
        if fitnesses[i] < pivot: 
            lessPop.append(x)
            lessFit.append(fitnesses[i])
            
        elif fitnesses[i] == pivot:
            equalPop.append(x)
            
        else:
            greaterPop.append(x)
            greaterFit.append(fitnesses[i])
        i = i + 1
    
    # concatena e retorna recursivamente.. as listas ordenadas
    return ordenar_pela_fitness(greaterPop, greaterFit) + equalPop + ordenar_pela_fitness(lessPop, lessFit)

def chooseParentTorneio(populacao, Distancias, Pedidos, Capacidade, Sp):
    nums = [i for i in range(len(populacao))]
    numA = random.choice(nums)
    nums.remove(numA)
    numB = random.choice(nums)
    nums.remove(numB)
    numC = random.choice(nums)
    nums.remove(numC)
    numD = random.choice(nums)
    #print "nums",nums,"A",numA,"B",numB
    
    #torneio...
    pop = []
    pop.append(populacao[numA])
    pop.append(populacao[numB])
    pop.append(populacao[numC])
    pop.append(populacao[numD])
    #ordenar esta...
    #custos = calcular_custoViagens(Distancias, populacao)
    custos = calcular_custoViagens_E_Capacidade(Distancias, pop, Pedidos, Capacidade)
         
    # Assign fitness, valor 0 para o pior e aumento ate ao melhor
    fitnesses = ranking(custos, Sp)
    #print "\nFitnesses: ",fitnesses
         
    #ordenar a populacao, quicksort, versao do maior para o mais pequeno
    pop = ordenar_pela_fitness(pop, fitnesses)
    
    parents = []
    parents.append(pop[0])
    parents.append(pop[1])
    return parents

#Ordered CrossOver
def orderedCrossOver(parentOne, parentTwo):
    #print "Parents:"
    #print parentOne
    #print parentTwo
    child = ["G" for i in range(len(parentOne))]
    #print child
    #escolher posicoes onde cortar
    cortes = []
    cortes.append(randint(1,len(parentOne)-3))
    corte = randint(1,len(parentOne)-2)
    while corte == cortes[0]:
        corte = randint(1,len(parentOne)-2)
    cortes.append(corte)
    cortes.sort()
    #print "Cortes",cortes
    
    #copiar o segment dentro do parentOne, destes dois cortes, para o filho
    segmento = []
    for i in range(cortes[1]):
        if (i >= cortes[0] and i <= cortes[1]):
            child[i]=parentOne[i]
            segmento.append(parentOne[i])
            
    #verificar os genes que faltam no child do parentOne
    #ordenar estes que faltam pela ordem que aparecem no parentTwo
    copy = parentTwo[:]
    for i in range(len(segmento)):
        if segmento[i] in copy:
            copy.remove(segmento[i])
    #print "parentTwo updated",parentTwo
    
    #colocar estes que faltam no child
    j = 0
    #print "Cortes: ",cortes
    for i in range(len(child)):
        if i < cortes[0] and j < len(copy):
            child[i]=copy[j]
            j = j + 1
        if i >= cortes[1] and j < len(copy):
    #        print "i[",i,"],j[",j,"]"
            child[i]=copy[j]
            j = j + 1
    
    #print "Child:"
    #print child
    return child

#Cyclic crossover (CX): identifies a number of so-called cycles between two parent chromosomes.
def cyclicCrossover(parentOne, parentTwo):
    #print "ONE:",parentOne
    #print "TWO:",parentTwo
    child = ["G" for i in range(len(parentOne))]
    
    child[0] = parentOne[0]
    
    i = 1
    while parentTwo[i] not in child:
        if parentTwo[i] in parentOne:
            j = parentOne.index(parentTwo[i])
            child[j]=parentOne[j]
            if j < len(parentTwo):
                i=j
        else:
            i = i + 1
    
    for i in range(len(child)):
        if child[i] == "G":
            child[i] = parentTwo[i]
    
    #print "Child ",child
    return child

def helpPMC(parentOne, parentTwo, elem, cortes, child, valorPonto3):
    #Step 3.1. Note the index of the value in parent 2
    indice = parentTwo.index(elem)
    #and locate the value from parent 1 in the same position.
    value = parentOne[indice]
    indice2 = parentTwo.index(value)
    
    #Step 3.3. If the index of this value in parent 2 is a part of the original segment, go to step 3.1 using this value.
    if indice2 >= cortes[0] and indice2 <= cortes[1]:
        helpPMC(parentOne, parentTwo, value, cortes, child, valorPonto3)
    #Step 3.4. If the position isn't a part of the original segment, insert the value derived from step 3 into child 1 in this position.
    else:
        child[indice2] = valorPonto3
        
    return child
    
#Partially-matched crossover (PMX)
def PartiallyMatchedCrossover(parentOne, parentTwo):
    child = ["G" for i in range(len(parentOne))]
        
    #Step 1. Randomly select a segment of genes from parent 1 and copy them directly to child 1.
    #escolher posicoes onde cortar
    cortes = []
    cortes.append(randint(1,len(parentOne)-3))
    corte = randint(1,len(parentOne)-2)
    while corte == cortes[0]:
        corte = randint(1,len(parentOne)-2)
    cortes.append(corte)
    cortes.sort()
    #print "\nCortes",cortes
    
    #copiar o segment dentro do parentOne, destes dois cortes, para o filho
    for i in range(len(parentOne)):
        if (i >= cortes[0] and i <= cortes[1]):
            child[i]=parentOne[i]
    #print "Child1",child
    
    #Step 2. In the same segment positions of parent 2, select each value that has not already been copied to child 1.
    seg2 = parentTwo[cortes[0]:cortes[1]]
    faltam = []
    for elem in seg2:
        if elem not in child:
            faltam.append(elem)
    #print "\nFaltam1",faltam,"len",len(faltam)
    
    #Step 3. For each of the selected values:
    for elem in faltam:
        child = helpPMC(parentOne, parentTwo, elem, cortes, child, elem)
        
    #Step 4. Copy any remaining positions from parent 2 to child 1.
    faltam = []
    for elem in parentTwo:
        if elem not in child:
            faltam.append(elem)
     
    j = 0
    for i in range(len(child)):
        if child[i] == "G":
            if j < len(faltam):
                child[i] = faltam[j]
                j = j + 1
                
    #print "Child ",child
    return child

#calcular os edges para um parent
def getEdges(parent):
    edges = []
  
    position = 1
    for position in range(len(parent)-2):
        if position == 0:
            edges.append([parent[position], (parent[-1], parent[position+1])])
        elif position < len(parent)-1:
            edges.append([parent[position], (parent[position-1], parent[position+1])])
        else:
            edges.append([parent[position], (parent[position-1], parent[0])])
    return edges

#part of merge_edges - unions 2 individual
def union(individual1, individual2):
    edges = list(individual1)

    for val in individual2:
        if val not in edges:
            edges.append(val)
    return edges

#sort the edges    
def sort_edges(individual):
    individual.sort(lambda x, y: cmp(x[0],y[0]))
  
#perform an union on two parents
def merge_edges(edgesOne, edgesTwo):
    #sort_edges(edgesOne)
    #sort_edges(edgesTwo)
  
    edges = []
    
    #if len(edgesOne) < len(edgesTwo):
    for i in range(len(edgesOne)):
        #print "I",i,"One:",len(edgesOne),"Two:",len(edgesTwo)
        edges.append([edgesOne[i][0], union(edgesOne[i][1], edgesTwo[i][1])])
    #else:
    #    for i in range(len(edgesTwo)):
    #        #print "I",i,"One:",len(edgesOne),"Two:",len(edgesTwo)
            #edges.append([edgesTwo[i][0], union(edgesTwo[i][1], edgesOne[i][1])])
        
    return edges

# removes node from neighbouring list
def remove_node_from_neighbouring_list(node, neighbour_list):
    removed_node = None

    for n in neighbour_list:
        if n[0] == node:
            removed_node = n
            neighbour_list.remove(n)
    
        if node in n[1]:
            n[1].remove(node)
    
    return removed_node

#return neighbours for a give node(s)
def get_current_neighbour(nodes, neighbour_lists):
    neighbours = []

    if nodes is not None:
        for node in nodes[1]:
            for neighbour in neighbour_lists:
                if node == neighbour[0]:
                    neighbours.append(neighbour)
    return neighbours

#part of get_best_neighbour   
def group_neighbours(neighbours):
    sorted_neighbours = []

    #store length of each individual neighbour + neighbour in a list
    for neighbour in neighbours:
        sorted_neighbours.append((len(neighbour[1]), neighbour))

    #sort the new list
    #sort_edges(sorted_neighbours)
    
    #group the neighbour by their size
    groups = []
    for k, g in groupby(sorted_neighbours, lambda x: x[0]):
        groups.append(list(g))

    return groups

#returns the best possible neighbour
def get_best_neighbour(neighbour):
    if len(neighbour) is 1:
        return neighbour[0]
    else:
        group_neighbour = group_neighbours(neighbour)
    return random.choice(group_neighbour[0])[1]

#returns a random neighbour from remaining_edges that does not exist in current_path
def get_next_random_neighbour(child, remaining_edges):
    random_node = None

    while random_node is None and len(remaining_edges) > 0:
        tmp_node = random.choice(remaining_edges)

        if tmp_node[0] not in child:
            random_node = tmp_node
    
    return random_node


#Edge recombination (EX), http://en.wikipedia.org/wiki/Edge_recombination_operator#Algorithm
def Edge_Recombination(parentOne, parentTwo):
    child = ["G" for i in range(len(parentOne))]
        
    edgesOne = getEdges(parentOne)
    edgesTwo = getEdges(parentTwo)
    edges = merge_edges(edgesOne, edgesTwo)
    
    previous = None
    child[0] = random.choice([parentOne[0], parentTwo[0]])
    
    current = child[0]
    
    i = 1
    while i < len(child) and len(edges) > 0:
        
        previous = remove_node_from_neighbouring_list(current, edges)
        current_neighbour = get_current_neighbour(previous, edges)
 
        next_node = None
        if len(current_neighbour) > 0:
            next_node = get_best_neighbour(current_neighbour)
        else:
            next_node = get_next_random_neighbour(child, edges)
        
        if next_node == None:
            break
        else:
            current = next_node[0]
            #print "NEXT:",next_node[0]
            if current not in child:
                child[i] = current
        
        #print "EDGES:"
        #for elem in edges:
        #    print elem
        #print "CHILD:",child
        i = i + 1
        
    faltam = []
    for elem in parentTwo:
        if elem not in child:
            faltam.append(elem)
    for elem in parentOne:
        if elem not in child and elem not in faltam:
            faltam.append(elem)
    #print "\nFaltam2",faltam,"len",len(faltam)
     
    j = 0
    for i in range(len(child)):
        if child[i] == "G":
            if j < len(faltam):
                child[i] = faltam[j]
                j = j + 1
            if j == len(parentTwo)-1:
                child[i] = parentTwo[j]
            if j == len(parentOne)-1:
                child[i] = parentOne[j]
    
    #print "CHILD:",child
    return child;

def check_sequencias(permut):
    #de 1 a n, determinar as sequencias possiveis de distancia 1 a n
    #print "Permut: ",permut,", len(",len(permut),")"
    sequencias = []
    permutSave = permut[:]
    
    for elem in permut:
        permut = permut[permut.index(elem)+1:]
        
        sequencia = []
        sequencia.append(elem)
        for elem2 in permut:
            sequencia.append(elem2)
            inv = sequencia[::-1]
            #print "Seq:",sequencia,", Inv:",inv
            #sequencias.append(sequencia[:])
            sequencias.append(inv[:])
        permut = permutSave[:]
    
    #print "Sequencias:"
    #for elem in sequencias:
    #    print elem
    return sequencias

def check_sequencias_permut2(sequencias, permut):
    return_seq = []
    
    for elem in sequencias:
        #print "Seq:",elem,"Permut:",permut
        posElem = 0
        posPermut = permut.index(elem[0])
        contador = 0
        while posPermut < len(permut):
            #print " -Verif:",elem[posElem],"com",permut[posPermut]
            if elem[posElem] == permut[posPermut]:
                contador = contador + 1
            posElem = posElem + 1
            posPermut = posPermut + 1
            if posElem + 1 > len(elem):
                break
        if contador == len(elem):
            return_seq.append(elem)
    
    return return_seq

def num_valores_iguais(permut1, permut2):
    iguais = 0
    for i in range(len(permut1)):
        if permut1[i] == permut2[i]:
            iguais = iguais + 1
    return iguais;

def invert_seq_help(permut1, permut2):
    ind1 = 0
    for i in range(len(permut1)):
        if permut1[i] != permut2[i]:
            ind1 = i
            break
    ind2 = permut2.index(permut1[ind1])
    #print "ind1:",ind1,", ind2",ind2
    inv = permut1[ind1:ind2+1]
    return inv
    
def compare_lists(permut1, permut2):
    for i in range(len(permut1)):
        if permut1[i] != permut2[i]:
            return False
    return True
    
def apply_reversals(permut1, permut2, dist):
    ops = 0
    permut = permut1[:]
    while ops < dist:
        # com isto procuramos elementos fora de ordem... e invertemos esta sequencia
        invert_seq = invert_seq_help(permut, permut2)
        elem = invert_seq[::-1]
        if len(elem) > 0:
            #print " -Seq help:",elem
            first = elem[len(elem)-1]
            ind = permut.index(first)
            for i in range(len(elem)):
                permut[ind] = elem[i]
                ind = ind + 1
        #print "Reversals after, P1",permut1," to P2",permut2    
        if compare_lists(permut1, permut2):
            break
        ops = ops + 1
    return permut
        
def Calc_Distancia_Reversals(permut1, permut2):
    distancia = 0
    while True:
        # com isto procuramos elementos fora de ordem... e invertemos esta sequencia
        invert_seq = invert_seq_help(permut1, permut2)
        elem = invert_seq[::-1]
        if len(elem) > 0:
            #print " -Seq help:",elem
            first = elem[len(elem)-1]
            ind = permut1.index(first)
            for i in range(len(elem)):
                permut1[ind] = elem[i]
                ind = ind + 1
            distancia = distancia + 1
        #print "Reversals after, P1",permut1," to P2",permut2    
        if compare_lists(permut1, permut2):
            break
        
#         #quantas arestas tem em comum ?
#         sequencias = check_sequencias(permut1)
#         #com as sequencias da permutacao 1, verificar se alguma existe na permutacao 2
#         seq_existem = check_sequencias_permut2(sequencias, permut2)
#         #print "Sequencias que sao mutuas:"
#         #for elem in seq_existem:
#         #    print elem
#         
#         #para cada sequencia
#         for elem in seq_existem:
#             print " -Seq:",elem
#             first = elem[len(elem)-1]
#             ind = permut1.index(first)
#             for i in range(len(elem)):
#                 permut1[ind] = elem[i]
#                 ind = ind + 1
#             distancia = distancia + 1
#             print "Reversals after, P1",permut1," to P2",permut2
#         if compare_lists(permut1, permut2):
#             break
    
    #print " Pais iguais ?",compare_lists(permut1, permut2)
    return distancia

def Reversals_Recombination(parentOne, parentTwo):
    #para testes...
    #p1 = [i for i in range(10)]
    #p2 = [i for i in range(10)]
    #random.shuffle(p1)
    #random.shuffle(p2)
    #print "\n\nReversals before, P1",p1," to P2",p2
    
    distancia = Calc_Distancia_Reversals(parentOne, parentTwo)
    if distancia > 4:
        max = distancia/2
        dist = randint(1,max)
        #print "Distancia calculada: ",distancia,", dist:",dist
        return apply_reversals(parentOne, parentTwo, dist)
    return parentTwo 

def choose_parents(populacao,Distancias, Pedidos, Capacidade, Sp):
    parents = []
    
    if len(populacao) == 2:
        parentOne = populacao[0]
        parentTwo = populacao[1]
        parents.append(parentOne)
        parents.append(parentTwo)
    else:
        #select 2 parents... por torneio
        parents = chooseParentTorneio(populacao, Distancias, Pedidos, Capacidade, Sp)
    
    return parents

def mutacoes(populacao, Elite, probabilidadeM):
    #print "\nPopulacao a Mutar: "
    #print_populacao(populacao[Elite:])
    
    newPopulacao = []
    for i in range(Elite):
        newPopulacao.append(populacao[i])
            
    pop = populacao[Elite:]
    for individuo in range(len(pop)):
        #a mutacao vai acontecer ao nao ??
        mutar = random.random() < probabilidadeM
        #print "\nProbabilidade_Mutacao: ",probabilidadeM,", vamos mutar ? ",mutar
        
        if mutar:
            #tipo de mutacao: 2-opt Select a permutation segment at random and reverse it
            startSegment = randint(1,len(pop[individuo])-3)
            endSegment = randint(startSegment+1,len(pop[individuo])-2)
            
            segmento = pop[individuo][startSegment:endSegment]
            
            #reverse...
            i = 0
            segmentoReversed = []
            for i in range(len(segmento)):
                pop[individuo][startSegment+i]=segmento[(len(segmento)-1)-i]
                segmentoReversed.append(segmento[(len(segmento)-1)-i])
            #print "\nMutar o individou: ",individuo,":\n -Segmento: [",startSegment," a ",endSegment,"] = ",segmento,", Reversed: ",segmentoReversed
            
    #print "\nPopulacao com o individuo mutado:"
    #print_populacao(populacao)
    return newPopulacao+pop

def recombinacao(populacao, Elite, Prob_Recombinacao, Distancias, algoritmo, Pedidos, Capacidade, Sp):
    #print "\nPopulacao a Recombinar: "
    #print_populacao(populacao[Elite:])
     
    #a recombinacao vai acontecer ao nao ??
    recombinar = random.random() < Prob_Recombinacao
    #print "\nProbabilidade_Recombinacao: ",Prob_Recombinacao,", vamos recombinar ? ",recombinar
    
    if recombinar:
        newPopulacao = []
        
        for i in range(Elite):
            newPopulacao.append(populacao[i])
        
        while len(populacao) > Elite:
            #print "len(populacao) = ",len(populacao)
            #print "\n- parentOne",parentOne
            #print "- parentTwo",parentTwo
            
            #recombinar e gerar os filhos
            if algoritmo == "OX":
                parents = choose_parents(populacao, Distancias, Pedidos, Capacidade, Sp)
                childOne = orderedCrossOver(parents[0], parents[1])
                childTwo = orderedCrossOver(parents[1], parents[0])
                #retirar os pais...
                #newPopulacao.append(parents[0])
                #newPopulacao.append(parents[1])
                populacao.remove(parents[0])
                populacao.remove(parents[1])
                #colocar os filhos...
                #print "- ChildOne ",childOne
                #print "- ChildTwo ",childTwo
                newPopulacao.append(childOne)
                newPopulacao.append(childTwo)
            elif algoritmo == "CX":
                parents = choose_parents(populacao, Distancias, Pedidos, Capacidade, Sp)
                childOne = cyclicCrossover(parents[0], parents[1])
                childTwo = cyclicCrossover(parents[1], parents[0])
                #retirar os pais...
                #newPopulacao.append(parents[0])
                #newPopulacao.append(parents[1])
                populacao.remove(parents[0])
                populacao.remove(parents[1])
                #colocar os filhos...
                #print "- ChildOne ",childOne
                #print "- ChildTwo ",childTwo
                newPopulacao.append(childOne)
                newPopulacao.append(childTwo)
            elif algoritmo == "PMX":
                parents = choose_parents(populacao, Distancias, Pedidos, Capacidade, Sp)
                childOne = PartiallyMatchedCrossover(parents[0], parents[1])
                childTwo = PartiallyMatchedCrossover(parents[1], parents[0])
                #retirar os pais...
                #newPopulacao.append(parents[0])
                #newPopulacao.append(parents[1])
                populacao.remove(parents[0])
                populacao.remove(parents[1])
                #colocar os filhos...
                #print "- ChildOne ",childOne
                #print "- ChildTwo ",childTwo
                newPopulacao.append(childOne)
                newPopulacao.append(childTwo)
            elif algoritmo == "EX":
                parents = choose_parents(populacao, Distancias, Pedidos, Capacidade, Sp)
                childOne = Edge_Recombination(parents[0], parents[1])
                childTwo = Edge_Recombination(parents[1], parents[0])
                #retirar os pais...
                #newPopulacao.append(parents[0])
                #newPopulacao.append(parents[1])
                populacao.remove(parents[0])
                populacao.remove(parents[1])
                #colocar os filhos...
                #print "- ChildOne ",childOne
                #print "- ChildTwo ",childTwo
                newPopulacao.append(childOne)
                newPopulacao.append(childTwo)
            elif algoritmo == "SbR":
                nums = [i for i in range(len(populacao))]
                num = random.choice(nums)
                child = Reversals_Recombination(populacao[num], newPopulacao[0])
                #newPopulacao.append(populacao[num])
                populacao.remove(populacao[num])
                newPopulacao.append(child)
            
        #print "\nPopulacao Recombinada: "
        #print_populacao(newPopulacao)
        return newPopulacao
    
    return populacao

def show_percurso_Best(Best, Mapa):
    #ver o percurso Best
    percurso = []
    for i in range(len(Best[0])):
        if Best[0][i] >= 90:
            percurso.append(Mapa[0])
        else:
            percurso.append(Mapa[Best[0][i]])
    print_Percurso(percurso)
    
def show_historico_resultados(Bests):
    historico = []
    for elem in Bests:
        historico.append(elem[1])
    #show the data
    title('Historico dos Bests')
    xlabel('X')
    ylabel('Y')
    plot(historico)
    pyplot.show()

def criarPercursos(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa):
    percursos = []
    
    percursosOX = []
    A = BestsOX[len(BestsOX)-1]
    percursoOX = []
    limites = []
    for i in range(len(A[0])):
        if A[0][i] >= 90:
            percursoOX.append(Mapa[0])
            limites.append(i)
        else:
            percursoOX.append(Mapa[A[0][i]])
    for i in range(len(limites)-1):
        list = percursoOX[limites[i]:limites[i+1]]
        list.append(percursoOX[0])
        percursosOX.append(list)
    percursos.append(percursosOX)
    
    percursosCX = []
    B = BestsCX[len(BestsCX)-1]
    percursoCX = []
    limites = []
    for i in range(len(B[0])):
        if B[0][i] >= 90:
            percursoCX.append(Mapa[0])
            limites.append(i)
        else:
            percursoCX.append(Mapa[B[0][i]])
    for i in range(len(limites)-1):
        list = percursoCX[limites[i]:limites[i+1]]
        list.append(percursoCX[0])
        percursosCX.append(list)
    percursos.append(percursosCX)
    
    percursosPMX = []
    C = BestsPMX[len(BestsPMX)-1]
    percursoPMX = []
    limites = []
    for i in range(len(C[0])):
        if C[0][i] >= 90:
            percursoPMX.append(Mapa[0])
            limites.append(i)
        else:
            percursoPMX.append(Mapa[C[0][i]])
    for i in range(len(limites)-1):
        list = percursoPMX[limites[i]:limites[i+1]]
        list.append(percursoPMX[0])
        percursosPMX.append(list)
    percursos.append(percursosPMX)
    
    percursosEX = []
    C = BestsEX[len(BestsEX)-1]
    percursoEX = []
    limites = []
    for i in range(len(C[0])):
        if C[0][i] >= 90:
            percursoEX.append(Mapa[0])
            limites.append(i)
        else:
            percursoEX.append(Mapa[C[0][i]])
    for i in range(len(limites)-1):
        list = percursoEX[limites[i]:limites[i+1]]
        list.append(percursoEX[0])
        percursosEX.append(list)
    percursos.append(percursosEX)
    
    percursosSbR = []
    C = BestsSbR[len(BestsSbR)-1]
    percursoSbR = []
    limites = []
    for i in range(len(C[0])):
        if C[0][i] >= 90:
            percursoSbR.append(Mapa[0])
            limites.append(i)
        else:
            percursoSbR.append(Mapa[C[0][i]])
    for i in range(len(limites)-1):
        list = percursoSbR[limites[i]:limites[i+1]]
        list.append(percursoSbR[0])
        percursosSbR.append(list)
    percursos.append(percursosSbR)
    
    return percursos

BestOfALL_OX = []
BestOfALL_CX = []
BestOfALL_PMX = []
BestOfALL_EX = []
BestOfALL_SbR = []
def save_compare_results(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa, Pedidos, Distancias, Optimo):
    BestsFinais = []
    cargasFinais = []
    custosFinais = []
    
    BestsFinais.append(BestsOX[len(BestsOX)-1])
    cargasOX = verificarCarga(BestsOX[len(BestsOX)-1][0], Pedidos)
    cargasFinais.append(cargasOX)
    custosFinais.append(BestsFinais[0][0])
    
    BestsFinais.append(BestsCX[len(BestsCX)-1])
    cargasCX = verificarCarga(BestsCX[len(BestsCX)-1][0], Pedidos)
    cargasFinais.append(cargasCX)
    custosFinais.append(BestsFinais[1][0])
    
    BestsFinais.append(BestsPMX[len(BestsPMX)-1])
    cargasPMX = verificarCarga(BestsPMX[len(BestsPMX)-1][0], Pedidos)
    cargasFinais.append(cargasPMX)
    custosFinais.append(BestsFinais[2][0])
    
    BestsFinais.append(BestsEX[len(BestsEX)-1])
    cargasEX = verificarCarga(BestsEX[len(BestsEX)-1][0], Pedidos)
    cargasFinais.append(cargasEX)
    custosFinais.append(BestsFinais[3][0])
    
    BestsFinais.append(BestsSbR[len(BestsEX)-1])
    cargasSbR = verificarCarga(BestsSbR[len(BestsSbR)-1][0], Pedidos)
    cargasFinais.append(cargasSbR)
    custosFinais.append(BestsFinais[4][0])
    
    custos = calcular_custoViagens(Distancias, custosFinais)
    
    print "\n\nCusto Optimo conhecido: ",Optimo
    print "Bests e suas cargas do varios algoritmos:"
    print "BestOX: ",BestsFinais[0]
    print "BestOX cargas: ",cargasFinais[0]
    print "BestOX custo percursos: ",custos[0]
    print "BestsCX: ",BestsFinais[1]
    print "BestsCX cargas: ",cargasFinais[1]
    print "BestsCX custo percursos: ",custos[1]
    print "BestsPMX: ",BestsFinais[2]
    print "BestsPMX cargas: ",cargasFinais[2]
    print "BestsPMX custo percursos: ",custos[2]
    print "BestsEX: ",BestsFinais[3]
    print "BestsEX cargas: ",cargasFinais[3]
    print "BestsEX custo percursos: ",custos[3]
    print "BestsSbR: ",BestsFinais[4]
    print "BestsSbR cargas: ",cargasFinais[4]
    print "BestsSbR custo percursos: ",custos[4]
    
    BestOfALL_OX.append(custos[0])
    BestOfALL_CX.append(custos[1])
    BestOfALL_PMX.append(custos[2])
    BestOfALL_EX.append(custos[3])
    BestOfALL_SbR.append(custos[4])
    
    print "\n\n\nResultados totais do OX"
    for elem in BestOfALL_OX:
        print " -",elem,
    print "\n\n\nResultados totais do CX"
    for elem in BestOfALL_CX:
        print " -",elem,
    print "\n\n\nResultados totais do PMX"
    for elem in BestOfALL_PMX:
        print " -",elem,
    print "\n\n\nResultados totais do EX"
    for elem in BestOfALL_EX:
        print " -",elem,
    print "\n\n\nResultados totais do SbR"
    for elem in BestOfALL_SbR:
        print " -",elem,
    
def show_resultados(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa, Pedidos, Distancias, Optimo):
    BestsFinais = []
    cargasFinais = []
    custosFinais = []
    
    BestsFinais.append(BestsOX[len(BestsOX)-1])
    cargasOX = verificarCarga(BestsOX[len(BestsOX)-1][0], Pedidos)
    cargasFinais.append(cargasOX)
    custosFinais.append(BestsFinais[0][0])
    
    BestsFinais.append(BestsCX[len(BestsCX)-1])
    cargasCX = verificarCarga(BestsCX[len(BestsCX)-1][0], Pedidos)
    cargasFinais.append(cargasCX)
    custosFinais.append(BestsFinais[1][0])
    
    BestsFinais.append(BestsPMX[len(BestsPMX)-1])
    cargasPMX = verificarCarga(BestsPMX[len(BestsPMX)-1][0], Pedidos)
    cargasFinais.append(cargasPMX)
    custosFinais.append(BestsFinais[2][0])
    
    BestsFinais.append(BestsEX[len(BestsEX)-1])
    cargasEX = verificarCarga(BestsEX[len(BestsEX)-1][0], Pedidos)
    cargasFinais.append(cargasEX)
    custosFinais.append(BestsFinais[3][0])
    
    BestsFinais.append(BestsSbR[len(BestsEX)-1])
    cargasSbR = verificarCarga(BestsSbR[len(BestsSbR)-1][0], Pedidos)
    cargasFinais.append(cargasSbR)
    custosFinais.append(BestsFinais[4][0])
    
    custos = calcular_custoViagens(Distancias, custosFinais)
    
    print "\n\nCusto Optimo conhecido: ",Optimo
    print "Bests e suas cargas do varios algoritmos:"
    print "BestOX: ",BestsFinais[0]
    print "BestOX cargas: ",cargasFinais[0]
    print "BestOX custo percursos: ",custos[0]
    print "BestsCX: ",BestsFinais[1]
    print "BestsCX cargas: ",cargasFinais[1]
    print "BestsCX custo percursos: ",custos[1]
    print "BestsPMX: ",BestsFinais[2]
    print "BestsPMX cargas: ",cargasFinais[2]
    print "BestsPMX custo percursos: ",custos[2]
    print "BestsEX: ",BestsFinais[3]
    print "BestsEX cargas: ",cargasFinais[3]
    print "BestsEX custo percursos: ",custos[3]
    print "BestsSbR: ",BestsFinais[4]
    print "BestsSbR cargas: ",cargasFinais[4]
    print "BestsSbR custo percursos: ",custos[4]
    
def print_Graficos(ax, percursos, texto):
    cores = ['r','g','b','g','c','y','m','k']
    pontoInit = percursos[0][0]
    xPontoInit = pontoInit[0]
    yPontoInit = pontoInit[1]
    for i in range(len(percursos)):
        xOX = [row[0] for row in percursos[i]]
        yOX = [row[1] for row in percursos[i]]
        cor = randint(0,len(cores)-1)
        c = cores[cor]
        cores.remove(c)
        ax.plot(xOX, yOX, color=c, label="Truck"+str(i+1))
    ax.plot(xPontoInit, yPontoInit, "o", label=texto)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=3, fancybox=True, shadow=True)
    

def show_compare_results(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa, Pedidos, Distancias, Optimo, Test):
    
    #mostrar os resultados finais...
    show_resultados(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa, Pedidos, Distancias, Optimo)
    
    #tratar dos percursos...
    percursos = criarPercursos(BestsOX, BestsCX, BestsPMX, BestsEX, BestsSbR, Mapa)
    #===========================================================================
    # for elem in percursos:
    #     print "Percursos:"
    #     for elem2 in elem:
    #         print " - Percurso:",elem2
    #===========================================================================
     
    fig = plt.figure()
    #tratar do grafico com as historias dos bests
    fig.subplots_adjust(hspace=.5) 
    
    ax = fig.add_subplot(3,2,1) # two rows, two column, first plot
    #ax.xlabel('Numero da Geracao')
    #ax.ylabel('Valor do Best')
    historicoOX = []
    for elem in BestsOX:
        historicoOX.append(elem[1])
    historicoCX = []
    for elem in BestsCX:
        historicoCX.append(elem[1])
    historicoPMX = []
    for elem in BestsPMX:
        historicoPMX.append(elem[1])
    historicoEX = []
    for elem in BestsEX:
        historicoEX.append(elem[1])
    historicoSbR = []
    for elem in BestsSbR:
        historicoSbR.append(elem[1])
    
    ax.plot(historicoOX, color="r", label="Ordered CrossOver")
    ax.plot(historicoCX, color="g", label="Cyclic crossover")
    ax.plot(historicoPMX, color="b", label="Partially-matched crossover")
    ax.plot(historicoEX, color="y", label="Edges crossover")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=3, fancybox=True, shadow=True)
    
    #OX
    ax2 = fig.add_subplot(3,2,2)
    print_Graficos(ax2, percursos[0],"Ordered CrossOver")
    print_Mapa(ax2, Mapa, Pedidos)
    
    #CX
    ax3 = fig.add_subplot(3,2,3)
    print_Graficos(ax3, percursos[1],"Cyclic crossover")
    print_Mapa(ax3, Mapa, Pedidos)
    
    #PMX
    ax4 = fig.add_subplot(3,2,4)
    print_Graficos(ax4, percursos[2],"Partially-matched crossover")
    print_Mapa(ax4, Mapa, Pedidos)
        
    #EX
    ax5 = fig.add_subplot(3,2,5)
    print_Graficos(ax5, percursos[3],"Edges crossover")
    print_Mapa(ax5, Mapa, Pedidos)
    
    #SbR
    ax6 = fig.add_subplot(3,2,6)
    print_Graficos(ax6, percursos[4],"Geometric crossover")
    print_Mapa(ax6, Mapa, Pedidos)
    
    #show tudo...
    pyplot.show()
    #or save the figure
    #savefig("Teste_"+str(Test)+".png")
