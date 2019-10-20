import pyttsx
from threading import Thread
import time

class TTS():
    def __init__(self,rate = 130, volume = 1):
        self.rate = rate
        self.volume = volume
        self.name = "tts"

    def say(self, text):
        self.voiceEngine = pyttsx.init()
        self.voiceEngine.setProperty('rate',self.rate)
        self.voiceEngine.setProperty('volume',self.volume)
        self.voiceEngine.say(text)
        a = self.voiceEngine.runAndWait()
        self.voiceEngine = ""
