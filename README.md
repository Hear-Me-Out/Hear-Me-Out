# Hear Me Out
Hear Me Out is an attempt to translate Indian Sign Language(ISL) gestures to text and speech using a sensor glove. This repository contains the code for the complete project.

Watch the demo at : https://youtu.be/pjQJLYO3Ago

## What's Different?
So there have been a lot of attempts to translate ISL gestures to speech but most of them can only translate static signs and have limited intelligence. With the advent of deep learning, there is an opportunity to make the translation process smarter.

Unlike the existing approaches, our design is capable of translating both static and dynamic gestures without the need of training on individual users. 

## Method
![method](https://user-images.githubusercontent.com/15849927/67158758-b1ac2a80-f359-11e9-97b0-c14033502aed.png)
- ### Hardware
    We have used an Adafruit Bluefruit nRF52 as the main MCU. The light weight and BLE capability makes it best for wireless devices. 
    
    Flex sensors are used to detect the bending of the fingers and accelerometer and gyroscope for the hand orientation.

    ![designed-glove](https://user-images.githubusercontent.com/15849927/67158689-f97e8200-f358-11e9-86fd-b92323275008.jpeg)

- ## Software
    Once the data is collected using the glove, we use LSTM to translate the gestures in to the corresponding text and speech output.


## Results
- ### Loss Accuracy Curves
![loss_acc_curves-reference](https://user-images.githubusercontent.com/15849927/67158779-ea4c0400-f359-11e9-846c-5c79f176d34e.png)

- ### Confusion Matrix
![confusion_matrix](https://user-images.githubusercontent.com/15849927/67158780-ea4c0400-f359-11e9-890c-eff888113694.png)

## Contributers
- [Ebey Abraham](https://github.com/MrGrayCode)
- [Akshatha Nayak](https://github.com/Aksh77)
- Ashna Iqbal

