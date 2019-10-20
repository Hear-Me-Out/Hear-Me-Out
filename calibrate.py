'''
Collect sensor data from the glove at sampling_rate
'''
import Adafruit_BluefruitLE
from utils import SensorDataStream
from utils import TTS
import traceback
from Adafruit_BluefruitLE.services import UART
import numpy as np
import pandas as pd
import time

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
    #offset = [-100, 802, -400, -268, 104, -45, 0,0,0,0,0]
    offset = [0,0,0,0,0,0,0,0,0,0,0]
    count = 0
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
    #calibrating glove
    try:
        row = []
        data = []
        received = sd.read()
        data = []

        if received != '':
                #split into the three segments
                received = received.split('#')
                #don't know why but splitting the string adds null character to the ends,
                #so remove those too
                received = list(map(lambda x: x.rstrip('\x00'), received))

                #convert from string to list of values
                for item in received:
                    data.extend(item[1:].split(','))

                #convert each element in the list from str to int
                data = list(map(int,data))

                row.append(data)
                #print(data)
                count += 1

        time.sleep(rate)

        df = pd.DataFrame(row, columns=np.arange(11))
        offset = list(df.mean())
        offset[2] -= 16384
        offset[-5:] = [0]*5
        offset = map(int,offset)
        print("Readings before offset: {}".format(data))
        data = list(np.subtract(data,offset))
        print("Readings after offset: {}".format(data))
        print "[CALIBRATED]"
        tts.say("calibrated glove")
        print(offset)
    except Exception as e:
        print data
        print traceback.format_exc()

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
