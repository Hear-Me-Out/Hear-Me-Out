'''
Collect sensor data from the glove at sampling_rate
'''
import Adafruit_BluefruitLE
from utils import SensorDataStream
from Adafruit_BluefruitLE.services import UART
import time
import datetime
import csv
import numpy as np

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

    #offset for the IMU
    offset = [588, 228, -370, -270, 104, -50, 0,0,0,0,0]
    #offset = [0,0,0,0,0,0,0,0,0,0,0]

    try:
        sd = SensorDataStream(UART,device)
        sd.start()

        labels = [  "good", "morning", "afternoon", "we_are", "from",
                    "R", "I", "T", "kottayam", "thank_you", "this_is",
                    "our", "project", "coffee", "idli", "sambhar",
                    "water", "how_are", "you", "i_am",  "please",
                    "sorry", "want", "where_is", "railway_station", "dosa" ]

        #get sample size
        print "Enter sample size: ",
        sample_size = input()

        for label in labels:
            s = sample_size
            print label
            print "Start collecting data(y/n) ",
            a = raw_input().lower()
            if a == 'y':
                time.sleep(2)

                #get data from device
                while s:
                    print "[START ACTION]"
                    count = 50
                    row = []
                    while count:
                        received = sd.read()
                        data = []
                        if received is not None:
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

                    #Uncomment For getting Offsets for Calibration--
                    import pandas as pd
                    df = pd.DataFrame(row, columns=np.arange(11))
                    print(df.mean())

                    print "Save Data?(y/n)",
                    #print(row)
                    a = raw_input().lower()
                    if a == 'y':
                        s -= 1
                        tm = datetime.datetime.now()
                        tm = '-'.join(str(tm).split())
                        fname = "Training_Data/"+label+"-"+tm+".csv"
                        try:
                            with open(fname, 'w') as f:
                                writer = csv.writer(f)
                                for r in row:
                                    writer.writerow(r)
                            f.close()
                        except KeyError:
                            print("[Exit]")
                            break

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
