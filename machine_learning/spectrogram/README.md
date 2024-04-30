# Audio Identification with a Neural Network

The goal of this project is to identify audio data using a neural network.

## Convolutional Neural Network

A convolutional neural network that identifies images from a large set of data can also be used to analyze audio data if
the audio data can be represented as an image.

![cnn.png](cnn.png)

In the example above, images of handwritten digits are identified as a digit by the convolutional neural network.

## Image Representation of Audio

Sound can be represented as a change in frequencies over time. This can be graphed as a three-dimensional graph with one
axis as time, another as frequency, and another as the amount of that frequency present. As an image, the horizontal
axis can be time, the vertical axis can be frequency, and the color can be the amount of frequency present. 

This type of image is known as a spectrogram, and they are often depicted with all three color channels for easier 
viewing. However, for the purposes of using them in a neural network, the color channel can be grayscale since it is 
one-dimensional. Spectrograms are useful for audio processing, however, they are useful for other types of data 
involving waves, such as data used in seismology.
