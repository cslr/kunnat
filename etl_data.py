#!/usr/bin/python3

import csv
import numpy

import math

import dwavebinarycsp
import dwave.inspector
import dimod
import random
from dwave.system import EmbeddingComposite, DWaveSampler, LeapHybridDQMSampler
from dimod import DiscreteQuadraticModel

############################################################
## ETL / preprocessing of municipalities data

csvDataFile = open('kta_20210327-131158.csv')
csvReader = csv.reader(csvDataFile, delimiter=';')

headers = next(csvReader)
headers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
data_num = 0;
data_elem = 0
data = numpy.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14])
xdata = numpy.array([[1,2,3,4,5,6,7,8,9,10,11,12,13,14]])

for row in csvReader:
    data[data_elem] = float(row[2])
    if(data_num == 0):
        headers[data_elem] = row[1]

    data_elem = data_elem + 1
    if(data_elem >= 14):
        xdata = numpy.append(xdata, [data], 0)
        data_elem = 0
        data_num += 1

xdata = numpy.delete(xdata, [0], 0)

# swap 1st and 3rd row with each other
xdata[:,[0,2]] = xdata[:,[2,0]]
tmp = headers[0]
headers[0] = headers[2]
headers[2] = tmp

print(headers)
print(xdata)

# data is now numpy array, first element is the target value
# next: discretizes other 13 fields into 1 bin indicator variables (smaller or larger than mean)

ddata = xdata

mean = numpy.mean(xdata, 0)
stdev = numpy.std(xdata, 0)

rows, cols = xdata.shape

print("{} rows and {} cols of data".format(rows, cols))

print(mean)

######################################################################
# next calculates E[Y|x_j,x_i] used for optimization, we discretize variables
# to N BINS: (2*sigma/(N/2) = tick length) except the first one which will be target variable

BINS = 6

for row in range(rows):
    for col in range(1,cols):
        bin = int((xdata[row][col]-mean[col])/(2*stdev[col]/(BINS/2)))
        bin = bin + BINS
        if(bin >= BINS):
            bin = BINS-1
        if(bin <= 0):
            bin = 0
        ddata[row][col] = bin; # discrete variable between 0...(BIN-1)

print(ddata)


EY = {}

# negative sign to maximize target (we minimize model energy)
for k in range(BINS):
    for l in range(BINS):
        for i in range(1, cols):
            for j in range(1, cols):
                EY[(i,k,j,l)] = 0.0
                for r in range(rows):
                    if(ddata[r][i] == k and ddata[r][j] == l):
                        EY[(i,k,j,l)] = EY[(i,k,j,l)] - ddata[r][0]/rows


# We minimize E[Y] so we use negative sign to actually maximize E[Y]
print(EY)

#####################################################################
## D-WAVE sampler solver part

# now transform E[Y|x_j,x_i] data to Ising model Jji, hj parameters
# UPDATE: We use BQM model so we can use E[Y|x_j,x_i] values directly

dqm = dimod.DiscreteQuadraticModel()

for p in range(1,len(headers)):
    dqm.add_variable(BINS, label=headers[p])

for p0 in range(1,len(headers)):
    for p1 in range(1, p0):
        v0 = headers[p0]
        v1 = headers[p1]

        EYmap = {}
        for k in range(BINS):
            for l in range(BINS): # BINS
                EYmap[(k,l)] = EY[(p0,k,p1,l)]

        dqm.set_quadratic(v0, v1, EYmap)


print("Sampling model..")

sampler = LeapHybridDQMSampler()

sampleset = sampler.sample_dqm(dqm, label='Municipalities best income')

#sampler = EmbeddingComposite(DWaveSampler())
#sampleset = sampler.sample(bqm,
#                           chain_strength=4,
#                           num_reads=1000,
#                           label='BQM/Ising model test')

best_sample = sampleset.first.sample
best_energy = sampleset.first.energy

print(best_sample, headers[0], -best_energy)





