import tensorflow as tf
import pickle
import numpy as np

PATH = "model.tf"

f = open("dataset.pkl", "rb")
dataset = pickle.load(f)
f.close()

X = []
Y = []
for i in range(len(dataset)):
    X.append(dataset[i][0])
    Y.append(dataset[i][1])

X = tf.constant(np.array(X))
Y = tf.constant(Y)

def train():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.Input(shape=(81,)))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(86, activation='relu'))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(32))
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, Y, epochs=200)
    model.save(PATH)

def evaluate():
    model = tf.keras.models.load_model(PATH)
    res = model.predict(X[0:1])
    print("result = ", res, "it is supposed to be ", Y[0:1])

evaluate()