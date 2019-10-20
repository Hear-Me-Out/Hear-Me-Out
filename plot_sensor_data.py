import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

labelled_data = np.load('Preprocessed_Data/labelled_data.npy')
cols = ['label', 'accx', 'accy', 'accz', 'gyrox', 'gyroy', 'gyroz', 'flex0', 'flex1', 'flex2', 'flex3', 'flex4']
lab_df = pd.DataFrame(labelled_data, columns=cols)
lab_df = lab_df.sort_values(by=['label'], ascending=True)

#plot each sensor data
for i in range(1,12):
    #get accelerometer x-axis data
    feat = []
    f = cols[i]
    for index,row in lab_df.iterrows():
        feat_r = []
        for j in row[f]:
            feat_r.append(j)
        feat.append(feat_r)
    feat_df = pd.DataFrame(feat)

    #plot data
    fig, ax = plt.subplots(figsize=(20,5))
    sns.heatmap(feat_df.T, ax=ax, cmap="Blues")
    plt.savefig('plots/Sensor Data/'+cols[i]+'.png',bbox_inches='tight')
    print("Saved", f, "data")
