# importamos las librerias necesarias
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
import time
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import apriori

# dataset de prueba
dataset = [{'a','b','c'},{'a','b','c','d'},{'b','c','e'},{'a','c','d','e'},{'d','e'}]

# convetrtimos al formato necesario para aplicar lso algoritmos
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)

# con fpgrowth o apriori sacamos los itemsets frecuentes
frequent = apriori(df, min_support=0.04, use_colnames=True)
# frequent = fpgrowth(df, min_support=0.04, use_colnames=True)

# creamos una lista con los valores unique de todos los soportes de los itemsets
su = frequent.support.unique()

# en este diccionario alamcenamos todos los itemsets que tienen el mismo support juntos
# la llave seria el valor unique de support que se saca del su
dicEqualSupports = {}

# recorremos y agregamso a al key correspondiende los itemsets segun el support
for i in range(len(su)):
    # buscamos aquellos itemsets que tienen el mismo support y los agrupamos bajo una misma llave
    inset = list(frequent.loc[frequent.support ==su[i]]['itemsets'])

    # alamcenamos la lista de itemsets de mismo support en el diccionario
    dicEqualSupports[su[i]] = inset

# lista con los itemsets cerrados finales
itemsetsCerrados = []

# recorremos todos los itemsets frecuentes
for index, row in frequent.iterrows():

    # boolerano que controla si es cerrado o no
    esCerrado = True

    # sacamos el itemset actual
    itemset = row['itemsets']

    # sacamos el soporte del itemset actual
    itemsetSupport = row['support']

    # del diccionario sacamos la lista de itemsets con los cuales revisar si es un superconjunto
    itemesetMismoSupport = dicEqualSupports[itemsetSupport]

    # recorremos la lista con los itemsets que tienen el mismo soporte y de los cuales hay que revisar si son superconjuntos
    for i in itemesetMismoSupport:
        # ignoramos los casos donde se compare el itemset con el mismo
        if (itemset!=i):

            # como la lista itemesetMismoSupport tiene itemsets con el mismo soporte
            # es suficiente con verificar si uno es subset del otro
            # si si lo es entonces no es un itemset cerrado
            if(frozenset.issubset(itemset,i)):
                esCerrado = False
                break
    
    # si la variable de control es true, agregamos el itemset a la lista de itemsets cerrados
    if(esCerrado):
        itemsetsCerrados.append(row['itemsets'])

# printeamos los resultados
print(f"Itemset base: ")
for i in dataset:
    print(i)
print()

print(f"Itemsets frecuentes: ")
for index, row in frequent.iterrows():
    print(list(row['itemsets']))
print()

print("Itemsets cerrados del dataset")
for x in itemsetsCerrados:
    print(list(x))