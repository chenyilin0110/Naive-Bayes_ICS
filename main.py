from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from torch.autograd import Variable
import torch.optim as optim
import torch.nn as nn
import torch
import numpy as np
import sys
import preprocess
import accuracyfunction
# import matplotlib.pyplot as plt
#import seaborn as sns

# set filename outputLayer testing iteration
finder = sys.argv[1]
filename = sys.argv[2]
outputLayer = sys.argv[3]
testing = sys.argv[4]
iteration = sys.argv[5]
number = sys.argv[6]

# load dataset
if finder == "multi":
    temp = np.loadtxt('dataset/multiclass/'+filename, dtype=np.str, delimiter=',')
elif int(finder) == 2:
    temp = np.loadtxt('dataset/2class/'+filename, dtype=np.str, delimiter=',')
elif int(finder) == 3:
    temp = np.loadtxt('dataset/3class/'+filename, dtype=np.str, delimiter=',')

if finder =="multi":
    noStringTemp = temp[0:,0:] 
else:
    noStringTemp = temp[1:,0:] #[欄,列] and clean top string

noStringTemp_X = noStringTemp[0:,0:-1]

# preprocess
noStringTemp_X = preprocess.missingValue(noStringTemp_X)
if finder != "multi":
    noStringTemp_Y = []
    noStringTemp_Y = preprocess.distinguishNaturalAttack(noStringTemp, noStringTemp_Y)
    # list->np
    noStringTemp_Y = np.array(noStringTemp_Y)    
else:
    noStringTemp_Y = noStringTemp[:,-1]    
    noStringTemp_Y = noStringTemp_Y.astype(int)
    # multiclass 1 to 41, but lossfunction from 0 begin
    for i in range(len(noStringTemp_Y)):
        noStringTemp_Y[i] -= 1

resultNormalize = preprocess.normalize(noStringTemp_X)

# build gaussian Naive Bayes
GaussianNaiveBayes = GaussianNB()

# split data
x_train, x_test, y_train, y_test = train_test_split(resultNormalize, noStringTemp_Y, test_size = float(testing)/100, random_state=42)

# training
GaussianNaiveBayesFit = GaussianNaiveBayes.fit(x_train, y_train)

# testing
y_test_prediction = GaussianNaiveBayes.predict(x_test)

print(int(number), " ", end='')
accuracyfunction.accuracy(y_test, y_test_prediction)