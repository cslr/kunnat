#!/usr/bin/python3

import csv
import numpy

import math

import dwavebinarycsp
import dwave.inspector
import dimod
import random
from dwave.system import EmbeddingComposite, DWaveSampler

############################################################
## ETL / preprocessing of municipalities data

MAX = 20 # 14

# csvDataFile = open('kta_20210327-131158.csv')
csvDataFile = open('kta_20210329-165303.csv')
csvReader = csv.reader(csvDataFile, delimiter=';')

header = next(csvReader)
data_num = 0;
data_elem = 0
data = numpy.array(list(range(1,MAX+1)))
xdata = numpy.array([list(range(1,MAX+1))])
header = list(range(1,MAX+1))

for row in csvReader:
    print("{} {} element".format(data_elem, data_num))
#    print(row)
#    print(row[2])
    if(row[2] == '.'):
        row[2] = 0.0
    data[data_elem] = float(row[2])
#    xdata[data_num][data_elem] = row[2]
    if(data_num == 0):
        header[data_elem] = row[1]

    data_elem = data_elem + 1
    if(data_elem >= MAX):
        xdata = numpy.append(xdata, [data], 0)
        data_elem = 0
        data_num += 1

xdata = numpy.delete(xdata, [0], 0)

# swap 1st and 3rd row with each other
xdata[:,[0,2]] = xdata[:,[2,0]]
tmp = header[0]
header[0] = header[2]
header[2] = tmp

print(header)
print(xdata)


# data is now numpy array, first element is the target value
# next: discretizes other 13 fields into 1 bin indicator variables (smaller or larger than mean)

ddata = xdata

mean = numpy.mean(xdata, 0)

rows, cols = xdata.shape

print("{} rows and {} cols of data".format(rows, cols))

print(mean)

for row in range(rows):
    for col in range(1,cols):
        ddata[row][col] = xdata[row][col] > mean[col]

print(ddata)

######################################################################
# next calculates E[Y|x_j,x_i] used for optimization 

EY = {}

for j in range(1,cols):
    for i in range(j+1, cols):
        EY[(j,i)] = 0.0


for j in range(1,cols):
    for i in range(j+1, cols):
        for r in range(rows):
            if(abs(ddata[r][i]*ddata[r][j]) > 0):
                EY[(j,i)] = EY[(j,i)] - ddata[r][0]
        EY[(j,i)] = EY[(j,i)] / rows


# We minimize E[Y] so we use negative sign to actually maximize E[Y]
print(EY)

#####################################################################
## D-WAVE sampler solver part

## exit()

# now transform E[Y|x_j,x_i] data to Ising model Jji, hj parameters
# UPDATE: We use BQM model so we can use E[Y|x_j,x_i] values directly

ai = {}

bqm = dimod.BinaryQuadraticModel(ai, EY, 0.0, dimod.Vartype.BINARY)

print("Sampling model..")

sampler = EmbeddingComposite(DWaveSampler())
sampleset = sampler.sample(bqm,
                           chain_strength=4,
                           num_reads=1000,
                           label='BQM/Ising model test')

best_sample = sampleset.first.sample

print(best_sample)



