import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Activation
from keras import optimizers
from keras.preprocessing import sequence
from keras.models import model_from_json

#load Training and Validation data
train_data = np.load('Preprocessed_Data/train_data.npy')
val_data = np.load('Preprocessed_Data/val_data.npy')
test_data = np.load('Preprocessed_Data/test_data.npy')

#load Training and Validation labels
train_label = np.load('Preprocessed_Data/train_label.npy')
val_label = np.load('Preprocessed_Data/val_label.npy')
test_label = np.load('Preprocessed_Data/test_label.npy')
labels =np.load('Preprocessed_Data/labels_list.npy')

model = Sequential([
  LSTM(50, input_shape=(50, 11)),
  Dense(100),
  Dropout(0.4),
  Dense(len(labels), activation='softmax'),
])
model.summary()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
hist = model.fit(train_data, train_label, validation_data = (val_data, val_label),
                batch_size=64, epochs=30)
loss, accuracy = model.evaluate(test_data, test_label)
print(loss, accuracy)

#save model
model_json = model.to_json()
with open("Model/model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("Model/model.h5")
print("Saved model to disk")

#Plot Loss and Accuracy Curves
import matplotlib.pyplot as plt
plt.figure(figsize=(12,8))
plt.subplot(211)
x = np.arange(1,len(hist.history['acc'])+1)
plt.scatter(x, hist.history['acc'], color='blue', s=10)
plt.plot(x,hist.history['acc'], 'b')
plt.scatter(x, hist.history['val_acc'], color='green', s=10)
plt.plot(x, hist.history['val_acc'], 'g')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.legend(['Training', 'Validation'], loc='lower right')

plt.subplot(212)
plt.scatter(x, hist.history['loss'], color='blue', s=10)
plt.plot(x,hist.history['loss'], 'b')
plt.scatter(x, hist.history['val_loss'], color='green', s=10)
plt.plot(x, hist.history['val_loss'], 'g')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training', 'Validation'], loc='upper right')
plt.savefig('plots/loss_acc_curves.png',bbox_inches='tight')
