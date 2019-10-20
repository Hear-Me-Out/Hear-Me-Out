'''
Collect sensor data from the glove at sampling_rate
'''
import Adafruit_BluefruitLE
from utils import SensorDataStream
from utils import TTS
import traceback
from Adafruit_BluefruitLE.services import UART
import time
import datetime
import csv
import numpy as np
import pandas as pd
from keras import optimizers
from keras.models import model_from_json
from calibrate import *
'''
import tensorflow as tf
global graph
graph = tf.get_default_graph()
'''

ble = Adafruit_BluefruitLE.get_provider()
rate = 0.02

def connectDevice():
    '''
    Connects to the Adafruit Bluefruit Module and return the object for that device
    '''
    #clear any cached data
    ble.clear_cached_data()
    #get BLE adapter
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print("[ Using adapter: {0} ]".format(adapter.name))

    #disconnet any connected UART devices
    UART.disconnect_devices()

    #scan for UART devices
    print("Scanning for UART devices...")
    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError("Failed to find any UART device!")
    finally:
        adapter.stop_scan()

    print("Connecting to device...")
    device.connect()
    return device

def readData():
    '''
    Reads sensor data from the Bluefruit module at the sampling rate
    '''
    device = connectDevice()

    #load model 0
    json_file = open('Model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("Model/model.h5")
    print("Loaded model from disk")
    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])

    labels = np.load("Preprocessed_Data/labels_list.npy")
    offset = [-1052, -1164, -264, -154, 165, 212, 0, 0, 0, 0, 0]

    try:
        sd = SensorDataStream(UART,device)
        tts = TTS()
        sd.start()
    except:
        pass
    print "[WAITING FOR SYNCHRONIZATION]"
    while(not sd.ready()):
        pass
    print "[DONE]"

    #main loop
    try:

        print "Start collecting data(y/n) ",
        a = raw_input().lower()

        while a=='y':
            #time.sleep(2)
            print "[START ACTION]"
            count = 50
            row = []
            while count:
                received = sd.read()
                data = []
                if received != '':
                    #split into the three segments
                    received = received.split('#')
                    #don't know why but splitting the string adds null character to the ends, so remove those too
                    received = list(map(lambda x: x.rstrip('\x00'), received))

                    #convert from string to list of values
                    for item in received:
                        data.extend(item[1:].split(','))

                    #convert each element in the list from str to int
                    data = list(map(int,data))

                    #adjust the offset
                    data = list(np.subtract(data,offset))

                    row.append(data)
                    print(data)
                    #writer.writerow(row)

                else:
                    print("Received no data!")
                time.sleep(rate)
                count -= 1

            #normalize data
            min_val_acc_gyro = [-32768]*6
            min_val_flex = [340]*5
            row.append(min_val_acc_gyro + min_val_flex)
            max_val_acc_gyro = [32768]*6
            max_val_flex = [610]*5
            row.append(max_val_acc_gyro + max_val_flex)

            df = pd.DataFrame(row, columns=np.arange(11))
            #scale acc and gyro values between -1 and 1
            for j in range(6):
                df[j] = df.apply(lambda x:(2*(x.astype(float) - min(x))/(max(x)-min(x)))-1)[j]

            #scale flex sensor values between 0 to 1
            for j in range(6,11):
                df[j] = df.apply(lambda x:(x.astype(float) - min(x))/(max(x)-min(x)))[j]
            df = df[:-2]

            inp = np.array(df.values)
            inp = inp.reshape((1,50,11))

            #predict input label
            prediction = loaded_model.predict(inp)
            pred = list(prediction[0])
            #print(pred)
            p = max(pred)
            i = pred.index(p)
            pred_label = labels[i]
            print(p, i, pred_label)
            if p>=0.7:
                tts.say(pred_label)
            #print("Start Next sign? (y/n)")
            #a = raw_input().lower()

    finally:
        device.disconnect()

def main():
    '''
    Main function
    '''
    ble.initialize()
    ble.run_mainloop_with(readData)

if __name__ == "__main__":
    main()
