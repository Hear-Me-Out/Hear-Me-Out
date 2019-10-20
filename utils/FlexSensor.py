# import the necessary packages
from threading import Thread
import serial
import time
from datetime import datetime

class SensorDataStream:
	def __init__(self, UART, device, name="SensorDataStream"):
		self.name = name
		self.stopped = False
		self.buffer = ""
		self.acc = ""
		self.gyro = ""
		self.flex = ""
		self.is_ready = False
		self.UART = UART
		self.device = device
		

	def start(self):
		print("Discovering Services...")
		self.UART.discover(self.device)
		print("[Service Discovered]")
		uart = self.UART(self.device)
		uart.write('')
		# start the thread to read data from the sensor
		t = Thread(target=self.update, name=self.name, args=(uart,))
		t.daemon = True
		t.start()
		return self

	def update(self,uart):
		# keep looping infinitely until the thread is stopped
		while True:
			acc = uart.read(timeout_sec=10)
			if acc is not None and acc[0] == 'A':
				gyro = uart.read(timeout_sec=10)
				if gyro is not None and gyro[0] == 'G':	
					flex = uart.read(timeout_sec =10)
					if flex is not None and flex[0] == 'F':
						self.acc = acc
						self.gyro = gyro
						self.flex = flex
						temp = "#".join([acc,gyro,flex])
						self.buffer = temp
						self.is_ready = True
						#print(self.buffer)

	def read(self):
		# return the data most recently read
		return self.buffer
	
	def ready(self):
		# return true if the readings are ready
		return self.is_ready
	
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		print("[EXIT!]")
		self.device.disconnect()
