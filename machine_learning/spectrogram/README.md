# Audio Identification with a Neural Network

The goal of this project is to identify audio data using a neural network.

A neural network is created to identify what instrument an audio file corresponds to.

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

There exists more than one way to measure the frequencies of a wave over time. The two methods explored for this project
are Fast Fourier Transform (FFT) and Continuous Wavelet Transform (CWT).

### Fast Fourier Transform

![fft_example.png](fft_example.png)

The Fast Fourier Transform provides higher accuracy measurements when compared to the Continuous Wavelet
Transform, but less information about the time at which the frequencies occur.

### Continuous Wavelet Transform

![cwt_example.png](cwt_example.png)

The Continuous Wavelet Transform trades a bit of accuracy on the frequencies for more accurate time measurement.

Both of these spectrogram types will be generated for the same audio data set, and the performance of the neural network
on each type will be compared to infer which is better for machine learning on audio.

## Creating the Neural Network

This project uses a large selection of short audio files of instrument samples, containing many different versions of
the same instruments, which allows the neural network to learn. Each file is placed in a folder with the name of the
instrument.

The [spectrogram.py](spectrogram.py) file reads through all the audio files and generates the FFT and CWT
representations and places them in a separate folder.

The [neural_network.py](neural_network.py) file converts each image into floating point matrices for the input data, and
an integer corresponding to the instrument type for the output data. This data is split into training and testing data
so that the neural network can learn and test its performance. The convolutional neural network model is then ran on the
training data to generate the weights and tested against the testing data to measure its performance.

The number of images, size of the images, and the width and depth of the neural network can each contribute to the speed
at which the model can train. Images of 1000 x 1000 pixel dimensions or a hidden layer of width 1000 can cause the
model training to take hours.

## Outcome



## How view of AI has changed

## Code

## Sources


