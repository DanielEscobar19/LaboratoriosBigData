import pandas as pd
from collections import Counter
from itertools import combinations

url = 'https://raw.githubusercontent.com/DanielEscobar19/LaboratoriosBigData/main/Laboratorio3/Sales_January_2019.csv'

# leemos el dataset
df = pd.read_csv(url)

# Agrupa los productos según su transacción (Order ID).
transacciones = df.groupby('Order ID')['Product'].apply(list).tolist()
transacciones = df.groupby('Order ID')['Product'].apply(list).reset_index().values.tolist()
transacciones = [[order_id, products] for order_id, products in transacciones]

# generamos una lista con los valores unique de los productos
itemset_1 = []
for transaccionActual in transacciones:
    for producto in transaccionActual[1]:
        if(producto not in itemset_1):
            itemset_1.append(producto)

# sorteamos el itemset de productos unicos
itemset_1 = sorted(itemset_1)

# soporte minimo que debe cumplir cada itemset
minSupport = 2
supportThreshold = minSupport/len(itemset_1)

# se cuentan las apariciones de cada valor del itemset
candidatos = Counter()
for producto in itemset_1:
    for transaccion in transacciones:
        if(producto in transaccion[1]):
            candidatos[producto] += 1

# mostramos la primera lista de candidatos
print("candidatos_1: ")
for i in candidatos:
    print(str([i])+": "+str(candidatos[i]))
print()

candidatosPodados = Counter()
for producto_soporte in candidatos:
    if(candidatos[producto_soporte] >= minSupport):
        candidatosPodados[frozenset([producto_soporte])]+=candidatos[producto_soporte]

# mostramos los candidatos podados
print("candidatos sin podados:")
for i in candidatosPodados:
    print(str(list(i))+": "+str(candidatosPodados[i]))
print()

# itemsets frecuenntes previos
itemsetsPrevios = candidatosPodados
podadasCantidad = 1

iteracion = 2
while True:
    # itemset por el que va la iteracion
    itemsetActual = set()

    # variable temporal para crear las combinaciones
    temporal = list(candidatosPodados)

    # creamos los subconjuntos no vacios de cada itemset
    for indexCandidato in range(0, len(temporal)):
        for indexCandidatoSiguiente in range(indexCandidato+1, len(temporal)):

            # recorre los candidatos y genera grupos del tamaño de la iteración
            unionTemporal = temporal[indexCandidato].union(temporal[indexCandidatoSiguiente])

            # agrega la union al itemset actual si es del tamaño de la iteracion
            if(len(unionTemporal) == iteracion):
                itemsetActual.add(unionTemporal)

    # convertimos a lista para poder iterar
    itemsetActual = list(itemsetActual)

    # candidatos actuales
    candidatos = Counter()

    # se cuentan las apariciones de cada valor del itemset
    for productos in itemsetActual:
        candidatos[productos] = 0
        for transaccion in transacciones:
            temporal = set(transaccion[1])
            if(productos.issubset(temporal)):
                candidatos[productos] += 1

    # mostramos la lista de candidatos actual
    print(f"Candidatos {str(iteracion)}:")
    for candidato in candidatos:
        # imprimimos el valor y la llave del diccionario canditatos
        print(f"{str(list(candidato))}: {str(candidatos[candidato])}")
    print()

    # candidatos luego de podar
    candidatosPodados = Counter()

    for candidato in candidatos:
        # la condicion poda los que no cumplen el soporte
        if(candidatos[candidato] >= minSupport):
            candidatosPodados[candidato] += candidatos[candidato]

    # imprimimos la lista de candidatos luego de ser podado
    print(f"Candidatos sin podados {str(iteracion)}:")
    for candidato in candidatosPodados:
        print(f"{str(list(candidato))} : {str(candidatosPodados[candidato])}")
    print()

    # si le itemset luego de podar esta vacio, detenemos el proceso
    if(len(candidatosPodados) == 0):
        break

    # asignamos el itemset previo para no perder el itemset final
    itemsetsPrevios = candidatosPodados
    podadasCantidad = iteracion

    # aumentamos las iteraciones para crear subsets mas grandes en la siguiente iteracion
    iteracion += 1

print(f"Resultado:\nCandidatos {str(podadasCantidad)}:")
for i in itemsetsPrevios:
    print(str(list(i))+": "+str(itemsetsPrevios[i]))
print()

######################### confianza minima para reglas de asociacion
confianzaMinima = 60;

print(f"Resultado reglas:")

def eliminarVacios(tuples):
    tuples = filter(None, tuples)
    return list(tuples)


# combinationsList contiene la lista de combinaciones del itemset actual
combinationsList = list()
for itemset in itemsetsPrevios:
    # creamos las combinaciones del itemset actual
    for i in range(len(itemset)):
        combinationsList += list(combinations(itemset, i))

    # combinationsList contiene la lista de combinaciones del itemset actual
    # eliminamos los conjuntos vacios 
    combinationsList = eliminarVacios(combinationsList)

    # para revisar lista de combinaciones actual
    # print(f"combinationsList {combinationsList}\n")

    # se cuentan las apariciones de cada valor del itemset
    # esto calcula los soportes
    soportes = Counter()
    for combinacion in combinationsList:
        for transaccion in transacciones:
            if(set(combinacion).issubset(set(transaccion[1]))):
                soportes[tuple(combinacion)] += 1

    # lista donde almacenar las reglas que cumplen un minimo de confianza
    reglasAsociacionFiltradas = list()

    for i in soportes:
        reglasAsociacionFiltradas.append(f'\nitemsetActual = {list(itemset)}')

        # formula vista en clase para las reglas de asociacion
        confianza = itemsetsPrevios[itemset]/soportes[i] * 100

        # string con regla de asociacion y su porcentaje
        regla = f'{list(i)} => {set(itemset)- set(i)}: supp({list(itemset)})/supp({str(list(i))}) == {itemsetsPrevios[itemset]}/{soportes[i]} = {confianza}%'

        # guardamos solo las que cumple con la confianza minima
        if (confianza >= confianzaMinima):
            reglasAsociacionFiltradas.append(f'{regla} Si cumple con la confianza minima ({confianzaMinima}%)')
        else:
            reglasAsociacionFiltradas.append(f'{regla} No cumple con la confianza minima ({confianzaMinima}%)')
    
    # print de los resultados ya filtrados
    for i in reglasAsociacionFiltradas:
        print(f"{i}")
    combinationsList.clear()
