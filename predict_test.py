import numpy as np
import pandas as pd
from keras import optimizers
from keras.models import model_from_json

#load model
json_file = open('Model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("Model/model.h5")
print("Loaded model from disk")

#load test data and labels
test_data = np.load('Preprocessed_Data/test_data.npy')
test_label = np.load('Preprocessed_Data/test_label.npy')
labels =np.load('Preprocessed_Data/labels_list.npy')

#load val data and labels
val_data = np.load('Preprocessed_Data/val_data.npy')
val_label = np.load('Preprocessed_Data/val_label.npy')

test_data =  np.concatenate((test_data, val_data), axis=0)
test_label =  np.concatenate((test_label, val_label), axis=0)

loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
loss, accuracy = loaded_model.evaluate(test_data, test_label)
print(loss, accuracy)

predictions = loaded_model.predict(test_data)
l = len(predictions)
pred_matrix = []
for i in range(l):
    pred = list(predictions[i])
    act_label = labels[list(test_label[i]).index(1)]
    p = max(pred)
    i = pred.index(p)
    pred_label = labels[i]
    if(pred_label==act_label):
        print(pred_label, p, act_label)
    else:
        print("********", pred_label, p, act_label, "********")
    mat_row = pred+[act_label]
    pred_matrix.append(mat_row)

import matplotlib.pyplot as plt
import seaborn as sns
col = list(labels)+["Actual labels"]
df_pm = pd.DataFrame(pred_matrix, columns=col)
#group by actual labels and take mean
df_pm = df_pm.groupby(["Actual labels"]).mean()
df_pm = df_pm.reindex(index=df_pm.index[::-1])
df_pm = df_pm.round(3).mul(100)
print(df_pm)
plt.figure(figsize=(12,12))

ax1 = sns.heatmap(df_pm, annot=True, cmap="Blues", fmt='g')
ax1.tick_params(axis = 'both', which = 'major', labelsize = 14)
ax1.set_xlabel("Predicted Labels", labelpad=10).set_fontsize(17)
ax1.set_ylabel("Actual Labels", labelpad=10).set_fontsize(17)
plt.savefig('plots/confusion_matrix.png',bbox_inches='tight')
