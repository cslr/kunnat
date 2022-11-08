#!/usr/bin/python3

import csv
import numpy

import math

from sklearn import linear_model


######################################################################
# ETL / preprocess data

csvDataFile = open('Kuntien_avainluvut_20221108-aikasarja.csv')
csvReader = csv.reader(csvDataFile, delimiter='\t')

headers = next(csvReader)
headers = [];

data = {}

counter = 0
first_time = True
for row in csvReader:

    if(counter == 0):
        name = row[0];
        data[row[0]] = numpy.ndarray((22,32));

    for i in range(len(row)-2):
        if(row[i+2] != '..'):
            data[row[0]][i, counter] = float(row[i+2])
        else:
            data[row[0]][i, counter] = None # nan in practice

    if(first_time):
        headers.append(row[1])
    
#    print(row)
    counter = counter + 1

    if(counter >= 32):
        counter = 0
        first_time = False

######################################################################        
# next computes (x,y=delta_x) values for learning linear model

X = []
Y = []

for name, value in data.items():
#    print(name)

    (ysize,xsize) = value.shape


    for j in range(ysize-1):
        
        hasNAN = False

        for i in range(xsize):
            if(math.isnan(value[j,i])):
                hasNAN = True
        
        for i in range(xsize):
            if(math.isnan(value[j+1,i])):
                hasNAN = True

        if(hasNAN == False):
            x = value[j, :]
            y = value[j+1,:] - value[j,:]

            X.append(x);
            Y.append(y);

print(len(X))

regr = linear_model.LinearRegression(fit_intercept=False);
regr.fit(X,Y)

A = numpy.array(regr.coef_)
b = numpy.array(regr.intercept_)

print(A)
print(b)
print(len(A))
print(len(A[0]))


### NOW WE HAVE MODEL delta_x = A*x

# generate target_delta vector and load x0 initial conditions vector

target_delta = numpy.zeros(Y[0].shape)
target_delta[17] = +5.0 # increase työllisyysaste/employment rate 5%

x0 = data['Mikkeli'][20,:] # previous year 2020

print(target_delta)
print(x0)


# now we need to solve for linear equation:
# delta = pinv(A^t*A) * A^T * target_delta - x0

At = A.transpose()
AtA = numpy.matmul(At,A)
invAtA = numpy.linalg.inv(AtA)
M = numpy.matmul(invAtA, At)

# delta = M*target_delta - x0

delta = numpy.matmul(M, target_delta) - x0

MM = numpy.linalg.inv(A)
delta2 = numpy.matmul(MM, target_delta)



print("VALUES:")

print(delta)
print(x0)

ratio = delta / x0

print(ratio)

# transforms to log-scale
for i in range(len(ratio)):
    if(ratio[i] < 0.0):
        ratio[i] = -math.log(abs(ratio[i]))
    else:
        ratio[i] = math.log(abs(ratio[i]))

print(headers)


######################################################################
# plots bar-figure (first solution)

import matplotlib.pyplot as plt
from textwrap import wrap


headers = [ '\n'.join(wrap(l,12)) for l in headers]


fig = plt.figure(figsize=(20,10))

plt.bar(headers[1:16], ratio[1:16], color='blue', width=0.4)

plt.title('Maksimoi työllisyyden');
plt.show()

plt.savefig('optimal_control-1.png')

fig = plt.figure(figsize=(20,10))

plt.bar(headers[17:32], ratio[17:32], color='blue', width=0.4)

plt.title('Maksimoi työllisyyden');
plt.show()

plt.savefig('optimal_control-2.png')


######################################################################
# plots bar-figure (2nd solution)

ratio2 = delta2 / x0

# transforms to log-scale
for i in range(len(ratio2)):
    if(ratio2[i] < 0.0):
        ratio2[i] = -math.log(abs(ratio2[i]))
    else:
        ratio2[i] = math.log(abs(ratio2[i]))
    


fig = plt.figure(figsize=(20,10))

plt.bar(headers[1:16], ratio2[1:16], color='blue', width=0.4)

plt.title('Maksimoi työllisyyden');
plt.show()

plt.savefig('better_optimal_control-1.png')

fig = plt.figure(figsize=(20,10))

plt.bar(headers[17:32], ratio2[17:32], color='blue', width=0.4)

plt.title('Maksimoi työllisyyden');
plt.show()

plt.savefig('better_optimal_control-2.png')
