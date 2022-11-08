#!/usr/bin/python3

import csv
import numpy

import math

from sklearn.linear_model import LinearRegression


#import dwavebinarycsp
#import dwave.inspector
#import dimod
#import random
#from dwave.system import EmbeddingComposite, DWaveSampler, LeapHybridDQMSampler
#from dimod import DiscreteQuadraticModel

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

xdata = xdata.astype('float')


# save xdata and headers to file
csvfile = open('etl_data.csv', 'w', newline='')

csvwriter = csv.writer(csvfile, delimiter=',')
csvwriter.writerow(headers)

for i in range(len(xdata[:,1])):
    csvwriter.writerow(xdata[i,:])
    
csvfile.close()




mean = numpy.mean(xdata, 0)
stdev = numpy.std(xdata, 0)

for i in range(len(xdata[1,:])):
    for j in range(len(xdata[:,i])):
        xdata[j,i] = float(xdata[j,i] - mean[i])/float(stdev[i])
    

mean = numpy.mean(xdata, 0)
stdev = numpy.std(xdata, 0)

print(mean)
print(stdev)


rows, cols = xdata.shape

print("{} rows and {} cols of data".format(rows, cols))

print(mean)

x = xdata[:,1:14]
y = xdata[:,0]



print(x)
print(y)

model = LinearRegression().fit(x,y)

print(headers[1:14])
print(model.coef_)

head = headers[1:14]


# plots bar-figure

import matplotlib.pyplot as plt
from textwrap import wrap


head = [ '\n'.join(wrap(l,12)) for l in head]


fig = plt.figure(figsize=(20,10))

plt.bar(head, model.coef_, color='maroon', width=0.4)

plt.title('Vaikutus verotuloihin');
plt.show()

plt.savefig('regression_results.png')

