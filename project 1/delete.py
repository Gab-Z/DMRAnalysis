#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      anagh
#
# Created:     20/06/2019
# Copyright:   (c) anagh 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def counting_sort(array1, max_val):
2	    m = max_val + 1
3	    count = [0] * m
4
5	    for a in array1:
6	    # count occurences
7	        count[a] += 1
8	    i = 0
9	    for a in range(m):
10	        for c in range(count[a]):
11	            array1[i] = a
12	            i += 1
13	    return array1


#arrondissement=df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION","TYPE"]).mean()
#print(df.groupby(["ARRONDISSEMENT","ANNEE DECLARATION"]).count())
#print(df.groupby(["MOIS DECLARATION","ANNEE DECLARATION"]).count())
#print(df.groupby("ANNEE DECLARATION").count())
#print(df.groupby("MOIS DECLARATION").count())