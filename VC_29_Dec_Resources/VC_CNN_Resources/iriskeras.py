# -*- coding: utf-8 -*-
"""IrisKeras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HHUcgHxCXtuQkzcuoENiWmfQjxkAXIiF

### Step 1: Importing important libraries. *Numpy:* Linear Algebra and manipulation of data. *Keras:* High-level API built on top of Tensorflow. *SKLearn:* Machine Learning libraries that holds datasets, models and other useful functions.
"""

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn.datasets import load_iris
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

"""## *Problem statement: Given the dimensions of petal and sepal, can we predict the species of Iris?*
### Classification Problem: 3 Classes = Setosa, Versicolor and Virginica. Total number of samples: 150 (50 in each class).

![alt text](https://thegoodpython.com/assets/images/iris-species.png)

### Step 2: Loading and visualizing the data.* Seaborn:* Data Visualization library built on top of Matplotlib
### **Class 0:** Setosa **Class 1:** Versicolor **Class 2:** Virginica
"""

import seaborn as sb
import matplotlib.pyplot as plt
iris = load_iris()
iris_x = iris.data
iris_y = iris.target
#(Sepal Length, Sepal Width, Petal Length, Petal Width)in centimeters
print("Example of iris_x = {}".format(iris_x[0]))
#(Target Class)
print("Example of iris_y = {}".format(iris_y[0]))

sb.pairplot(sb.load_dataset("iris"),hue='species')

#Converting class vector from row vector to column vector
print(iris_y.shape)
iris_y = iris_y.reshape(-1,1)
print(iris_y.shape)
print(iris_x.shape)

"""### Step 3: Building the model"""

#encoding the classes
iris_ye = OneHotEncoder(sparse=False).fit_transform(iris_y)
train_x,test_x,train_y,test_y = train_test_split(iris_x,iris_ye,test_size=0.2)

iris_m = Sequential()
iris_m.add(Dense(4,input_shape=(4,),activation='relu',name='Layer'))
iris_m.add(Dense(5,activation='relu',name='HiddenLayer'))
iris_m.add(Dense(3,activation='softmax',name='Output'))

iris_m.compile(optimizer=Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])

iris_m.summary()

keras.utils.plot_model(iris_m)

"""### Step 4: Training the model"""

history = iris_m.fit(train_x,train_y,verbose=1,batch_size=5,epochs=500)

"""Step 5: Evaluating the model on unseen data (Test set)"""

results = iris_m.evaluate(test_x,test_y)

print('Test Loss = {}'.format(results[0]))
print('Test Accuracy = {}'.format(results[1]))

from sklearn.metrics import classification_report,confusion_matrix
pred_y = iris_m.predict(test_x)
pred_yl = np.argmax(pred_y,axis=1)
test_yl = np.argmax(test_y,axis=1)
print(classification_report(test_yl,pred_yl))
print(confusion_matrix(test_yl,pred_yl))

plt.xlim(0,500)
plt.ylim(0.0,1.0)
plt.plot(history.history['acc'])
plt.plot(history.history['loss'])
plt.title('Model Metrics')
plt.ylabel('Accuracy/Loss')
plt.xlabel('Epoch')
plt.legend(['ACC', 'LOSS'], loc='upper left')
plt.show()
